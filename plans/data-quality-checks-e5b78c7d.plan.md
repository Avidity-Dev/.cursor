<!-- e5b78c7d-ea03-42d7-aa0a-0e11a2c3b024 88b25511-90b6-4d2c-b518-93be0caa90a6 -->
# Data Quality Checks and Enhanced Error Handling

## Phase 1: Quick Fixes (Immediate)

### 1.1 Add Validation to Critical Staging Models

**Target files:**

- `transforms/models/staging/stg_addresses.sql`
- `transforms/models/staging/stg_hco.sql`
- `transforms/models/staging/stg_vn_hco.sql`

**Add WHERE clause filters to catch obvious bad data:**

```sql
-- In stg_addresses.sql, add at end:
where 1=1
  -- Reject records with string values in numeric fields
  and not regexp_like(latitude__v, '[a-zA-Z]')  
  and not regexp_like(longitude__v, '[a-zA-Z]')
  -- Reject if VID contains non-numeric characters
  and try_cast(entity_vid__v as number) is not null
```



```sql
-- In stg_hco.sql and stg_vn_hco.sql, add at end:
where 1=1
  -- Reject if NPI contains letters (except for NULL/empty)
  and (npi_num__v is null or npi_num__v = '' or not regexp_like(npi_num__v, '[a-zA-Z]'))
  -- Reject if VID is not numeric
  and try_cast(vid__v as number) is not null
```

### 1.2 Enhance safe_coordinate_cast Macro with Logging

**File:** `transforms/macros/core/safe_conversions.sql`

**Modify `safe_coordinate_cast` to detect non-numeric values:**

```sql
{% macro safe_coordinate_cast(column_name, coord_type='latitude', default=none) -%}
  case
    -- Check if contains letters (data quality issue)
    when regexp_like({{ column_name }}, '[a-zA-Z]') then null
    -- Normal conversion
    {% if coord_type == 'latitude' %}
      else {{ safe_decimal(column_name, precision=9, scale=6, default=default if default is not none else 'null') }}
    {% else %}
      else {{ safe_decimal(column_name, precision=10, scale=6, default=default if default is not none else 'null') }}
    {% endif %}
  end
{%- endmacro %}
```

## Phase 2: Comprehensive Data Quality Framework (Later)

### 2.1 Create New Validation Macros

**New file:** `transforms/macros/data_quality/validation.sql`

```sql
-- validate_numeric_field: Check if field can be safely cast to number
{% macro validate_numeric_field(column, allow_null=true) -%}
  {% if allow_null %}
    ({{ column }} is null or {{ column }} = '' or try_cast({{ column }} as number) is not null)
  {% else %}
    ({{ column }} is not null and {{ column }} != '' and try_cast({{ column }} as number) is not null)
  {% endif %}
{%- endmacro %}

-- validate_vid: Check if Veeva ID is valid (numeric, non-null)
{% macro validate_vid(column) -%}
  ({{ column }} is not null and try_cast({{ column }} as number) is not null)
{%- endmacro %}

-- validate_coordinate: Check if lat/lon is valid range and numeric
{% macro validate_coordinate(column, coord_type='latitude') -%}
  {% if coord_type == 'latitude' %}
    ({{ column }} is null or (try_cast({{ column }} as number) between -90 and 90))
  {% else %}
    ({{ column }} is null or (try_cast({{ column }} as number) between -180 and 180))
  {% endif %}
{%- endmacro %}

-- detect_data_quality_issues: Return flag for suspicious values
{% macro detect_data_quality_issues(column, expected_type='numeric') -%}
  case
    when {{ column }} is null then 'null_value'
    when trim({{ column }}) = '' then 'empty_string'
    {% if expected_type == 'numeric' %}
      when regexp_like({{ column }}, '[a-zA-Z]') then 'contains_letters'
      when try_cast({{ column }} as number) is null then 'not_numeric'
    {% endif %}
    else 'valid'
  end
{%- endmacro %}
```

### 2.2 Create Data Quality Logging Models

**New file:** `transforms/models/data_quality/dq_staging_issues.sql`

```sql
-- Captures data quality issues from all staging models for monitoring
with source_issues as (
  select 
    'stg_addresses' as model_name,
    'latitude__v' as field_name,
    latitude__v as field_value,
    entity_vid__v as record_id,
    {{ detect_data_quality_issues('latitude__v', 'numeric') }} as issue_type
  from {{ source('edw_ingest_veeva', 'od__address') }}
  where {{ detect_data_quality_issues('latitude__v', 'numeric') }} != 'valid'
  
  union all
  
  select 
    'stg_addresses' as model_name,
    'longitude__v' as field_name,
    longitude__v as field_value,
    entity_vid__v as record_id,
    {{ detect_data_quality_issues('longitude__v', 'numeric') }} as issue_type
  from {{ source('edw_ingest_veeva', 'od__address') }}
  where {{ detect_data_quality_issues('longitude__v', 'numeric') }} != 'valid'
  
  union all
  
  select 
    'stg_hco' as model_name,
    'npi_num__v' as field_name,
    npi_num__v as field_value,
    vid__v as record_id,
    {{ detect_data_quality_issues('npi_num__v', 'numeric') }} as issue_type
  from {{ source('edw_ingest_veeva', 'od__hco') }}
  where npi_num__v is not null 
    and {{ detect_data_quality_issues('npi_num__v', 'numeric') }} != 'valid'
)

select 
  *,
  current_timestamp() as detected_at
from source_issues
```

