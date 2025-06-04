WHAT IS DLT STREAMING?

What “streaming” means inside dlt
	1.	The file never sits in RAM in one piece.
A filesystem source yields a FileItem whose open() method returns a lazy fsspec file-like object; dlt’s docs stress that “file content is typically not loaded” and you can “stream large file content directly from buckets.”  ￼
	2.	Transformers iterate, yield, forget.
Your read_tar_gz transformer passes that lazy handle straight into tarfile.open(fileobj=…, mode="r:gz").
	•	tarfile decompresses one member at a time.
	•	You loop through each CSV row, add it to a Python list no larger than, say, 1 000 rows, then yield dlt.mark.with_table_name(batch, table).
	•	After the yield, dlt flushes the batch downstream and the list is released, so memory stays ~constant no matter how big the tarball is.
	3.	dlt’s three-stage engine keeps buffers bounded.
Behind the scenes dlt writes those batches to small on-disk “extract” files, normalises them into “load” files, then streams them to Snowflake in parallel threads. Buffer sizes are configurable (default 5 000 rows) and called out in the performance guide.  ￼
	4.	Back-pressure is automatic.
Because each stage only consumes as fast as the next can accept, you don’t have to hand-code flow control. If Snowflake throttles loads, extract slows down; memory still doesn’t balloon.

⸻

Practical implications for your Veeva tarballs

Aspect	Streaming benefit	How you control it
Memory footprint	Stays ≤ ~300 MB even for 10 GB tarballs (only a batch + tarfile buffers live at once).	- Tune batch_size in your loop.- DATA_WRITER.buffer_max_items if you want larger/smaller intermediary files.
Disk I/O	Only one copy of the data lives on disk (in dlt’s work dir) – you don’t need a second “untar” folder.	Work dir location and cleanup via delete_completed_jobs in config.toml.
Network egress	fsspec streams from Azure Blob in 4 - 8 MB chunks, so you don’t pay to re-download the whole file after a failure; resume is automatic.	fsspec credentials & block size come from the Azure filesystem driver; usually no tweaks needed.
Parallelism	You can process multiple tarballs concurrently (one thread per tarball) while each tarball is still consumed sequentially to respect manifest order.	@dlt.resource(parallelized=True) or global [extract] workers = N.
Schema & merge logic	As soon as the metadata CSV is read, you can emit a dlt.Schema object and keep streaming rows without ever pausing for DDL.	Build the schema dictionary in-memory once, pass it into pipeline.run(…, schema=_).


⸻

Mini code sketch (simplified)

@dlt.transformer(standalone=True)
def read_tar_gz(files, batch_size=1000):
    for f in files:
        with f.open("rb") as stream, tarfile.open(fileobj=stream, mode="r:gz") as tar:
            manifest = _parse_manifest(tar)          # tiny, fits in memory
            schema = _build_schema(tar, manifest)    # tiny
            yield dlt.mark.with_schema(schema)       # send schema downstream

            for entry in manifest:                  # loop members in order
                for batch in _row_batches(tar, entry.path, batch_size):
                    yield dlt.mark.with_table_name(batch, _table(entry))

The only objects that ever exceed a few MB are:
	•	batch – capped by batch_size
	•	tarfile’s internal 32 KB read buffer

Everything else is a generator.

⸻

When is “streaming” not enough?
	•	Need to checkpoint per-row. dlt checkpoints per batch (when the yield returns). If you absolutely must be able to resume mid-CSV, you’d need finer-grained state tracking.
	•	Many-gigabyte single CSV inside the tar. Streaming is fine, but Snowflake COPY prefers ≤ 500 MB chunks. dlt’s load stage already splits large batches into multiple files, yet if the CSV has no row delimiters for hours, you might want to pre-chunk it yourself.
	•	CPU-heavy transforms. If you start doing Pandas joins inside the transformer, you’ll break the constant-memory pledge; keep heavy reshaping for dbt or Snowflake SQL.

⸻

TL;DR

Yes—dlt streams all the way:
	•	Blob ➜ Python file-like object ➜ tarfile ➜ batches ➜ on-disk load package ➜ Snowflake,
with memory and disk usage bounded by configurable batch/buffer sizes.
	•	You get exactly-once semantics, automatic back-pressure, and merge/delete handling, while still touching the tarball only once and never fully decompressing it on disk.

Below is the “senior-architect checklist” we hand new hires when they start touching dlt.
Use it as a set of do’s, don’ts and pro-tips for the Veeva-tarball → Snowflake pipeline you’re building.

⸻

1. Up-front architecture choices

