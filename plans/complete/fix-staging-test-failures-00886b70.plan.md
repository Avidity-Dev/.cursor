<!-- 00886b70-d4b9-4a2c-b883-d0493ae59944 3534fc61-fba6-4756-8c18-90694f038b81 -->
# Fix Staging Test Failures

## Problem Summary

Staging tests have two categories of failures:

1. **Layer violation**: Relationship tests in staging reference intermediate models
2. **SQL syntax errors**: `expression_is_true` tests with aggregates fail in Snowflake WHERE clauses

## Changes Required

### 1. Move Cross-Layer Relationship Tests (Priority 1)

**File**: `transforms/models/staging/_staging.yml`

- Remove relationship test at line ~37 that references `int_primary_affiliations_dbt`
- This test validates that staging data has corresponding intermediate records (backward dependency)

**File**: `transforms/models/intermediate/results/_results.yml`

- Verify this relationship test already exists or add it
- The test should validate `int_primary_affiliations_dbt.hco_vid` → `stg_hco.hco_vid`
- This is the correct direction: intermediate depends on staging, not vice versa

### 2. Fix Aggregate Expression Tests (Priority 2)

Replace problematic `dbt_utils.expression_is_true` tests with appropriate alternatives:

**Files to update**: `transforms/models/staging/_staging.yml`

**Test Replacements**:

| Current Test | Line | Replacement |
|--------------|------|-------------|
| `stg_addresses` - `count(*) > 0` | ~163-167 | `dbt_utils.row_count` with `min_value: 1` |
| `stg_addresses` - `count(distinct address_vid) > 0` | ~168-173 | Custom singular test or remove (covered by not_null) |
| `stg_hcp` - `count(*) > 0` | ~59 | `dbt_utils.row_count` with `min_value: 1` |
| `stg_hcp` - name check (line ~64) | ~64 | Custom singular test (complex CASE logic) |
| `stg_hcp_specialty` - `count(*) > 0` | ~223 | `dbt_utils.row_count` with `min_value: 1` |
| `stg_hcp_specialty` - `count(distinct specialty) > 0` | ~228 | Custom singular test or remove |
| `stg_target_file_stage` - `count(*) > 0` | ~558-562 | `dbt_utils.row_count` with `min_value: 1` |
| `stg_target_file_stage` - `count(distinct account_type) = 2` | ~563-567 | Custom singular test (business logic) |
| `stg_vn_hcp` - `count(*) > 0` | ~312 | `dbt_utils.row_count` with `min_value: 1` |
| `stg_crm_kol_flags` - `count(*) > 0` | ~501 | `dbt_utils.row_count` with `min_value: 1` |

### 3. Create Custom Singular Tests (Priority 3)

For complex business logic checks, create singular tests in `transforms/tests/staging/`:

**New files**:

- `assert_stg_target_file_stage_has_both_account_types.sql` - validates 2 distinct account types
- `assert_stg_hcp_has_names.sql` - validates name presence logic
- `assert_stg_hcp_specialty_has_values.sql` - validates specialty distinct count (if needed)
- `assert_stg_addresses_has_entities.sql` - validates distinct address_vid (if needed)

Each singular test should return rows that fail validation (empty = pass).

### 4. Verify Intermediate Test Coverage (Priority 4)

**File**: `transforms/models/intermediate/results/_results.yml`
Ensure these tests exist:

- Relationship from `int_primary_affiliations_dbt.hcp_vid` → `stg_hcp.hcp_vid`
- Relationship from `int_primary_affiliations_dbt.hco_vid` → `stg_hco.hco_vid`

Check other intermediate model test files for any staging-level tests that should be moved.

## Validation

After changes:

1. Run `dbt test --select staging` - all staging tests should pass independently
2. Run `dbt test` - full test suite (intermediate tests may still fail on missing models until they're built)
3. Verify staging tests don't reference any `int_*` or mart models

### To-dos

- [x] ~~Move cross-layer relationship tests from staging to intermediate layer test files~~
- [x] ~~Fix expression_is_true tests to use SELECT subqueries for aggregates~~
- [x] ~~Create custom singular tests for complex aggregate business logic validations~~
- [x] ~~Verify intermediate models have proper relationship tests to staging layer~~
- [x] ~~Update dbt_testing_best_practices.mdc with learnings~~