# Propuesta: remedición del coste de telemetría y dónde poner la frontera de `@signal`

**Estado:** propuesta (2026-07-19). Todo medido en este host, con el comando al lado.
**Origen:** trabajo de rendimiento en SMonitor (`smonitor` en `main`, commits `023e39f` y `df86d5d`),
tras el cual las cifras de telemetría de este repositorio dejaron de reproducirse.
**Relación con [`python_overhead_before_rusterization.md`](python_overhead_before_rusterization.md):**
lo continúa. Aquella propuesta ya está implementada y su sección de resultados es correcta salvo por
una cifra —los 64,9 µs con telemetría activa—, que este documento actualiza y explica.

---

## 1. Lo que ha cambiado, sin tocar este repositorio

`python_overhead_before_rusterization.md` cierra diciendo:

> Con la telemetría activa, sin profiling, la misma llamada mide **64,9 µs**. […] confirma que las
> llamadas internas entre funciones que también son API pública aún generan señales anidadas.

Esa medición era exacta. Medida hoy contra el SMonitor de aquel momento reproduce **65,0 µs**. Pero
con el SMonitor actual, y **sin ningún cambio en PyUnitWizard**, la misma llamada mide **39,5 µs**:

| `puw.get_value(q, to_unit="nanometers")` | SMonitor de 2026-07-12 | SMonitor actual |
|---|---:|---:|
| con telemetría activa | 65,0 µs | **39,5 µs** |
| con telemetría desactivada | 28,4 µs | 29,0 µs |
| coste de la telemetría | 36,6 µs | **10,5 µs** |

El camino desactivado está igual, como debe ser: aquel *fast path* ya estaba hecho. Lo que bajó 3,5×
es el camino **activo**, que es donde corren los usuarios.

### Composición actual de la llamada (39,5 µs)

| | coste | % |
|---|---:|---:|
| pint desnudo — el trabajo real | 15,6 µs | 39 % |
| overhead propio de PyUnitWizard | 13,4 µs | 34 % |
| telemetría de SMonitor | 10,5 µs | 27 % |

Conviene contrastarlo con la tabla que abre la propuesta anterior: SMonitor era el **45 %** de una
llamada de 262 µs. Hoy es el **27 %** de una de 39,5 µs.

---

## 2. Dos cifras de §2c que ya no se reproducen

La sección **2c** de la propuesta anterior afirma:

> **4.800 invocaciones del decorador de SMonitor** […] para 300 llamadas — 16 […] por llamada.
> […] **Arreglo:** decorar **sólo** la superficie pública. Dentro, funciones desnudas.

Medido hoy, son **5 wrappers por llamada**, no 16. Y —esto importa más que el número— **los cinco
son API pública**, no helpers privados:

```
1. pyunitwizard.api.extraction.get_value      ← lo que el usuario llamó
2. pyunitwizard.api.conversion.convert
3. pyunitwizard.api.introspection.get_form
4. pyunitwizard.parse.parse
5. pyunitwizard.api.introspection.get_form    ← segunda vez
```

El arreglo que proponía §2c —«decorar sólo la superficie pública»— **ya está hecho**. Lo que queda no
es superficie pública decorada de más: es superficie pública **llamándose a sí misma**.

Eso invalida la instrucción tal como está escrita. Aplicada literalmente hoy, significaría quitar
`@signal` de `convert`, `get_form` y `parse` — que son precisamente funciones que un usuario puede
llamar directamente, y perderíamos su señal cuando lo haga.

*(No he vuelto a medir el lado de DepDigest, que §2c también cita con 10 invocaciones por llamada.
Esa cifra queda sin verificar en este documento.)*

---

## 3. El dato que más orienta la decisión: no se emite nada

En 50 llamadas a `puw.get_value` se emiten **cero eventos**.

Los 10,5 µs no producen ninguna señal: son el coste de *estar preparado* para producirla. Es el caso
silencioso, y es el que domina en cualquier bucle numérico. Cualquier razonamiento sobre "el valor
diagnóstico de estas señales" debe partir de ahí: en el camino caliente, hoy, ese valor es cero
eventos y 10,5 µs.

---

## 4. Qué queda por decidir, con su precio

El ahorro disponible, si sólo el punto de entrada quedara instrumentado:

| | µs |
|---|---:|
| telemetría hoy (5 wrappers × 2,1 µs) | 10,5 |
| telemetría con 1 solo wrapper | 2,1 |
| **ahorro** | **8,4 µs — el 21 % de la llamada** |

### Cómo cobrarlo sin perder señales

Quitar `@signal` de `convert`, `get_form` y `parse` **sí** perdería señales: son API pública. Pero
hay una forma de no perder ninguna, que es la que ya insinuaba el cierre de la propuesta anterior
—separar el wrapper público de la implementación privada:

```python
@signal
def get_form(item):
    return _get_form(item)      # frontera pública: emite

def _get_form(item):            # implementación: no emite
    ...
```

