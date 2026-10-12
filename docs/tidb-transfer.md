# Transfer Starbase's downloaded material sources to TiDB

Prepared 12 October 2026. TiDB is the selected provider. Connection credentials,
the instance's storage plan and the live target schema have not yet been supplied
or inspected. **No cloud upload or application cutover has been performed.**

## Transfer scope

The [snapshot inventory](cloud-data-inventory.json) lists all 14 normalized source
collections: 6,265,691 source records and 4.52 GB of normalized files. The full
download cache is 8.80 GB, including raw archives and publisher pages. Counts
include separate observations and overlapping collections, not unique commercial
grades. See [the source breakdown](cloud-data-migration.md).

TiDB receives queryable material records, properties and provenance. Original
BZ2 archives, Parquet files, PDFs and HTML snapshots should also be retained in
object storage with checksum/path metadata when a bucket is available. They are
preserved locally; this command does not upload them as SQL blobs. No raw archive
upload is claimed complete. Undownloaded providers are outside this transfer.

TiDB Cloud Starter's free quota includes 5 GiB of row storage, 5 GiB of columnar
storage and 50 million monthly request units. SQL rows, indexes and the separate
property table mean normalized file size is not a database-capacity estimate.
Check the instance's storage and RU budget before the complete 6.27-million-record
load. No paid plan or spending limit has been enabled by this project. See
[TiDB's plan documentation](https://docs.pingcap.com/tidbcloud/select-cluster-tier/).

During this inspection, MySQL reported approximately 5.14 GiB of allocated data
and indexes for the local `Material` and `Material_Property` tables alone, while
the Alexandria import was still running. This is evidence for checking capacity,
not an exact forecast of TiDB storage usage.

## Configure the private connection

Copy `server/.env.tidb.example` to `server/.env.tidb`, restrict permissions to 600,
and fill in the Connect panel's host, port, full username, password and database
name. Use an empty database dedicated to Starbase, or an existing Starbase schema.
If the instance exposes only `test`, its name can be used after schema inspection.
The command does not create databases or drop existing tables.

```bash
cp server/.env.tidb.example server/.env.tidb
chmod 600 server/.env.tidb
```

`DB_SSL=true` verifies both the certificate chain and hostname. Node's trusted CA
roots work for TiDB Cloud Starter. Set `DB_SSL_CA` to an absolute local CA-file
path if required by the selected endpoint. See
[TiDB's mysql2 connection guide](https://docs.pingcap.com/tidb/dev/dev-guide-sample-application-nodejs-mysql2/).
The cloud file is ignored by Git. The existing local `server/.env` stays in place.

## Verify, inspect, import

Run from the project root:

```bash
# Offline: hash and parse every normalized file; verify counts and property coverage.
npm run data:cloud -- --verify

# Read-only cloud inspection: require TiDB, encrypted transport and compatible tables.
npm run data:cloud -- --check --env server/.env.tidb

# Import all 14 sources in bounded transactions, then stage the teammate records.
npm run data:cloud -- --import --env server/.env.tidb \
  --stage-teammate docs/contributions/teammate-material-seed.review.json
```

The import mode verifies all selected snapshots before the first write. It then
inspects the target before initializing the app schema. Incompatible teammate
tables cause an explicit stop; they are not replaced. Existing users/projects are
not migrated from the local database by this catalog transfer.

The default batch size is 1,000 materials; `--batch-size` accepts 1–5,000. Stable
source keys and external IDs retain the app's upsert behavior. Each successful
batch saves its file position and normalized digest in `Catalog_Import_Progress`.
Rerun the same command after interruption. A batch committed before its checkpoint
may replay safely; database row counts never determine which file rows to skip.
Run one transfer process against the destination at a time.

Each source remains `importing` and unavailable to catalog queries until database
counts, all property-coverage totals, source provenance, and first/middle/last
record samples reconcile. Samples include values, citations/conditions in metadata,
URLs and aliases. Completed sources are verified on repeat runs. Unexplained extra
records cause a reconciliation failure; the loader never silently deletes them.

For a source-specific import or retry, use comma-separated source keys:

```bash
npm run data:cloud -- --import --source nist-jarvis-elastic,borg-mpea
```

The [teammate review](teammate-schema-review.md) explains the separate
`Contribution_Review` table and the citations needed before those values become
active catalog evidence. Her original SQL is retained as an archival contribution.

## Application cutover and verification

After the cloud counts reconcile, point the backend to the same private file:

```bash
STARBASE_ENV_FILE=server/.env.tidb npm start
```

For a hosted backend, configure the corresponding DB variables in its deployment
environment. Keep `DB_SSL=true` and set a persistent `JWT_SECRET`. Verify
`/api/health`, source totals, search, material details, comparison and at least one
engineering and one computed-data recommendation against the live TiDB target.
The runtime reports the MySQL protocol driver as `database: mysql` for TiDB too.
Do not call the migration complete based on a successful connection or importer
exit alone. Local downloads and the local database should be retained until cloud
verification and raw-archive preservation are complete.

## Validation completed in this workspace

- `npm run data:cloud -- --verify`: all 14 normalized SHA-256 values matched;
  every JSON/JSONL material was parsed; exact counts reconciled to 6,265,691.
- `npm test`: 23 passed, 0 failed, 1 existing opt-in MySQL test skipped. New tests
  cover certificate/hostname verification, corrupt/truncated files, zero values,
  checkpoint replay after a simulated connection loss, snapshot changes and
  rejection of incompatible schemas before catalog initialization.
- The original contribution digest, all 37 material rows, all 45 property rows
  and all 37 price rows match the review export exactly.

TiDB connectivity, DDL compatibility, actual cloud transactions, storage/RU
usage, record reconciliation and live API behavior remain unverified until the
private connection configuration is supplied. A disposable MySQL schema test
was unavailable with the current local user's permissions; the local catalog
was not used for synthetic transfer imports.