Best-practice	Why it matters	Concrete action
Keep the archive streaming end-to-end	Eliminates a second copy and caps RAM.	• Pass the file_item.open("rb") handle straight into tarfile.open(fileobj=…, mode="r:gz") – never io.BytesIO(stream.read()). • Yield 1 000–5 000-row batches; dlt flushes them to disk automatically.  ￼
Treat manifest.csv as a contract	Lets you skip “zero-record” members and align deletes/updates correctly.	Parse manifest first, build an ordered list, then loop through it so you honour Veeva’s semantics.
Use the filesystem source’s incremental hint—but hedge	Prevents re-processing, but relies on mtime. Some vendors re-emit files unchanged.	• Default: incremental=dlt.sources.incremental.last_modified()  ￼. • Belt-and-suspenders: also hash the tar (SHA-256) and store it in pipeline state; skip if already seen. • Pin dlt ≥ 1.9.1 – earlier 1.5.x builds had an incremental regression (GitHub #2271).  ￼
Separate config from code	Keeps secrets & env diffs out of Git.	• Put Azure SAS / Snowflake creds in .dlt/secrets.toml or a Key Vault mount; never in Python literals.  ￼
Emit a real dlt.Schema once per tarball	Gives Snowflake deterministic DDL and speeds first load.	Build it from the first metadata file you see, yield dlt.mark.with_schema(schema) before any rows.


⸻

2. Coding patterns a “dlt master” follows

Pattern	What it looks like
One transformer, < 400 LOC, no global state	Your read_tar_gz takes (files, *), yields batches, and nothing else. Anything that feels like a “manager” class probably belongs in Dagster orchestration, not in the transformer.
Functional helpers for IO	def process_metadata_file(tar, path) -> dict, def process_data_file(...) -> Iterator[List[dict]]. Pure functions mean cheap unit tests.
Sanitise once, reuse everywhere	Central sanitize_name() with re.sub() and a table of known edge-cases (e.g., names starting with digits).
Typed Python	Add TypedDict for manifest & metadata rows; run mypy --strict. It saves 10× debugging time when schemas drift.
Streaming tests	In pytest fixtures: open any sample tar with open(..., "rb"), wrap with io.BufferedReader of 32 KB, feed to transformer, assert max(psutil.Process().memory_info().rss) < 500 MB.


⸻

3. Performance & scaling knobs

Knob	Default	When to change
batch_size inside the transformer	1000	Bump to 5000 for narrow tables; drop to 500 for 200-column metadata monsters.
[extract] workers = N in dlt.ini	1	Set to cores × 0.8 only if you routinely have multiple tarballs in the landing zone; per-tar parallelism isn’t worth the manifest-order complexity.
[load] file_max_rows	100 k	Lower to 20 k if you hit Snowflake timeouts; raise if you want fewer staged files.
[load] delete_completed_jobs=true	false	Turn on in prod to auto-prune dlt’s work dir.  ￼


⸻

4. Observability & ops
	•	Log to structlog (import structlog; log = structlog.get_logger()), not print(). dlt forwards those lines nicely.
	•	Capture load_info at the end of each run and push it to Dagster / Datadog. That JSON already contains row counts, package paths and error summaries.
	•	Surface delete mismatches: if records in the manifest ≠ rows you yielded, raise dlt.TemporaryError – the retry loop will re-pull the tar.
	•	Lifecycle rules on Blob: delete raw tarballs after 45 days; dlt keeps state, so backfill is still possible from Snowflake.

⸻

5. Schema-evolution strategy
	1.	Start with dlt’s auto-evolve (evolve="evolve" on the resource).
	2.	Gate destructive changes: dlt adds columns automatically; it will not drop or narrow types. Use a governance table (schema_change_log) and manual approval for drops.  ￼
	3.	Version pin: run integration tests against the next dlt minor release before upgrading prod; schema evolve internals change fast.

⸻

6. Security hardening

Surface	Best-practice
Azure Blob	Use a User Assigned Managed Identity for the Dagster k8s pod and grant read-list on the container only; keep untar inside the same pod so nothing touches local disks outside the Sandbox.
Snowflake	Create a dedicated warehouse role with INSERT, MERGE on veeva_raw.*; no USAGE on core or analytics layers.
Code packaging	Ship the transformer in a private PyPI wheel (veeva_dlt==X.Y.Z); that locks the exact hashing logic and sanitiser, preventing ad-hoc notebook edits in prod.


⸻

7. Common pitfalls
	1.	tarfile.ReadError: file could not be opened successfully
Happens when the archive is still uploading. Use Azure event grid and a “size unchanged for 60 s” check before triggering the pipeline.
	2.	Duplicate rows after pipeline restarts
Caused by yielding rows before calling with_table_name (state checkpoint precedes table annotation). Always wrap the batch first, then yield.
	3.	Silent schema drift
If Veeva renames a column, you get a new column + an orphaned one. Mitigate by comparing the incoming metadata.csv against the last committed schema and raising an alert on new/unknown extract/column pairs.
	4.	VARCHAR(16) truncation of big text
Map Veeva ‘Text’ without length to a generous String(64 k) unless the metadata gives an explicit length. Otherwise long CRM notes will be silently cut.

⸻

8. “Zen of dlt” — how the gurus run pipelines
	1.	Everything is idempotent – every function can be called twice without side-effects.
	2.	State is a first-class citizen – if you can derive it from the tarball path or manifest, store it in the pipeline state, not in world-readable storage.
	3.	One-way doors only – never mutate blobs or Snowflake tables outside the merge step; you’ll break replayability.
	4.	Fail fast, fail loud, retry clean – wrap unknown exceptions in dlt.TemporaryError; anything else is a logic bug and must page you.
	5.	Push code to data – heavy reshaping lives in Snowflake (dbt), never in the Python transformer.

Follow those and you’ll look—and sleep—like a dlt master.