### 2.3 Create Quarantine Tables

**New file:** `transforms/models/data_quality/quarantine_addresses.sql`

```sql
-- Records from od__address that fail validation - excluded from staging
select
  *,
  case
    when not {{ validate_vid('entity_vid__v') }} then 'invalid_vid'
    when regexp_like(latitude__v, '[a-zA-Z]') then 'invalid_latitude'
    when regexp_like(longitude__v, '[a-zA-Z]') then 'invalid_longitude'
    when not {{ validate_coordinate('latitude__v', 'latitude') }} then 'lat_out_of_range'
    when not {{ validate_coordinate('longitude__v', 'longitude') }} then 'lon_out_of_range'
  end as rejection_reason,
  current_timestamp() as quarantined_at
from {{ source('edw_ingest_veeva', 'od__address') }}
where not (
  {{ validate_vid('entity_vid__v') }}
  and {{ validate_coordinate('latitude__v', 'latitude') }}
  and {{ validate_coordinate('longitude__v', 'longitude') }}
  and not regexp_like(coalesce(latitude__v, ''), '[a-zA-Z]')
  and not regexp_like(coalesce(longitude__v, ''), '[a-zA-Z]')
)
```

**Similar files needed:**

- `quarantine_hco.sql`
- `quarantine_hcp.sql`

### 2.4 Create dbt Tests for Data Quality

**New file:** `transforms/models/data_quality/_data_quality.yml`

```yaml
version: 2

models:
  - name: dq_staging_issues
    description: "Data quality issues detected in staging layer"
    tests:
      - dbt_utils.expression_is_true:
          expression: "count(*) < 100"
          name: staging_dq_issues_under_threshold
    
  - name: quarantine_addresses
    description: "Address records rejected due to data quality issues"
    
  - name: quarantine_hco
    description: "HCO records rejected due to data quality issues"
```

### 2.5 Enhanced Macro Error Handling

**Update:** `transforms/macros/core/safe_conversions.sql`

Add optional logging parameter to all safe_* macros:

```sql
{% macro safe_cast(column, target_type, default=none, precision=18, scale=5, log_failures=false) -%}
  {% if log_failures %}
    -- Wrap in CTE that logs failures to monitoring table
    case
      when try_cast(nullif(trim({{ column }}), '') as {{ target_type }}) is null 
        and {{ column }} is not null 
        and trim({{ column }}) != ''
      then (
        -- Log the failure (pseudo-code, implement via stored proc or separate process)
        -- insert into dq_conversion_failures (column_name, value, target_type, timestamp)
        {{ default if default is not none else 'null' }}
      )
      else coalesce(try_cast(nullif(trim({{ column }}), '') as {{ target_type }}), {{ default if default is not none else 'null' }})
    end
  {% else %}
    -- Original implementation
    ...existing code...
  {% endif %}
{%- endmacro %}
```

## Implementation Strategy Summary

**Fail-Fast (Phase 1):**

- WHERE clause filters in staging models reject bad records immediately
- Pipeline stops if critical validations fail

**Log Warnings (Phase 2):**

- `dq_staging_issues` model captures all issues
- Can be monitored via dashboards/alerts
- Pipeline continues, issues logged for review

**Quarantine (Phase 2):**

- Separate quarantine models store rejected records
- Allows data team to investigate root causes
- Records can be manually corrected and reprocessed

## Files to Create/Modify

**Phase 1 (Quick Fixes):**

- Modify: `stg_addresses.sql`, `stg_hco.sql`, `stg_vn_hco.sql`
- Modify: `safe_conversions.sql` (safe_coordinate_cast)

**Phase 2 (Comprehensive):**

- Create: `macros/data_quality/validation.sql`
- Create: `models/data_quality/dq_staging_issues.sql`
- Create: `models/data_quality/quarantine_addresses.sql`
- Create: `models/data_quality/quarantine_hco.sql`
- Create: `models/data_quality/quarantine_hcp.sql`
- Create: `models/data_quality/_data_quality.yml`
- Modify: `safe_conversions.sql` (add log_failures parameter)
- Create: `dbt_project.yml` (add data_quality schema config)

### To-dos

- [ ] Add WHERE clause validation filters to stg_addresses.sql, stg_hco.sql, stg_vn_hco.sql to reject records with letters in numeric fields
- [ ] Enhance safe_coordinate_cast macro to detect and handle non-numeric values (letters) with regexp_like check
- [ ] Create macros/data_quality/validation.sql with validate_numeric_field, validate_vid, validate_coordinate, detect_data_quality_issues macros
- [ ] Create models/data_quality/dq_staging_issues.sql to capture and log all data quality issues from staging models
- [ ] Create quarantine models (quarantine_addresses.sql, quarantine_hco.sql, quarantine_hcp.sql) to isolate rejected records
- [ ] Create models/data_quality/_data_quality.yml with dbt tests to monitor data quality thresholds
- [ ] Add optional log_failures parameter to safe_cast and related macros in safe_conversions.sql for enhanced error tracking
- [ ] Update dbt_project.yml to configure data_quality schema and materialization settings