# Test CLAUDE.md with Cursor Rule Imports

This file tests various import patterns for bringing Cursor rules into Claude Code.

## Test 1: Direct Rule Import
Testing if .mdc files can be imported directly:

@/Users/michaelhood/git/.cursor/rules/python/code_style.mdc
@/Users/michaelhood/git/.cursor/rules/general/data_engineering.mdc

## Test 2: Wildcard Import Pattern
Testing if wildcards work for importing multiple rules:

@/Users/michaelhood/git/.cursor/rules/python/*.mdc
@/Users/michaelhood/git/.cursor/rules/general/*.mdc

## Test 3: Relative Path Import
Testing relative imports (assuming this file is in project root):

@../../.cursor/rules/python/testing.mdc

## Test 4: Home Directory Shorthand
Testing if ~ expansion works:

@~/.cursor/rules/general/documentation.mdc

## Test 5: Mixed Content with Imports
Here's some regular CLAUDE.md content mixed with imports:

### Project-Specific Guidelines
- Follow DDD architecture patterns
- Use type hints everywhere

### Imported Python Rules
@/Users/michaelhood/git/.cursor/rules/python/code_style.mdc

### Imported Testing Rules
@/Users/michaelhood/git/.cursor/rules/python/testing.mdc

## Test 6: Recursive Import Test
Create a rule that imports another rule to test depth limits:

@/Users/michaelhood/git/.cursor/rules/prime.mdc

## Test Notes
- Max import depth: 5 hops according to docs
- Imports not evaluated in code blocks: `@this-should-not-import.md`
- Both relative and absolute paths should work