Los llamadores internos usan `_get_form`. Un usuario que llame a `get_form` sigue generando su
señal, exactamente como hoy. Lo que desaparece no es señal: es la **repetición anidada** de una
señal por una llamada que el usuario no hizo.

Ése es justo el criterio que la propuesta anterior ya enunciaba:

> La telemetría quiere saber que el usuario llamó a `get_value`, no que `get_value` llamó tres veces
> a `digest_form`.

### Lo que sí se paga

Conviene decirlo antes de decidir, no después:

- **Atribución de errores menos precisa.** Hoy, una excepción dentro de `get_form` llamada desde
  `convert` se emite con `source` apuntando a `get_form`, y la cadena de breadcrumbs muestra el
  camino. Con la implementación privada sin decorar, el evento se atribuiría al wrapper decorado más
  cercano. La excepción sigue propagándose y sigue emitiéndose; lo que se pierde es resolución.
- **Duplicación de superficie.** Cada función pública pasa a tener dos formas, y hay que mantener
  la disciplina de que los llamadores internos usen la privada. Es el tipo de invariante que se
  degrada en silencio si no se vigila.
- `get_form` se atraviesa **dos veces** por llamada. Eso es el problema §2b de la propuesta anterior
  —trabajo repetido—, no un problema de decoradores. Resolverlo primero podría hacer innecesaria
  parte de esta discusión: serían 4 wrappers en vez de 5 sin tocar ninguna frontera.

**Recomendación:** atacar §2b (resolver el *form* una sola vez) **antes** que esta separación. Es más
barato, no toca fronteras, no degrada la atribución de errores, y reduce el número de wrappers como
efecto secundario. Volver a medir después, y decidir entonces si los ~8 µs restantes justifican
duplicar la superficie pública.

---

## 5. Y lo que ya no hay que arreglar aquí

El §2a de la propuesta anterior —el coste de los decoradores— puede darse por cerrado desde el lado
de SMonitor. Lo que queda por wrapper son ~2,1 µs, y el suelo del diseño está en torno a los 1,2 µs
por llamada decorada: el resto son dos escrituras de `ContextVar` que compran el aislamiento correcto
entre tareas `asyncio` y threads. Bajar de ahí exige renunciar a ese aislamiento, y no debe hacerse.

En otras palabras: **el siguiente bloque de coste del tamaño del nuestro ya no es SMonitor, son los
13,4 µs de overhead propio de PyUnitWizard** (§2b y siguientes).

---

## 6. Cómo se verifica

```bash
python -c "
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw, smonitor, pint, timeit
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm','ps','K','mole','amu','e','kJ/mol','kJ/(mol*nm**2)'])
q = puw.quantity(1.5,'angstroms')
ureg = pint.UnitRegistry(); pq = 1.5*ureg.angstrom
us = lambda f: timeit.timeit(f, number=5000)/5000*1e6
print(f'{us(lambda: pq.to(ureg.nanometer).magnitude):5.1f} us  pint desnudo')
smonitor.configure(enabled=False, handlers=[])
print(f'{us(lambda: puw.get_value(q, to_unit=\"nanometers\")):5.1f} us  puw, telemetria off')
smonitor.configure(enabled=True, handlers=[])
print(f'{us(lambda: puw.get_value(q, to_unit=\"nanometers\")):5.1f} us  puw, telemetria on')"
```

Contar wrappers atravesados por llamada:

```bash
python -c "
import warnings; warnings.filterwarnings('ignore')
import pyunitwizard as puw, smonitor
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm','ps','K','mole','amu','e','kJ/mol','kJ/(mol*nm**2)'])
q = puw.quantity(1.5,'angstroms')
smonitor.configure(enabled=True, handlers=[])
m = smonitor.get_manager(); before = m.report()['calls_total']
for _ in range(100): puw.get_value(q, to_unit='nanometers')
print((m.report()['calls_total'] - before)/100, 'wrappers por llamada')"
```

`benchmarks/conversion_baseline.py` ya vigila `get_value_nm_to_angstrom` con la telemetría
desactivada. **Sugerencia:** añadir el mismo caso con telemetría activa, que es el modo en el que
corre un usuario real y el único donde estos 10,5 µs son visibles.

---

## 7. Procedencia

Medido en un solo host: Python 3.13, x86_64, Linux 6.17, `pyunitwizard` 0.22.0, `pint` como *form*
por defecto, SMonitor en `main` tras `df86d5d`. Los antes/después de §1 se obtuvieron ejecutando el
mismo script contra dos *worktrees* de SMonitor en la misma sesión, con el pint desnudo como
control: se mantuvo en 15,6–17,3 µs en todas las corridas.

Una cautela sobre las cifras por wrapper: los microbenchmarks de SMonitor
(`benchmarks/signal_enabled.py`) miden una función sintética de un solo argumento posicional y dan
~1,24 µs por wrapper. Aquí, con argumentos reales y `**kwargs`, salen ~2,1 µs. **El microbenchmark
subestima el coste real en torno a 1,7×**; sirve para comparar antes/después, no para predecir
absolutos en este repositorio.
