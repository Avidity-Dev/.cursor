<!-- 5f4817dc-101c-447d-998b-735149755e93 250e4bcf-6617-4619-8c63-6004b5abd780 -->
# Safe Testing Strategy for exact_address_match Change (Using dbt-audit-helper)

## Goal

Test the impact of changing `exact_address_match` from line1-only to complete address matching by using `dbt-audit-helper` to compare production tables against test versions.

## Why dbt-audit-helper?

`dbt-audit-helper` is purpose-built for this exact scenario:

- ✅ Automatically compares row counts, column values, and aggregations
- ✅ Generates side-by-side comparison reports
- ✅ Handles NULL differences gracefully
- ✅ Much cleaner than manual SQL comparison queries
- ✅ Industry standard tool for refactoring validation

## Strategy: Use dbt Schema Override + audit-helper

We'll use dbt's `schema` config to build the modified models into a separate schema (e.g., `mdm_test` instead of `mdm`), then use audit-helper to compare them. Production tables remain untouched.

## Implementation Steps

### 1. Install dbt-audit-helper

**File**: `transforms/packages.yml`

Add audit-helper package:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: dbt-labs/codegen
    version: 0.13.1
  - package: dbt-labs/audit_helper
    version: 0.9.0  # Latest stable version
```

Then install:

```bash
cd transforms
dbt deps
```

### 2. Create a dbt Variables Configuration

**File**: `transforms/dbt_project.yml` (add to existing vars section)

Add a testing flag:

```yaml
vars:
  test_exact_address_match: false  # Set to true when testing
```

### 3. Add Schema Override to Affected Models

For each model that needs testing, add conditional schema config:

**Files to modify**:

- `transforms/models/mdm/intermediate/enriched/mdm_affiliations_enriched.sql`
- `transforms/models/mdm/intermediate/enriched/mdm_affiliations_extension.sql`
- `transforms/models/mdm/intermediate/candidates/mdm_match_candidates.sql`
- `transforms/models/mdm/intermediate/aggregated/mdm_hcp_match_stats.sql`

**Pattern** (add to config block of each file):

```sql
{{
  config(
    schema='mdm_test' if var('test_exact_address_match', false) else 'mdm',
    tags=['intermediate', 'affiliations', 'enriched'],
    materialized='table',
    unique_key=['hcp_vid', 'hco_vid']
  )
}}
```

### 4. Make the Logic Change

**File**: `transforms/models/mdm/intermediate/enriched/mdm_affiliations_enriched.sql`

Replace lines 146-149 with:

```sql
-- Exact address match (line1, city, state, postal)
{{ complete_address_match(
    'hcp.hcp_address_line_1', 'hcp.hcp_city', 'hcp.hcp_state', 'hcp.hcp_postal_code',
    'hco.hco_address_line_1', 'hco.hco_city', 'hco.hco_state', 'hco.hco_postal_code'
) }} as exact_address_match,
```

Update documentation (line 34):

```
- Exact address match compares complete address (line1, city, state, postal)
```

### 5. Update Schema Documentation

**File**: `transforms/models/mdm/intermediate/enriched/_enriched.yml`

Update descriptions for `exact_address_match` field (appears in both mdm_affiliations_enriched and mdm_affiliations_extension):

Change from:

```yaml
description: Flag indicating exact address line 1 match (0/1)
```

To:

```yaml
description: Flag indicating complete address match (line1, city, state, postal) (0/1)
```

### 6. Build Test Tables

Run dbt with the test flag enabled:

```bash
cd transforms
dbt run --vars '{test_exact_address_match: true}' --select mdm_affiliations_enriched+
```

This will:

- Build `mdm_test.mdm_affiliations_enriched` (new logic)
- Build `mdm_test.mdm_affiliations_extension` (pulls from test enriched)
- Build `mdm_test.mdm_match_candidates` (pulls from test extension)
- Build `mdm_test.mdm_hcp_match_stats` (pulls from test extension)

Production tables in `mdm.*` remain unchanged.

### 7. Create Audit Helper Comparison Models

**File**: `transforms/analysis/audit_affiliations_enriched.sql` (new file)

```sql
{% set old_relation = ref('mdm_affiliations_enriched') %} -- Production
{% set new_relation = adapter.get_relation(
    database=target.database,
    schema='mdm_test',
    identifier='mdm_affiliations_enriched'
) %} -- Test

{{ audit_helper.compare_relations(
    a_relation=old_relation,
    b_relation=new_relation,
    primary_key="hcp_vid || '-' || hco_vid",
    exclude_columns=['_dbt_loaded_at']
) }}
```

**File**: `transforms/analysis/audit_match_candidates.sql` (new file)

```sql
{% set old_relation = ref('mdm_match_candidates') %} -- Production
{% set new_relation = adapter.get_relation(
    database=target.database,
    schema='mdm_test',
    identifier='mdm_match_candidates'
) %} -- Test

{{ audit_helper.compare_relations(
    a_relation=old_relation,
    b_relation=new_relation,
    primary_key="hcp_vid || '-' || hco_vid",
    exclude_columns=['_dbt_loaded_at']
) }}
```

**File**: `transforms/analysis/audit_hcp_match_stats.sql` (new file)

```sql
{% set old_relation = ref('mdm_hcp_match_stats') %} -- Production
{% set new_relation = adapter.get_relation(
    database=target.database,
    schema='mdm_test',
    identifier='mdm_hcp_match_stats'
) %} -- Test

