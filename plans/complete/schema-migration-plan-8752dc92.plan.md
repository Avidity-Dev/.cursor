<!-- 8752dc92-90ac-47ea-8612-297917b9dd2f 7a234a12-a289-478c-9576-b7ff5253d68a -->
# Schema Migration: EDW.INGEST_VEEVA to INGEST.VEEVA_NETWORK/VEEVA_OPENDATA

## Overview

Migrate dbt source definitions from the consolidated `EDW.INGEST_VEEVA` schema to separate `INGEST.VEEVA_NETWORK` and `INGEST.VEEVA_OPENDATA` schemas, removing `vn__` and `od__` table prefixes.

## Changes Required

### 1. Create Git Worktree

Create a new worktree named `schema-migration` from main branch for isolated development.

### 2. Update dbt Source Definitions

**File**: `transforms/models/_sources/edw_ingest_veeva.yml`

Split the single source into two separate sources:

- **ingest_veeva_network** source (database: `INGEST`, schema: `VEEVA_NETWORK`)
- `HCP` (was `vn__hcp`)
- `HCO` (was `vn__hco`)
- `ADDRESS` (shared with OpenData)

- **ingest_veeva_opendata** source (database: `INGEST`, schema: `VEEVA_OPENDATA`)  
- `HCP` (was `od__hcp`)
- `HCO` (was `od__hco`)
- `ADDRESS` (was `od__address`)
- `AFFILS` (was `od__affils`)
- `HCO_HIERARCHY` (was `od__hco_hierarchy`)

Preserve all column definitions, descriptions, freshness checks, and tests from the existing source file.

### 3. Update Staging Models

Update `source()` references in 7 staging models:

- `transforms/models/staging/stg_hco.sql` - Change from `source('edw_ingest_veeva', 'od__hco')` to `source('veeva_opendata', 'HCO')`
- `transforms/models/staging/stg_vn_hco.sql` - Change to `source('veeva_network', 'HCO')`
- `transforms/models/staging/stg_hcp.sql` - Change to `source('veeva_opendata', 'HCP')`
- `transforms/models/staging/stg_vn_hcp.sql` - Change to `source('veeva_network', 'HCP')`
- `transforms/models/staging/stg_addresses.sql` - Change to `source('veeva_opendata', 'ADDRESS')`
- `transforms/models/staging/stg_affiliations.sql` - Change to `source('veeva_opendata', 'AFFILS')`
- `transforms/models/staging/stg_hco_hierarchy.sql` - Change to `source('veeva_opendata', 'HCO_HIERARCHY')`

### 4. Update dbt Test Expressions

Update hardcoded schema paths in test expressions:

- `transforms/models/_sources/edw_ingest_veeva.yml` lines 51, 137, 211 - Change `edw.ingest_veeva.od__hco`, `edw.ingest_veeva.vn__hco`, etc. to new paths
- Example: `(SELECT COUNT(*) FROM edw.ingest_veeva.od__hco)` → `(SELECT COUNT(*) FROM ingest.veeva_opendata.hco)`

### 5. Create Python Reference Document

**File**: `docs/reports/schema_migration_python_references.md`

Document all 31 Python files that reference the old schema for manual review:

- List file paths
- Show line numbers and specific references
- Categorize by file type (config, repository, script, notebook, test)
- Provide search/replace guidance

## Verification Steps

1. Compile dbt models: `make dbt_compile`
2. Run dbt source freshness checks: `dbt source freshness`
3. Run staging model tests: `dbt test --select staging.*`
4. Verify no references to old schema remain in transforms/: `grep -r "edw.ingest_veeva\|EDW.INGEST_VEEVA" transforms/`

## Rollback Plan

If issues arise, delete the worktree and the changes remain isolated from main branch.

### To-dos

- [ ] Create new git worktree named schema-migration from main branch
- [ ] Split edw_ingest_veeva.yml into separate veeva_network and veeva_opendata sources
- [ ] Update source() references in 7 staging SQL models
- [ ] Update hardcoded schema paths in dbt test expressions
- [ ] Generate documentation of Python files with old schema references
- [ ] Verify dbt compilation and test execution succeeds