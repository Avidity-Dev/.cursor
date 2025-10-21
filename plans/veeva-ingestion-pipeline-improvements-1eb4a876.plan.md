<!-- 1eb4a876-aa73-4a70-b433-bfb3d61a331d fb30c1f1-c156-4d3e-838e-4ada7f634cc5 -->
# Veeva Ingestion Pipeline Improvements

## Goals

- Increase reliability and idempotency
- Reduce operational risk (partial files, reprocessing)
- Tighten schema/contracts and observability
- Fix scheduling and improve backlog handling

## Cross-Cutting Improvements

### Idempotency and Manifests

- Introduce a persisted manifest (e.g., `ingest.veeva_file_manifest`) to record processed files with: source path, checksum, size, run_id, model, processed_at, rows_loaded, status.
- Skip reprocessing if an identical file (path+checksum) already exists in the manifest.

### Integrity and Validation

- Compute SHA-256 checksum and record count pre-load; verify post-load rows match (or within tolerance when headers/invalid rows are skipped).
- Fail fast on header/schema mismatch; surface actionable error messages.

### Observability

- Standardize Dagster materialization metadata (rows, bytes, checksum, run_id) and emit counters/timers to metrics (e.g., statsd/OpenTelemetry) with consistent tags: pipeline, model, stage.
- Add alerting on repeated failures and anomalous row deltas.

### Security and Access

- Move SFTP auth to key-based credentials; rotate keys; least-privilege.
- Prefer Azure AD/Managed Identity for ADLS over connection strings.

### Data Retention / Lifecycle

- Define ADLS lifecycle policies per prefix (retain N runs); document restore procedure.

### Schema Contracts

- Prefer explicit column schemas where stable; lock file_format options; capture schema drift to a log table and alert.
- Add dbt tests for source freshness and null/not-null/unique constraints on key columns.

## OpenData (SFTP → ADLS → Snowflake)

### Atomicity and Concurrency

- Upload to `.../{model}/_inflight/{filename}.tmp` then atomic rename to final path to avoid partial reads.
- Allow parallel extraction per model (assets already independent) with bounded concurrency.

### Load Hardening

- Switch from pure inference to explicit `CopyConfiguration` per model (where feasible) and set `ON_ERROR=ABORT_STATEMENT` (or staged error handling) with logging of errors into a quarantine table.
- Optional: move from TRUNCATE to MERGE on stable natural keys if business requires incremental updates.

### Scheduling Fix

- Wire the OpenData schedule to the OpenData job (currently points to Link).
```24:30:prometheus/veeva/schedules.py
opendata_full_export_schedule = dg.ScheduleDefinition(
    name="opendata_full_export_schedule",
    job=link_full_export_job,  # should target the OpenData job
    cron_schedule="0 18 * * 0",
    execution_timezone="America/Los_Angeles",
    default_status=dg.DefaultScheduleStatus.RUNNING,
)
```


### Idempotent Uploads

- Before ADLS upload, check manifest for (model, run_id) or (path, checksum); skip duplicates.

## Network (SFTP → Snowflake via dlt)

### Sensor Backlog Handling

- Process all new directories newer than the cursor in order (not just latest). Batch multiple RunRequests or a single run with all directories.

### Robust File-to-Model Mapping

- Make regex tolerant to suffix/prefix variations and case; log unmapped files explicitly and quarantine.

### dlt Load Guarantees

- Enforce CSV dialect (delimiter, quote, escape) explicitly; reject malformed rows or write them to an error table.
- Add per-file idempotency using manifest; skip if already processed.

### Optional ADLS Staging (Hybrid)

- If auditability is required, stage CSVs to ADLS first (like OpenData) then load; keep direct path as default if latency is paramount.

## Operations

- Add manual backfill parameters: allow selecting a historical run_id/directory.
- Document runbooks for retry, backfill, and cursor reset.

## Acceptance Criteria

- No partial files observed by loaders (atomic writes verified)
- Re-running on same input skips cleanly (manifest proven)
- Schema/row count mismatches alert within 5 minutes
- OpenData schedule triggers the correct job
- Network sensor processes multiple new directories in order

### To-dos

- [ ] Wire OpenData schedule to OpenData job in `prometheus/veeva/schedules.py`
- [ ] Create `ingest.veeva_file_manifest` to track processed files and outcomes
- [ ] Compute SHA-256 and row counts pre-/post-load; persist in manifest
- [ ] Skip loads when (path+checksum) already processed successfully
- [ ] Upload OpenData files to _inflight/ then atomic rename to final path
- [ ] Define explicit COPY configs per OpenData model (file_format, ON_ERROR)
- [ ] Prototype MERGE for OpenData on stable keys; keep TRUNCATE default
- [ ] Process all new Network dirs newer than cursor, not only latest
- [ ] Harden regex and mapping for Network; quarantine unmapped files
- [ ] Set explicit CSV dialect in dlt; route bad rows to error table
- [ ] Migrate SFTP auth to key-based; rotate keys and update resources
- [ ] Adopt Azure AD/Managed Identity for ADLS resource access
- [ ] Define ADLS lifecycle rules per prefix; document restore
- [ ] Emit standardized metrics and alerts for rows, bytes, duration
- [ ] Add dbt tests for source freshness and key constraints
- [ ] Add run_id/directory params for manual backfills