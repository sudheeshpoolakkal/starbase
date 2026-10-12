# Teammate material seed review

Reviewed 12 October 2026. The exact attachment is preserved in
`contributions/teammate-material-seed.original.sql`. The linked review JSON keeps
every contributed material, property, category, claimed source, process and cost.

The contribution contains **37 materials, 45 property observations, 7 processes,
14 process mappings and 37 price entries**, plus 5 categories and 3 claimed data
sources. An in-memory SQLite inspection found no dangling references or duplicate
material codes. This checks internal structure; it does not validate the values.

## How to use the contribution

Keep the current application's catalog schema as the integration target. Do not
execute the attachment against the application database. The app expects
`Material.name`, `Data_Source.source_key`, a reusable `Property` dictionary and
numeric/text values in `Material_Property`; the attachment defines different
columns under overlapping table names. Its hard-coded IDs also do not identify
records in the downloaded sources.

The TiDB transfer command can preserve all 37 records in a separate
`Contribution_Review` table. This table is excluded from library queries and
recommendations. Each staged record retains the original SQL digest, original
IDs, density, properties with units/conditions, claimed source, processes with
scores/notes, and costs with dates/suppliers. Staging is idempotent and preserves
an existing review status on repeat uploads.

Ask the teammate for the exact datasheet/record link or export, page/table,
grade/product form, test method and property conditions. Supplier prices need a
traceable quotation, product form, quantity, currency and date. The submitted
publisher homepages and supplier names do not establish those particular values.
Review the feasibility-score scale and supporting process evidence too.

After verification, normalize the supported properties through the existing
catalog importer under stable source/external IDs. Keep test conditions and
property citations in metadata. Preserve separately sourced observations even
when the grade names overlap; reconcile grade aliases without deleting records.

## Schema and field mapping

| Submitted field | Integration treatment |
| --- | --- |
| `material_category.category_name` | `Material_Category.name`; preserve the original label in review metadata |
| `material_name`, `material_code` | `Material.name` plus searchable aliases; use a source accession for `external_id` |
| `data_source` homepage/year | Claimed provenance only until the actual property record is identified |
| `density_g_cm3` | `density`, g/cm³, when verified |
| Yield / tensile strength | `yieldStrength` / `tensileStrength`, MPa, retaining condition and product form |
| Compressive strength | A distinct property; requires a catalog extension, never a tensile-strength substitution |
| Thermal conductivity | `thermalConductivity`, W/m·K, retaining measurement temperature |
| Rockwell C / Vickers hardness | Separate `hardnessRockwellC` / `hardnessVickers` fields |
| Melting point | `meltingPoint`; does not establish a service-temperature ceiling |
| Max operating temperature | Review the continuous-use definition and conditions before mapping to `maxServiceTemp` |
| Electrical resistivity, Ω·cm | Convert explicitly to µΩ·m by multiplying by 10,000, when verified |
| Conductivity, MS/m; fracture toughness; dielectric strength; electron mobility | Retain submitted units in staging; add separate property definitions if needed |
| `material_process.feasibility_score`, `notes` | Preserve in staging; app association tables currently do not store these fields |
| USD/kg supplier prices | Preserve as dated quotations pending verification; do not map to the app's ordinal `cost` tier |

The attachment uses inline column-level `REFERENCES`. MySQL and TiDB parse but
ignore these clauses; executable migrations need explicit `FOREIGN KEY (...)`
constraints. See [TiDB's foreign-key documentation](https://docs.pingcap.com/tidb/stable/foreign-key/).
Future cost/process tables should also enforce positive prices and a documented
feasibility-score range. Database-generated IDs avoid collisions with imports.
Material names/codes should not be globally unique across source observations,
conditions and product forms.

## Specific records needing clarification

- Aluminum 6061-T6's investment-casting association needs a grade/product-form review.
- The gray-iron name says G2500 while its code says Class 35.
- The PET record's code and description identify PETG.
- The aramid-composite name contains the spelling `Arimid`.
- Continuous-use limits and all February 2026 supplier prices lack specific citations.

Original values have been preserved. No contributed observation or quotation is
claimed verified, and no teammate row has been added to the active catalog.
