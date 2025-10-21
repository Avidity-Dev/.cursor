<!-- f1ca4ff3-dfe3-4305-b245-43cc45a9678b e66544de-aaad-4285-98cc-b075161967c9 -->

# CI Test for dbt YAML Test Best Practices

## Overview

Create a standalone Python validation script that runs in CI to enforce dbt testing best practices, preventing regression of the issues we just fixed. No pytest wrapper needed - keep it simple and direct.

## Validation Rules

The script will check for:

1. **Unwrapped Aggregates** - Detect bare aggregate functions in `expression_is_true` tests
2. **Missing Arguments Section** - Ensure `expression_is_true` tests use the `arguments` key
3. **Proper Subquery Usage** - Verify aggregates are wrapped in `(SELECT ... FROM ...)`
4. **Macro Usage** - Confirm tests use `{{ ref() }}` or `{{ source() }}` instead of hardcoded table names

## Implementation Details

### File: `transforms/scripts/validate_dbt_tests.py`

Create a new validation script following the pattern of existing scripts:

- `analyze_test_coverage.py` - for structure reference
- `analyze_defense_in_depth.py` - for YAML parsing patterns

**Key Features:**

- Parse all YAML files in `transforms/models/` and `transforms/seeds/`
- Use regex patterns to detect anti-patterns
- Exit with non-zero code if violations found
- Provide clear, actionable error messages with file paths and line numbers

**Anti-Pattern Detection:**

```python
# Pattern 1: Unwrapped aggregates (case-insensitive)
AGGREGATE_FUNCTIONS = [
    r'\bcount\s*\(',
    r'\bsum\s*\(',
    r'\bavg\s*\(',
    r'\bmax\s*\(',
    r'\bmin\s*\(',
]

# Pattern 2: Proper SELECT wrapper
GOOD_PATTERN = r'\(\s*SELECT\s+.*\s+FROM\s+'

# Pattern 3: Macro usage
MACRO_PATTERN = r'\{\{\s*(ref|source)\s*\('
```

**Validation Logic:**

For each `dbt_utils.expression_is_true` test:

1. ✅ Verify `arguments:` key exists
2. ✅ Verify `expression:` is present under `arguments:`
3. ✅ Check if expression contains aggregate function (COUNT, SUM, etc.)
4. ✅ If aggregate found, verify it's wrapped in `(SELECT ... FROM {{ ref() }})` or `{{ source() }}`
5. ✅ Verify macro usage ({{ ref() }} or {{ source() }}) is present
6. ❌ Flag violations with file path, line number, and suggestion

**Output Format:**

```
🔍 Validating dbt test YAML files...

✅ transforms/models/mdm/marts/_mdm_marts.yml
✅ transforms/models/mdm/staging/_staging.yml
✅ transforms/models/mdm/_sources/edw_gold_crm.yml

❌ FAILED: transforms/models/mdm/intermediate/_intermediate.yml

  Line 45: Unwrapped aggregate function detected
    Test: int_hcp_unified_minimum_row_count
    Expression: "count(*) > 10000"

    Fix: Wrap in SELECT subquery with macro:
    expression: "(SELECT COUNT(*) FROM {{ ref('int_hcp_unified') }}) > 10000"

  Line 78: Missing arguments section
    Test: dbt_utils.expression_is_true

    Fix: Add arguments key:
    tests:
      - dbt_utils.expression_is_true:
          arguments:
            expression: "your_expression_here"

============================================================
❌ VALIDATION FAILED: 2 violations found
See: .cursor/rules/dbt/dbt_testing_best_practices.mdc
============================================================

Exit code: 1
```

**Script Structure:**

