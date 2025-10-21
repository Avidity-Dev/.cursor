# Add Parent HCO Names and Types

## Overview

The HCO marts model currently exposes parent VIDs but not their names and types. This plan adds 4 new fields by implementing self-joins directly in the mart layer to look up parent HCO attributes.

## Implementation Strategy

### Simplified Mart-Only Approach

Instead of propagating fields through all layers, we'll implement the self-joins directly in the mart model. This is simpler and achieves the same end result while keeping the upstream models clean.

The mart will self-join with `mdm_hco_enriched` to look up parent attributes:

- `parent_hco_name` and `parent_hco_type` from immediate parent VID
- `avid_top_parent_name` and `avid_top_parent_type` from top parent VID

## Implementation Steps

### 1. Update Marts Layer - HCO Dimension

**File**: `transforms/models/mdm/marts/hco.sql`

Replace the current CTE structure with a new approach that includes self-joins:

```sql
with enriched_hcos as (
    select * from {{ ref('mdm_hco_enriched') }}
),

-- Self-join for immediate parent attributes
immediate_parents as (
    select
        hco_vid as parent_vid,
        hco_name as parent_name,
        hco_type as parent_type
    from enriched_hcos
),

-- Self-join for top parent attributes
top_parents as (
    select
        hco_vid as top_parent_vid,
        hco_name as top_parent_name,
        hco_type as top_parent_type
    from enriched_hcos
)

select
    -- ============================================================
    -- IDENTIFIERS
    -- ============================================================
    cast(hcos.hco_vid as number(19,0)) as vid,  -- Enforce precision contract
    hcos.npi_num,

    -- ============================================================
    -- ORGANIZATION INFORMATION
    -- ============================================================
    hcos.hco_name,
    hcos.hco_type,
    hcos.hco_status,

    -- ============================================================
    -- PRIMARY ADDRESS
    -- ============================================================
    hcos.address_line_1,
    hcos.address_line_2,
    hcos.city,
    hcos.state,
    hcos.postal_code,
    hcos.vn_country as country,

    -- ============================================================
    -- HIERARCHY
    -- ============================================================
    cast(hcos.parent_hco_vid as number(19,0)) as parent_hco_vid,  -- Enforce precision contract
    ip.parent_name as parent_hco_name,  -- Addresses TODO line 81
    ip.parent_type as parent_hco_type,  -- Addresses TODO line 82
    hcos.avid_top_parent,
    tp.top_parent_name as avid_top_parent_name,  -- Addresses TODO line 84
    tp.top_parent_type as avid_top_parent_type,  -- Addresses TODO line 85

    -- ============================================================
    -- PROGRAM FLAGS
    -- ============================================================
    hcos.is_340b_eligible,
    hcos.in_network,
    hcos.is_dmd_coe,
    hcos.is_mda_center,
    hcos.is_ppmd_account,

from enriched_hcos hcos
left join immediate_parents ip
    on hcos.parent_hco_vid = ip.parent_vid
left join top_parents tp
    on hcos.avid_top_parent = tp.top_parent_vid

-- Defense-in-depth: VID is primary key and must not be null
-- While staging enforces this via SQL filter + dbt test, marts should
-- be resilient to test configuration errors or skipped test runs
where hcos.hco_vid is not null
```

## Key Design Decisions

1. **Self-joins at mart layer**: Simpler than propagating through all layers, achieves same result
2. **LEFT JOINs preserve all records**: Parent lookups won't filter out orphaned HCOs
3. **Consistent naming**: Uses `avid_top_parent_name` and `avid_top_parent_type` to match existing field naming
4. **Defense-in-depth filtering**: Maintains the existing WHERE clause for data quality

## Testing Considerations

After implementation, verify:

- Records with parents show names/types correctly
- Records without parents have NULL parent attributes (not filtered out)
- OpenData HCOs have NULL top parent fields (since they don't have top parents)
- Network HCOs have populated top parent fields when available
- Join performance is acceptable (should be fast since it's a self-join on the same table)

## Files Modified

1. `transforms/models/mdm/marts/hco.sql` - Add self-joins and expose 4 new parent fields, remove TODO comments

### To-dos

- [ ] Update marts/hco.sql to add self-joins for parent names/types and expose the 4 new fields, removing TODO comments