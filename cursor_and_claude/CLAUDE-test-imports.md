# CLAUDE.md Import Test Configuration

This test file verifies different import strategies for Cursor rules into Claude Code.

## Strategy 1: Core Rules Import
Import essential rules that apply to most development tasks:

@/Users/michaelhood/git/.cursor/rules/python/code_style.mdc
@/Users/michaelhood/git/.cursor/rules/python/testing.mdc
@/Users/michaelhood/git/.cursor/rules/general/development_workflow.mdc
@/Users/michaelhood/git/.cursor/rules/general/documentation.mdc

## Strategy 2: Category-Based Imports
Group imports by category for better organization:

### Python Development
@/Users/michaelhood/git/.cursor/rules/python/code_style.mdc
@/Users/michaelhood/git/.cursor/rules/python/testing.mdc

### General Development
@/Users/michaelhood/git/.cursor/rules/general/data_engineering.mdc
@/Users/michaelhood/git/.cursor/rules/general/security.mdc
@/Users/michaelhood/git/.cursor/rules/general/logging.mdc

### Architecture & Design
@/Users/michaelhood/git/.cursor/rules/modes/architect.mdc

## Strategy 3: Conditional Import Approach
Use comments to indicate when certain rules should apply:

<!-- Always Active Rules -->
@/Users/michaelhood/git/.cursor/rules/python/code_style.mdc
@/Users/michaelhood/git/.cursor/rules/general/security.mdc

<!-- Project-Specific Rules -->
@/Users/michaelhood/git/.cursor/rules/entity_resolution_debugging.mdc

<!-- On-Demand Rules (reference but don't auto-import) -->
<!-- When creating documentation: @/Users/michaelhood/git/.cursor/rules/general/documentation.mdc -->
<!-- When architecting: @/Users/michaelhood/git/.cursor/rules/modes/architect.mdc -->

## Existing CLAUDE.md Content
Keep all existing project-specific guidance:

### Build/Test/Lint Commands
- `make setup` - Install dependencies
- `make test` - Run all tests
- `pytest tests/ -v` - Run tests with verbose output
- `make lint` - Run Ruff linter
- `make typecheck` - Run type checking with mypy
- `make format` - Auto-format code with Ruff

### Architecture Overview
The mastermind project follows Domain-Driven Design (DDD) architecture.
See `src/CLAUDE.md` for detailed layer guidance.

## Import Verification Checklist
- [ ] .mdc files load without syntax errors
- [ ] YAML frontmatter is properly handled
- [ ] Rule content is accessible in Claude context
- [ ] Nested imports work (if rules reference other files)
- [ ] Relative vs absolute paths both function
- [ ] Wildcards work or fail gracefully