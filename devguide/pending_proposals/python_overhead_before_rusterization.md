# Propuesta: el overhead de Python **antes** de rusterizar

**Estado:** propuesta (2026-07-12). **Todo medido**, con el comando al lado.
**Origen:** perfilado desde MolSysViewer, investigando por qué una operación del visor costaba
10 ms. Ver `molsysviewer/devguide/pending_proposals/import_cost_and_lazy_loading.md`.
**Relación con [`rusterization_pyunitwizard_core.md`](rusterization_pyunitwizard_core.md):** no lo
contradice, pero **cambia su orden**. Léase primero éste.

---

## 1. El dato que cambia la prioridad

Medido sobre `puw.get_value(q, to_unit="nanometers")` (Python 3.13, pint como *form* por defecto):

| | coste | % |
|---|---|---|
| **pint desnudo — el trabajo real** | **17 µs** | **7 %** |
| overhead de los decoradores, **incluso desactivados** | 127 µs | 49 % |
| telemetría activa (SMonitor) | 118 µs | 45 % |
| **total `puw.get_value`** | **262 µs** | **15× pint** |

```bash
python -c "
import timeit, pint
from pyunitwizard import ...   # configurado con pint
ureg = pint.UnitRegistry(); qp = 1.5*ureg.angstrom; qw = puw.quantity(1.5,'angstroms')
print(timeit.timeit(lambda: qp.to(ureg.nanometer).magnitude, number=3000)/3000*1e6, 'µs  pint')
print(timeit.timeit(lambda: puw.get_value(qw, to_unit='nanometers'), number=3000)/3000*1e6, 'µs  puw')"
```

**El cálculo es el 7 % del coste. El 93 % es la capa que lo envuelve.**

### Por qué esto afecta a la propuesta de rusterización

`rusterization_pyunitwizard_core.md` propone llevar la validación y conversión a Rust, y sitúa el
cuello de botella en *"el wrapper de Pint, el parseo de strings de unidades y el GIL"*.

**Si el cálculo se hiciera infinitamente rápido —0 µs— la llamada seguiría costando 245 µs.** Una
mejora del **7 %**, a cambio de una toolchain de Rust, PyO3, Maturin y un core nativo que
mantener.

Eso **no invalida** la rusterización: para operaciones sobre arrays **muy** grandes (una trayectoria
entera de coordenadas en una sola llamada) el cálculo sí puede llegar a dominar. Pero el caso común
del ecosistema no es *una llamada gigante*: son **miles de llamadas pequeñas**, y ahí el coste es
**fijo** — medido, un array de 1000×3 cuesta **lo mismo que un escalar** (253 µs vs 262 µs), porque
el tiempo no está en los datos, está en el despacho.

**Recomendación: quitar el overhead de Python primero.** Cuando la llamada baje de 262 µs a ~30 µs,
se podrá volver a medir y **entonces** decidir si el cálculo importa lo suficiente como para
rusterizarlo. Optimizar el 7 % antes que el 93 % es invertir el orden.

---

## 2. Los tres problemas, medidos

### 2a. El coste de los decoradores — **se arregla en SMonitor y DepDigest, no aquí**

Con SMonitor **desactivado**, `puw.get_value` sigue costando **143 µs**, frente a los 17 µs del
trabajo real: **el modo apagado cuesta 7,5× el cálculo.** La causa es que el `if not enabled` llega
*después* de construir el manager, y que DepDigest se decora a sí mismo con `@signal`.

**Esos dos arreglos no pertenecen a este repositorio, y no se documentan aquí.** Están, con las
mediciones, donde toca:

- `smonitor/devguide/pending_proposals/overhead_optimization_and_profiles.md` — el *fast path* del
  decorador. *(La propuesta ya existía; le faltaban los números.)*
- `depdigest/devguide/pending_proposals/fast_dependency_cache.md` — el cache, más dos defectos que
  esa propuesta no cubría: el auto-decorado con `@signal` y el `resolve_config()` por llamada.

**Se mencionan aquí sólo porque el coste se paga en PyUnitWizard**, y porque sin ellos los arreglos
de §2b y §2c rinden mucho menos de lo que podrían.

### 2b. PyUnitWizard entra en 22 funciones internas por llamada, **repitiendo trabajo**

Perfilado de 100 llamadas a `puw.get_value`:

```
   3×  _private/forms.py:8    digest_form        ← detecta el mismo "form" TRES veces
   3×  _private/forms.py:38   digest_to_form
   2×  api/introspection.py   get_form
   2×  api/conversion.py:68   convert
   2×  _private/parsers.py:3  digest_parser
   ───────────────────────────────────────────
   22 llamadas internas para convertir 1,5 Å a nm
```

**Esto es trabajo tirado con independencia de lo que cueste un decorador.** El *form* de una
cantidad no cambia a mitad de la llamada: detectarlo tres veces es puro despilfarro.

**Arreglo:** resolver el *form* y el *parser* **una vez** al entrar en la función pública, y pasarlos
hacia dentro. No cambia la API.

### 2c. Los helpers privados están decorados

**Doce funciones de la API llevan `@digest` / `@signal`** (validation 2, construction 2, extraction
4, conversion 3, context 1), y una llamada pública las atraviesa. Resultado medido: **4.800
invocaciones del decorador de SMonitor y 3.000 de DepDigest para 300 llamadas** — 16 y 10 por
llamada, respectivamente.

**Un `@signal` pertenece a la frontera pública de la librería, no a cada helper que ésta se llama a
sí misma.** La telemetría quiere saber que el usuario llamó a `get_value`, no que `get_value` llamó
tres veces a `digest_form`.