```python
#!/usr/bin/env python3
"""
Validate dbt test YAML files follow best practices.

Checks:
- No unwrapped aggregates in expression_is_true tests
- Proper use of arguments section
- Use of {{ ref() }} or {{ source() }} macros
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any
import yaml

class ValidationError:
    def __init__(self, file_path, line_num, test_name, error_type, expression, suggestion):
        self.file_path = file_path
        self.line_num = line_num
        self.test_name = test_name
        self.error_type = error_type
        self.expression = expression
        self.suggestion = suggestion

def find_yaml_files(base_path: Path) -> List[Path]:
    """Find all YAML files in models and seeds directories."""
    yaml_files = []
    for pattern in ['**/*.yml', '**/*.yaml']:
        yaml_files.extend(base_path.glob(pattern))
    return sorted(yaml_files)

def validate_expression_is_true_test(test_def: Dict[str, Any], file_path: str) -> List[ValidationError]:
    """Validate a single expression_is_true test."""
    errors = []

    # Check 1: arguments key exists
    if 'arguments' not in test_def:
        errors.append(ValidationError(
            file_path, None, "dbt_utils.expression_is_true",
            "Missing arguments section",
            "", "Add 'arguments:' key with 'expression:' inside"
        ))
        return errors

    # Check 2: expression exists in arguments
    if 'expression' not in test_def['arguments']:
        errors.append(ValidationError(
            file_path, None, test_def.get('config', {}).get('alias', 'unknown'),
            "Missing expression in arguments",
            "", "Add 'expression:' under 'arguments:'"
        ))
        return errors

    expression = test_def['arguments']['expression']
    test_name = test_def.get('config', {}).get('alias', 'expression_is_true_test')

    # Check 3: Unwrapped aggregates
    for agg_pattern in AGGREGATE_FUNCTIONS:
        if re.search(agg_pattern, expression, re.IGNORECASE):
            # Check if it's wrapped in SELECT
            if not re.search(GOOD_PATTERN, expression, re.IGNORECASE):
                errors.append(ValidationError(
                    file_path, None, test_name,
                    "Unwrapped aggregate function",
                    expression,
                    "Wrap in SELECT subquery: (SELECT COUNT(*) FROM {{ ref('model') }}) > threshold"
                ))
                break

    # Check 4: Macro usage (if SELECT is present)
    if re.search(r'\bSELECT\b', expression, re.IGNORECASE):
        if not re.search(MACRO_PATTERN, expression):
            errors.append(ValidationError(
                file_path, None, test_name,
                "Missing {{ ref() }} or {{ source() }} macro",
                expression,
                "Use {{ ref('model_name') }} or {{ source('schema', 'table') }}"
            ))

    return errors

def validate_yaml_file(file_path: Path) -> List[ValidationError]:
    """Validate all tests in a single YAML file."""
    errors = []

    with open(file_path) as f:
        data = yaml.safe_load(f)

    if not data:
        return errors

    # Walk through YAML structure looking for expression_is_true tests
    # Handle both model tests and source tests
    for section in ['models', 'sources', 'seeds']:
        if section not in data:
            continue

        for item in data[section]:
            # Model-level tests
            if 'tests' in item:
                for test in item['tests']:
                    if isinstance(test, dict) and 'dbt_utils.expression_is_true' in test:
                        errors.extend(validate_expression_is_true_test(
                            test['dbt_utils.expression_is_true'],
                            str(file_path)
                        ))

            # Column-level tests
            if 'columns' in item:
                for col in item['columns']:
                    if 'tests' in col:
                        for test in col['tests']:
                            if isinstance(test, dict) and 'dbt_utils.expression_is_true' in test:
                                errors.extend(validate_expression_is_true_test(
                                    test['dbt_utils.expression_is_true'],
                                    str(file_path)
                                ))

            # Source tables
            if 'tables' in item:
                for table in item['tables']:
                    if 'tests' in table:
                        for test in table['tests']:
                            if isinstance(test, dict) and 'dbt_utils.expression_is_true' in test:
                                errors.extend(validate_expression_is_true_test(
                                    test['dbt_utils.expression_is_true'],
                                    str(file_path)
                                ))

    return errors

def main():
    """Main validation entry point."""
    print("🔍 Validating dbt test YAML files...\n")

    # Find all YAML files
    transforms_path = Path(__file__).parent.parent
    yaml_files = find_yaml_files(transforms_path / 'models')
    yaml_files.extend(find_yaml_files(transforms_path / 'seeds'))

    all_errors = []
    passed_files = []

    for yaml_file in yaml_files:
        errors = validate_yaml_file(yaml_file)
        if errors:
            all_errors.extend(errors)
        else:
            passed_files.append(yaml_file)

    # Print results
    for f in passed_files:
        print(f"✅ {f.relative_to(transforms_path.parent)}")

    if all_errors:
        print(f"\n{'='*60}")
        print(f"❌ VALIDATION FAILED: {len(all_errors)} violation(s) found")
        print(f"{'='*60}\n")

        # Group errors by file
        errors_by_file = {}
        for err in all_errors:
            if err.file_path not in errors_by_file:
                errors_by_file[err.file_path] = []
            errors_by_file[err.file_path].append(err)

        for file_path, errors in errors_by_file.items():
            print(f"\n❌ FAILED: {file_path}\n")
            for err in errors:
                print(f"  {err.error_type}")
                print(f"    Test: {err.test_name}")
                if err.expression:
                    print(f"    Expression: {err.expression[:80]}...")
                print(f"    Fix: {err.suggestion}\n")

        print(f"{'='*60}")
        print("See: .cursor/rules/dbt/dbt_testing_best_practices.mdc")
        print(f"{'='*60}")
        sys.exit(1)
    else:
        print(f"\n{'='*60}")
        print(f"✅ ALL VALIDATIONS PASSED")
        print(f"{'='*60}")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### File: `.github/workflows/dbt-tests.yml` (NEW)

Create a GitHub Actions workflow for dbt test validation:

```yaml
name: dbt Test Validation

