# Cloud material-data transfer inventory

Prepared 12 October 2026 for the Starbase Material Selection System.

**All 14 collections containing 6,265,691 records are uploaded and reconciled in TiDB.** All 37 teammate materials are staged in `Contribution_Review`. The cloud-backed local API verifies the complete catalog. The dashboard reports 5.48 GiB row storage, exceeding the free 5 GiB allowance; no paid spending limit is enabled. See [the TiDB transfer guide](tidb-transfer.md) and [verification report](tidb-verification.json).

## Verified normalized snapshots

14 source collections contain **6,265,691 expected source records**. All normalized files match their manifest SHA-256 digests. JSON counts were parsed; JSONL counts were read from the headers of matching full-file snapshots. Overlapping collections and separate source observations are included in this total.

| Source | Records | Evidence |
| --- | ---: | --- |
| NIST JARVIS-DFT elastic benchmarks | 19,335 | computed |
| Borg et al. experimental MPEA alloys | 1,545 | experimental |
| Outokumpu Core stainless steels | 31 | literature-extracted |
| Outokumpu Supra stainless steels | 22 | literature-extracted |
| Outokumpu Forta stainless steels | 28 | literature-extracted |
| MaterialRegistry engineering references | 702 | literature-extracted |
| NASA Goddard vacuum outgassing tests | 12,859 | experimental |
| NASA TPSX thermal protection materials | 1,545 | literature-extracted |
| AFLOW elastic and thermal calculations | 5,664 | computed |
| Materials Project core crystal properties | 154,377 | computed |
| Materials Project GNoME crystal properties | 116,948 | computed |
| NOMAD published elastic calculations | 120 | computed |
| Alexandria PBE 3D calculations | 5,777,914 | computed |
| Alexandria PBE convex-hull subset | 174,601 | computed |

The normalized import files occupy 4.52 GB. The entire download cache contains 1,680 files and occupies 8.80 GB, including raw archives and normalized outputs. File-level paths, sizes, source URLs, licenses and normalized checksums are recorded in `cloud-data-inventory.json`.

## Current transfer constraints

The application uses TiDB's MySQL protocol with verified TLS. Its private cloud configuration is saved in the Git-ignored `server/.env.tidb`; the local database configuration is retained separately. All normalized snapshots have been fully parsed and hash-verified. The two Alexandria streams were restored from their raw archives and match the original normalized SHA-256 values exactly. Lossless Alexandria packing removes 2.12 GB of repeated main-source fields, but final metered row storage still exceeds the free allowance.

## Transfer sequence

1. Inspect the selected TiDB instance's version, available storage, connection configuration and existing schema. Read the current cloud schema before making changes.
2. Select the matching schema and loader. Preserve source keys, external IDs, property units, evidence labels, conditions, provenance, licenses and missing values. Retain Alexandria main/hull and Materials Project core/GNoME as separate collections.
3. Import all 14 verified normalized snapshots in bounded, restartable batches. Track each source checksum, committed progress, expected count and completion state. Avoid changing local import configuration while its existing process runs.
4. Reconcile cloud source counts and property coverage against the inventory; check sample record values and metadata. Mark each collection complete only after reconciliation.
5. Preserve original downloaded snapshots in the cloud storage service selected for the project, with an object/path manifest linked to database source metadata. The destination for original archives still needs to be chosen.
6. Configure the backend for the cloud database and verify the live health endpoint, library search, material details and recommendations.
7. Stage the reviewed teammate contribution in `Contribution_Review`. Obtain property-level citations and traceable price quotations before normalizing those records into the active catalog.

Data not actually downloaded is outside this inventory. The JARVIS collection here is the elastic benchmark snapshot; the full JARVIS archive and unavailable vendor exports are not represented.

Queryable catalog transfer and cloud-backed local API verification are complete. Raw archives remain local; a cloud object-storage destination was not supplied. Hosted backend cutover remains a separate deployment step. Capacity above the free allowance still needs resolution.