**Arreglo:** decorar **sólo** la superficie pública. Dentro, funciones desnudas.

---

## 3. Y un problema de import: seis backends para declarar unos `TypeVar`

`pyunitwizard/_private/quantity_or_unit.py` importa **todos** los backends de unidades instalados
—pint, openmm.unit, unyt, astropy.units, physipy, quantities— dentro de `try/except`, **sólo para
construir unos `TypeVar`**:

```python
try:
    import unyt                                # ← arrastra sympy y matplotlib
    quantity_types.append(unyt.unyt_quantity)
except:
    pass
```

Un consumidor que sólo use pint (como MolSysViewer, que hace
`set_default_form('pint')`) **paga igual**:

| | RSS |
|---|---|
| pint + openmm.unit | 146 MB |
| + unyt, astropy, physipy, quantities | 211 MB |
| **desperdicio, siempre, nunca usado** | **65 MB** |

Y es el 50 % del tiempo de importar PyUnitWizard (`python -X importtime`): 1,70 s de los 1,93 s se
van en `_private/quantity_or_unit`.

**En runtime un `TypeVar` no valida nada.** Se puede:

- declararlos bajo `TYPE_CHECKING` (coste cero en ejecución), o
- construir la lista **perezosamente**, la primera vez que se pida, o
- importar **sólo los backends configurados**.

Cualquiera de las tres devuelve **65 MB y 1,7 s** a todo el ecosistema.

---

## 4. Qué esperar de cada arreglo

| arreglo | dónde | `get_value` pasa de 262 µs a… |
|---|---|---|
| fast path del decorador (§2a) | SMonitor | ~145 µs |
| resolver el *form* una sola vez (§2b) | **PyUnitWizard** | ~90 µs (estimado — **medir**) |
| desdecorar los helpers privados (§2c) | **PyUnitWizard** | ~30 µs (estimado — **medir**) |
| rusterizar el cálculo | PyUnitWizard | −17 µs sobre lo que quede |

**Los tres primeros son cambios de una tarde y no tocan la API.** El cuarto es un proyecto.

Las estimaciones de §2b y §2c están marcadas como tales **a propósito**: son las únicas cifras de
este documento que no he medido, porque medirlas exige hacer el cambio. Todo lo demás lleva su
comando al lado.

---

## 5. Cómo se verifica

```bash
# el objetivo: acercarse a pint, no a 15× pint
python -c "
import timeit
from pyunitwizard import ...
q = puw.quantity(1.5,'angstroms')
t = timeit.timeit(lambda: puw.get_value(q, to_unit='nanometers'), number=3000)/3000
print(f'{t*1e6:.1f} µs   (hoy: 262 µs | pint desnudo: 17 µs)')"

# el import
python -X importtime -c "import pyunitwizard" 2>&1 | tail -1        # hoy: ~1,9 s
/usr/bin/time -v python -c "import pyunitwizard" 2>&1 | grep Maximum # objetivo: −65 MB
```

Y `benchmarks/` + `performance_baseline_0.20.x.json` ya existen en este repositorio: **este trabajo
debería moverles la aguja de forma visible.** Si no lo hace, es que el diagnóstico está mal — y
entonces hay que volver a medir, no seguir optimizando.

## Implementación y resultados (2026-07-12)

Las optimizaciones previas a cualquier rusterización alcanzan el objetivo de esta propuesta:

| estado acumulado | `get_value(..., to_unit="nanometers")` |
|---|---:|
| línea base original | 262 µs |
| fast path desactivado de SMonitor | 137,9 µs |
| sin auto-instrumentación de DepDigest | 125,8 µs |
| condiciones `when` sin `Signature.bind` caliente | 54,1 µs |
| sin reconversión recursiva de la unidad ya parseada | **28,6 µs** |
| Pint desnudo | 17 µs |

Además, `_private/quantity_or_unit.py` deja de importar seis backends para construir tipos runtime.
Los aliases completos existen sólo bajo `TYPE_CHECKING`; en ejecución son `Any`. La importación
directa de ese módulo baja de **1,91 s / 217 MB** a **0,12 s / 25 MB** en este host. El adaptador de
un objeto externo se registra perezosamente desde `get_form`, de modo que un objeto Pint carga sólo
Pint, no todos los backends instalados.

La última mejora de conversión no elimina una validación: `_parse_unit_string` ya había producido
una unidad en el `to_form` correcto, pero `convert` volvía a pasarla recursivamente por la API
pública antes de usarla. Ahora la entrega directamente cuando el backend coincide; si Matplotlib u
otro cliente proporciona una unidad de un backend distinto, se traduce directamente mediante
`dict_translate_unit`, sin reentrar en los cinco decoradores de dependencia.

`benchmarks/conversion_baseline.py` incluye el caso `get_value_nm_to_angstrom` para vigilar este
camino. Con 28,6 µs frente a 17 µs del backend, rusterizar deja de ser una respuesta al overhead de
despacho; sólo debe reevaluarse para cargas donde el cálculo numérico domine de verdad.

Con la telemetría activa, sin profiling, la misma llamada mide **64,9 µs**. Es una reducción de 4×
frente a los 262 µs originales, pero confirma que las llamadas internas entre funciones que también
son API pública aún generan señales anidadas. Separar wrappers públicos de implementaciones
privadas puede reducir ese coste diagnóstico en una ronda posterior; no es necesario para el
objetivo de producción desactivada de ~30 µs alcanzado aquí.
