<!-- e2e415af-72dd-441f-bf37-c825eb809336 98650447-871d-4519-86b9-b8c447e4a979 -->
# Separate Network from OpenData Attribution Pipeline

## Overview

Refactor the MDM attribution pipeline to calculate primary affiliations using only OpenData, then union Network records back as the source of truth. This enables proper comparison and reconciliation between OpenData-derived affiliations and Network ground truth.

## Current Architecture

```
Staging → Unified (Network + OpenData) → Enriched → Matching → Primary Affiliations
```

## Target Architecture (Phase 1)

```
Staging (with source_system) → Unified (OpenData only) → Enriched → Matching → Primary Affiliations
```

## Target Architecture (Phase 2 - Future)

```
Phase 1 Output → Union Network → Compare & Reconcile
```

---

## Phase 1: OpenData-Only Attribution Pipeline (This Task)

### 1. Add Source Tracking to Staging Models

Add `source_system` column to all staging models with literal values 'NETWORK' or 'OPENDATA'.

**Why:** Establishes clear data lineage from the start. Prepares for future direct staging→enriched flow when we remove unified models.

**Files to modify:**

- `transforms/models/mdm/staging/stg_vn_hcp.sql` - Add `'NETWORK' as source_system`
- `transforms/models/mdm/staging/stg_vn_hco.sql` - Add `'NETWORK' as source_system`  
- `transforms/models/mdm/staging/stg_od_hcp.sql` - Add `'OPENDATA' as source_system`
- `transforms/models/mdm/staging/stg_od_hco.sql` - Add `'OPENDATA' as source_system`
- `transforms/models/mdm/staging/_staging.yml` - Document the new column with tests

**Implementation:** Add column right after existing metadata columns (`_dbt_loaded_at`).

### 2. Modify Unified Models to OpenData Only

Change unified models to ONLY include OpenData records by removing Network from the union.

**Why:** This makes enriched models naturally OpenData-only without needing explicit filters. Since enriched reads from unified, and unified only has OpenData, enriched automatically only has OpenData.

**Files to modify:**

**mdm_hcp_unified.sql:**

- Remove `network_hcps` CTE entirely
- Remove `network_vids` deduplication CTE (no longer needed)
- Keep only `opendata_hcps` CTE
- Simplify final SELECT to just return opendata_hcps (no union)
- Update docstring: "OpenData HCPs only - Network excluded from attribution calculations"

**mdm_hco_unified.sql:**

- Remove `network_hcos` CTE entirely
- Remove `network_vids` deduplication CTE
- Remove `opendata_only` CTE (unnecessary filtering)
- Simplify to just select from `opendata_hcos` 
- Update docstring: "OpenData HCOs only - Network excluded from attribution calculations"

**Result:** Enriched models automatically contain only OpenData with no code changes needed.

### 3. Update Documentation for Downstream Models

Update docstrings in models that now implicitly only contain OpenData.

**Files to modify:**

- `transforms/models/mdm/intermediate/enriched/mdm_hcp_enriched.sql`
    - Update line 22: "Starts with OpenData-only HCP dataset (Network excluded)"
    - Update line 41: "Sources: mdm_hcp_unified (OpenData only)"

- `transforms/models/mdm/intermediate/enriched/mdm_hco_enriched.sql`
    - Update line 22: "Starts with OpenData-only HCO dataset (Network excluded)"
    - Update line 40: "Sources: mdm_hco_unified (OpenData only)"

- `transforms/models/mdm/intermediate/enriched/_enriched.yml`
    - Update `mdm_hcp_unified` and `mdm_hco_unified` descriptions
    - Note: "Attribution calculated from OpenData only. Network records will be added back in future phase for comparison."

### 4. Add Tests for Source Tracking

Add tests to verify source_system column and OpenData-only pipeline.

**In `_staging.yml` for each staging model (stg_vn_hcp, stg_vn_hco, stg_od_hcp, stg_od_hco):**