on:
  pull_request:
    paths:
      - "transforms/models/**/*.yml"
      - "transforms/models/**/*.yaml"
      - "transforms/seeds/**/*.yml"
  push:
    branches:
      - main
      - develop

jobs:
  validate-dbt-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install pyyaml

      - name: Validate dbt test YAML files
        run: |
          python transforms/scripts/validate_dbt_tests.py
```

### Update: `transforms/scripts/README.md`

Add documentation for the new validation script:

````markdown
### `validate_dbt_tests.py`

Validates that all dbt test YAML files follow best practices from `.cursor/rules/dbt/dbt_testing_best_practices.mdc`.

**Checks:**

- No unwrapped aggregate functions in expression_is_true tests
- All expression_is_true tests use proper `arguments:` section
- Aggregate functions wrapped in SELECT subqueries
- Use of `{{ ref() }}` or `{{ source() }}` macros

**Usage:**

```bash
# From transforms directory
python scripts/validate_dbt_tests.py

# From project root
python transforms/scripts/validate_dbt_tests.py

# From CI (exits with non-zero on violations)
python transforms/scripts/validate_dbt_tests.py || exit 1
```
````

**Exit Codes:**

- 0: All validations passed
- 1: Violations found

**Example Output:**

```
🔍 Validating dbt test YAML files...

✅ transforms/models/mdm/marts/_mdm_marts.yml
❌ FAILED: transforms/models/mdm/intermediate/_intermediate.yml

  Unwrapped aggregate function
    Test: int_hcp_unified_minimum_row_count
    Expression: "count(*) > 10000"
    Fix: Wrap in SELECT subquery: (SELECT COUNT(*) FROM {{ ref('model') }}) > threshold

============================================================
❌ VALIDATION FAILED: 1 violation found
See: .cursor/rules/dbt/dbt_testing_best_practices.mdc
============================================================
```

````

## Files to Create

1. `transforms/scripts/validate_dbt_tests.py` - Standalone validation script (~250 lines)
2. `.github/workflows/dbt-tests.yml` - CI workflow (~30 lines)

## Files to Modify

1. `transforms/scripts/README.md` - Add documentation for new script

## Testing Strategy

### Local Testing

```bash
# Test the validator
python transforms/scripts/validate_dbt_tests.py

# Should pass (all tests are good)
echo $?  # Should output 0

# Test with intentional violation
# 1. Edit a YAML file: change "expression: \"(SELECT COUNT(*)" to "expression: \"count(*)"
# 2. Run validator - should fail with exit code 1
# 3. Revert the change
````

### CI Testing

- Runs automatically on PRs that modify YAML files
- Blocks merge if violations detected
- Fast feedback loop (< 10 seconds)
- No external dependencies (Snowflake, database, etc.)

## Benefits

✅ **Simple & Direct** - One script, one purpose, easy to understand

✅ **Prevents Regression** - Catches issues before they reach main branch

✅ **Educational** - Clear error messages teach best practices

✅ **Fast Feedback** - Runs in seconds, no database connection needed

✅ **Zero Overhead** - No test framework, no subprocess calls

✅ **Consistent Quality** - Enforces standards across all contributors

✅ **Documentation-Driven** - References the best practices guide

## Implementation Status

✅ **COMPLETED** - All components implemented and tested

### Files Created

1. `transforms/scripts/validate_dbt_tests.py` - Standalone validation script (~290 lines)
2. `.github/workflows/dbt-tests.yml` - CI workflow (~30 lines)

### Files Modified

1. `transforms/scripts/README.md` - Added documentation for new script

### Testing Results

- ✅ Script successfully identifies 16 existing violations across multiple YAML files
- ✅ Provides clear error messages with file paths and suggested fixes
- ✅ Exits with appropriate codes (0 for success, 1 for violations)
- ✅ Fast execution (< 10 seconds)

### Benefits Achieved

- **Prevents Regression**: Catches issues before they reach main branch
- **Educational**: Clear error messages teach best practices
- **Fast Feedback**: Runs in seconds, no database connection needed
- **Zero Overhead**: No test framework complexity
- **Consistent Quality**: Enforces standards across all contributors

## Next Steps

The validation script has identified 16 violations that need to be fixed in the dbt YAML test files. The violations include:

- Unwrapped aggregate functions (e.g., `count(*) > 1000` instead of `(SELECT COUNT(*) FROM {{ ref('model') }}) > 1000`)
- Missing `{{ ref() }}` or `{{ source() }}` macros in SELECT subqueries

## Future Enhancements (Optional)

- Add `--fix` flag to automatically correct violations
- Check for lowercase column names consistency
- Validate test severity levels (ERROR vs WARN usage)
- Ensure descriptive test aliases are used
- Check for proper use of `config:` blocks
- Add `--verbose` flag for detailed output
