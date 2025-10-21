#!/usr/bin/env python3
"""
Test script to validate Claude Code import strategies for Cursor rules.

This script helps verify that .mdc files can be properly imported and used
in CLAUDE.md files for Claude Code.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def parse_mdc_file(filepath: Path) -> Dict:
    """Parse an .mdc file and extract its frontmatter and content."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Check for YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
            except yaml.YAMLError as e:
                return {'error': f'YAML parse error: {e}', 'filepath': str(filepath)}
        else:
            frontmatter = {}
            body = content
    else:
        frontmatter = {}
        body = content

    return {
        'filepath': str(filepath),
        'frontmatter': frontmatter,
        'body': body,
        'lines': len(body.split('\n'))
    }


def find_imports_in_file(filepath: Path) -> List[str]:
    """Find all @import statements in a file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern to match @imports (not in code blocks)
    # Simple pattern - could be enhanced to skip code blocks
    import_pattern = r'^@([/~][\S]+\.mdc?)$'
    imports = re.findall(import_pattern, content, re.MULTILINE)

    return imports


def resolve_import_path(import_path: str, base_dir: Path) -> Optional[Path]:
    """Resolve an import path to an actual file path."""
    # Handle home directory expansion
    if import_path.startswith('~'):
        import_path = os.path.expanduser(import_path)

    # Handle absolute paths
    if import_path.startswith('/'):
        return Path(import_path) if Path(import_path).exists() else None

    # Handle relative paths
    resolved = base_dir / import_path
    return resolved if resolved.exists() else None


def test_import_patterns():
    """Test various import patterns and report results."""
    test_files = [
        'test-claude-imports.md',
        'CLAUDE-test-imports.md'
    ]

    cursor_rules_dir = Path('/Users/michaelhood/git/.cursor/rules')
    project_dir = Path('/Users/michaelhood/git/mastermind/worktrees/matching')

    results = {
        'total_rules': 0,
        'test_files': [],
        'import_patterns': {
            'absolute': [],
            'relative': [],
            'home': [],
            'wildcard': []
        },
        'mdc_files': [],
        'errors': []
    }

    # Count total cursor rules
    if cursor_rules_dir.exists():
        results['total_rules'] = len(list(cursor_rules_dir.rglob('*.mdc')))

    # Analyze test files
    for test_file in test_files:
        test_path = project_dir / test_file
        if test_path.exists():
            imports = find_imports_in_file(test_path)
            results['test_files'].append({
                'file': test_file,
                'imports_found': len(imports),
                'imports': imports
            })

            # Categorize import patterns
            for imp in imports:
                if imp.startswith('/'):
                    results['import_patterns']['absolute'].append(imp)
                elif imp.startswith('~'):
                    results['import_patterns']['home'].append(imp)
                elif '*' in imp:
                    results['import_patterns']['wildcard'].append(imp)
                else:
                    results['import_patterns']['relative'].append(imp)

    # Sample and analyze a few .mdc files
    sample_mdcs = [
        cursor_rules_dir / 'python' / 'code_style.mdc',
        cursor_rules_dir / 'python' / 'testing.mdc',
        cursor_rules_dir / 'general' / 'documentation.mdc',
        cursor_rules_dir / 'general' / 'data_engineering.mdc'
    ]

    for mdc_path in sample_mdcs:
        if mdc_path.exists():
            mdc_data = parse_mdc_file(mdc_path)
            results['mdc_files'].append(mdc_data)

    return results


def generate_test_report(results: Dict) -> str:
    """Generate a markdown report of test results."""
    report = []
    report.append("# Claude Code Import Test Results\n")

    report.append(f"## Summary")
    report.append(f"- Total Cursor rules available: {results['total_rules']}")
    report.append(f"- Test files analyzed: {len(results['test_files'])}")
    report.append(f"- MDC files sampled: {len(results['mdc_files'])}\n")

    report.append("## Import Pattern Analysis")
    for pattern_type, imports in results['import_patterns'].items():
        report.append(f"\n### {pattern_type.title()} Imports")
        if imports:
            for imp in imports[:5]:  # Show first 5 examples
                report.append(f"- `@{imp}`")
        else:
            report.append("- None found")

    report.append("\n## MDC File Structure")
    report.append("Sample .mdc files analyzed:")
    for mdc in results['mdc_files']:
        if 'error' not in mdc:
            fm = mdc['frontmatter']
            report.append(f"\n### {Path(mdc['filepath']).name}")
            report.append(f"- Description: {fm.get('description', 'N/A')}")
            report.append(f"- Globs: {fm.get('globs', 'N/A')}")
            report.append(f"- Always Apply: {fm.get('alwaysApply', False)}")
            report.append(f"- Content Lines: {mdc['lines']}")

    report.append("\n## Testing Recommendations")
    report.append("\n### Manual Testing Steps")
    report.append("1. **Start new Claude Code session** in this project")
    report.append("2. **Rename test file** to CLAUDE.md: `mv CLAUDE-test-imports.md CLAUDE.md`")
    report.append("3. **Ask Claude Code** to read @/Users/michaelhood/git/.cursor/rules/python/code_style.mdc")
    report.append("4. **Verify content** by asking about specific rule details")
    report.append("5. **Test wildcards** by checking if multiple files load")

    report.append("\n### Expected Behaviors")
    report.append("- ✅ Direct file imports should work with absolute paths")
    report.append("- ✅ Home directory (~) expansion should work")
    report.append("- ⚠️  Wildcards may not work (need to test)")
    report.append("- ✅ YAML frontmatter should be ignored/handled gracefully")
    report.append("- ✅ Rule content should be accessible in context")

    return '\n'.join(report)


def main():
    """Run the import validation tests."""
    print("Testing Claude Code import patterns for Cursor rules...")

    results = test_import_patterns()
    report = generate_test_report(results)

    # Save report
    report_path = Path('/Users/michaelhood/git/mastermind/worktrees/matching/claude-import-test-report.md')
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"\nTest report saved to: {report_path}")
    print("\nQuick Summary:")
    print(f"- Found {results['total_rules']} cursor rules")
    print(f"- Analyzed {len(results['test_files'])} test files")
    print(f"- Sampled {len(results['mdc_files'])} .mdc files")
    print("\nNext step: Follow manual testing steps in the report")


if __name__ == "__main__":
    main()