```yaml
- name: source_system
  description: "Source system identifier: NETWORK or OPENDATA"
  tests:
    - not_null
    - accepted_values:
        values: ['NETWORK', 'OPENDATA']
```

**In `_enriched.yml` for unified models:**

```yaml
tests:
  - dbt_utils.expression_is_true:
      config:
        alias: mdm_hcp_unified_only_opendata
      arguments:
        expression: "(SELECT COUNT(*) FROM {{ ref('mdm_hcp_unified') }} WHERE source_system != 'OPENDATA') = 0"
```

### 5. Test and Validate

Run dbt build commands to verify the refactored pipeline works correctly.

**Commands to run:**

```bash
# 1. Test staging models with new source_system column
dbt build --select stg_vn_hcp stg_vn_hco stg_od_hcp stg_od_hco

# 2. Test unified models (should now be OpenData only)
dbt build --select mdm_hcp_unified mdm_hco_unified

# 3. Test enriched models (should inherit OpenData-only)
dbt build --select mdm_hcp_enriched mdm_hco_enriched

# 4. Test full attribution pipeline
dbt build --select mdm_primary_affiliations_resolved+
```

**Validation queries to run:**

```sql
-- Verify unified only contains OpenData
SELECT source_system, COUNT(*) 
FROM mdm_hcp_unified 
GROUP BY source_system;
-- Expected: Only 'OPENDATA' rows

-- Verify enriched inherited OpenData-only
SELECT source_system, COUNT(*) 
FROM mdm_hcp_enriched 
GROUP BY source_system;
-- Expected: Only 'OPENDATA' rows

-- Check affiliation count change
SELECT COUNT(*) FROM mdm_primary_affiliations_resolved;
-- Expected: Lower than before (only OpenData HCPs now)
```

---

## Phase 2: Network Union and Reconciliation (Future Task - Not AAA-634)

**Status:** Blocked - requires ingestion pipeline changes first

**Blockers:**

- Veeva Network ingestion pipeline doesn't currently capture HCP-HCO affiliation data
- `stg_affiliations` only has OpenData affiliations, not Network affiliations
- Need proper column mapping for Network affiliation data

**Required work (separate Linear issue):**

1. Update dlt Veeva Network source to extract HCP-HCO affiliation relationships
2. Create staging model for Network affiliations (or add to existing `stg_affiliations`)
3. Create `mdm_affiliations_with_network.sql` to union OpenData-derived + Network ground truth
4. Create `mdm_affiliation_reconciliation.sql` to compare and flag differences
5. Define reconciliation business rules (MATCH, MISMATCH, NETWORK_ONLY, OPENDATA_ONLY)
6. Implement decision logic for handling mismatches

**Out of scope for AAA-634.**

---

## Success Criteria (Phase 1)

- [x] All staging models have `source_system` column with tests
- [x] Unified models only contain OpenData records (Network removed from union)
- [x] Enriched models automatically contain only OpenData (no filter needed)
- [x] Primary affiliations calculated from OpenData-only data
- [x] All dbt tests pass
- [x] Documentation updated to reflect new architecture
- [x] Validation queries confirm OpenData-only pipeline

## Open Questions

1. **Network-only HCPs**: In Phase 2, what affiliation should we use for HCPs that only exist in Network? (No OpenData-derived affiliation available)
2. **Mismatch resolution**: When OpenData says HCP→HCO_A but Network says HCP→HCO_B, which wins? Always Network?
3. **Confidence scoring**: Should mismatches reduce confidence scores or trigger manual review?

These will be answered in Phase 2 planning.

### To-dos

- [x] Add source_system column to all 4 staging models and add tests in _staging.yml
- [ ] Refactor mdm_hcp_unified and mdm_hco_unified to only include OpenData (remove Network CTEs and union)
- [x] Update documentation in enriched models and schema files to reflect OpenData-only architecture
- [x] Add tests to verify unified models only contain OpenData records
- [ ] Run dbt build commands and validation queries to verify Phase 1 works correctly