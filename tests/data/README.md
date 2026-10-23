# Consumer-derived quantity fixtures

`sabueso_activity_quantities.json` contains 343 ChEMBL activity observations
extracted from committed Sabueso fixtures. The source section records exact
Sabueso commit, paths, file hashes and extraction scope. Activity identifiers
retain links to the original database records. Units are explicitly mapped from
ChEMBL `nM`/`%` to canonical `nanomolar`/`percent`; magnitudes, assay types and
source relations are retained. Relations remain provenance, not exact-value or
interval semantics inferred by the codec.

These ChEMBL-derived data are distributed under **CC BY-SA 3.0**, separately
from the software license. Attribution: ChEMBL, EMBL-EBI; source data retained
by `uibcdf/sabueso`. See [ChEMBL's data notice](https://chembl.gitbook.io/chembl-interface-documentation/about)
and [the license](https://creativecommons.org/licenses/by-sa/3.0/). The file
extracts/reformats numerical observations; it does not copy complete source
documents or clinical/personal data.

The H5MSM coordinate fixture and TopoMT record fixture retain their own original
repository/path/commit/hash provenance inside their JSON files. Tiling a retained
coordinate frame in a benchmark is synthetic stress data, not additional
observed simulation frames. Provider tests do not establish consumer migration.