{{ audit_helper.compare_relations(
    a_relation=old_relation,
    b_relation=new_relation,
    primary_key='hcp_vid',
    exclude_columns=['_dbt_loaded_at']
) }}
```

**File**: `transforms/analysis/audit_exact_address_detail.sql` (new file)

Detailed comparison focused on exact_address_match changes:

```sql
{% set old_relation = ref('mdm_affiliations_enriched') %}
{% set new_relation = adapter.get_relation(
    database=target.database,
    schema='mdm_test',
    identifier='mdm_affiliations_enriched'
) %}

{{ audit_helper.compare_column_values(
    a_relation=old_relation,
    b_relation=new_relation,
    primary_key="hcp_vid || '-' || hco_vid",
    column_to_compare='exact_address_match'
) }}
```

**File**: `transforms/analysis/exact_address_match_changes.sql` (new file)

For even more detail on what changed:

```sql
-- Show examples of affiliations where exact_address_match changed
with prod as (
    select
        hcp_vid,
        hco_vid,
        exact_address_match as prod_match,
        hcp_address_line_1,
        hcp_city,
        hcp_state,
        hcp_postal_code,
        hco_address_line_1,
        hco_city,
        hco_state,
        hco_postal_code
    from {{ ref('mdm_affiliations_enriched') }}
),

test as (
    select
        hcp_vid,
        hco_vid,
        exact_address_match as test_match
    from {{ adapter.get_relation(
        database=target.database,
        schema='mdm_test',
        identifier='mdm_affiliations_enriched'
    ) }}
),

changes as (
    select
        p.*,
        t.test_match,
        case
            when p.prod_match = 1 and t.test_match = 0 then 'LOST_MATCH'
            when p.prod_match = 0 and t.test_match = 1 then 'GAINED_MATCH'
        end as change_type
    from prod p
    inner join test t using (hcp_vid, hco_vid)
    where p.prod_match != t.test_match
)

select
    change_type,
    count(*) as count,
    -- Show 5 examples per change type
    listagg(
        concat(
            'HCP:', hcp_vid, ' HCO:', hco_vid,
            ' | HCP: ', hcp_city, ', ', hcp_state, ' ', hcp_postal_code,
            ' | HCO: ', hco_city, ', ', hco_state, ' ', hco_postal_code
        ), '\n'
    ) within group (order by hcp_vid)
    over (partition by change_type rows between unbounded preceding and 4 following) as examples
from changes
group by change_type
order by change_type
```

### 8. Run Audit Comparisons

```bash
# Compare overall relations (row counts, column counts, mismatches)
dbt run --select audit_affiliations_enriched
dbt run --select audit_match_candidates
dbt run --select audit_hcp_match_stats

# Detailed comparison of exact_address_match column
dbt run --select audit_exact_address_detail

# Custom change analysis
dbt run --select exact_address_match_changes
```

Output will show:

- Total rows in each table
- Rows that exist in production but not test
- Rows that exist in test but not production
- Rows with different values
- Summary of mismatches per column

### 9. Review Results

Audit helper will create tables in your target schema with comparison results:

```sql
-- View audit results in Snowflake
SELECT * FROM <target_schema>.audit_affiliations_enriched;
SELECT * FROM <target_schema>.audit_match_candidates;
SELECT * FROM <target_schema>.audit_hcp_match_stats;
SELECT * FROM <target_schema>.audit_exact_address_detail;
SELECT * FROM <target_schema>.exact_address_match_changes;
```

Look for:

- **in_a_not_in_b**: Rows that disappeared (should be 0)
- **in_b_not_in_a**: New rows that appeared (should be 0)
- **count_rows_different**: Rows where at least one column differs
- **percent_of_total**: What % of rows changed

### 10. Cleanup After Testing

Once satisfied with results:

**Option A**: Keep the changes, remove schema override

- Remove `schema` config overrides from all models
- The next `dbt run` will update production tables with new logic

**Option B**: Revert the changes

- Revert the `exact_address_match` implementation
- Drop test tables: `DROP SCHEMA mdm_test CASCADE;`

## Alternative: Use dbt Clone Feature

If your Snowflake edition supports zero-copy cloning, you can also:

```sql
-- Clone production table
CREATE TABLE mdm_test.mdm_affiliations_enriched CLONE mdm.mdm_affiliations_enriched;

-- Then build just the test version
dbt run --vars '{test_exact_address_match: true}' --select mdm_affiliations_enriched
```

## Summary

**Advantages of this approach**:

- ✅ Production tables remain untouched
- ✅ Side-by-side comparison in same Snowflake instance
- ✅ Can test full downstream impact
- ✅ Easy to revert if results are unexpected
- ✅ Can validate in CI before merging to main branch

**Files to create**: 2 analysis queries

**Files to modify**: 4 SQL models (add schema config), 1 dbt_project.yml (add var)

**Next steps after reviewing this plan**:

1. Should I proceed with this implementation?
2. Do you want to use the schema override approach or have a different testing strategy in mind?