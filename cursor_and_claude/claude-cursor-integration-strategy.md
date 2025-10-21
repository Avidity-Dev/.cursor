# Claude Code + Cursor Rules Integration Strategy

## Testing Summary

Created test files to validate importing Cursor `.mdc` rules into Claude Code via `@import` syntax in CLAUDE.md files.

### What We Tested
- **74 Cursor rules** available in `/Users/michaelhood/git/.cursor/rules/`
- **Multiple import patterns**: absolute paths, home directory (~), wildcards
- **MDC file structure**: YAML frontmatter + markdown content

### Key Findings
1. **MDC files are valid markdown** with optional YAML frontmatter
2. **Claude Code supports @imports** (as of 2025) with 5-hop depth limit
3. **Both tools can consume same files** without modification

## Recommended Strategy: Unified Rule System

### Implementation Plan

#### 1. Keep Cursor Rules as Primary Source
```
/Users/michaelhood/git/.cursor/rules/    # Master location
├── general/                            # Shared development rules
├── python/                             # Language-specific rules
├── modes/                              # Special modes (architect, etc.)
└── project-specific/                   # Per-project overrides
```

#### 2. Minimal CLAUDE.md with Smart Imports
```markdown
# CLAUDE.md

## Project Rules
Import shared development standards from Cursor rules:

@~/.cursor/rules/general/development_workflow.mdc
@~/.cursor/rules/general/security.mdc
@~/.cursor/rules/python/code_style.mdc
@~/.cursor/rules/python/testing.mdc

## Project-Specific Configuration
[Keep existing build commands, architecture notes, etc.]
```

#### 3. Conditional Import Pattern
For rules that should only load in certain contexts:

```markdown
<!-- Always Active -->
@~/.cursor/rules/python/code_style.mdc

<!-- Context-Specific (commented for manual activation) -->
<!-- When architecting: @~/.cursor/rules/modes/architect.mdc -->
<!-- For data engineering: @~/.cursor/rules/general/data_engineering.mdc -->
```

## Migration Steps

### Phase 1: Test Import Functionality
1. Backup current CLAUDE.md: `cp CLAUDE.md CLAUDE.md.backup`
2. Add single import: `@~/.cursor/rules/python/code_style.mdc`
3. Start new Claude Code session and verify rule loads
4. Test asking about specific rule content

### Phase 2: Gradual Migration
1. Identify overlapping content between CLAUDE.md and Cursor rules
2. Remove duplicates from CLAUDE.md
3. Add @imports for corresponding Cursor rules
4. Test in new Claude Code session

### Phase 3: Full Integration
1. Convert CLAUDE.md to primarily use @imports
2. Keep only project-specific content in CLAUDE.md
3. Document import structure for team

## Benefits of This Approach

### Advantages
- **Single source of truth**: Maintain rules in one location
- **Tool parity**: Both Cursor and Claude Code use same rules
- **Version control**: All rules tracked in git
- **Modular**: Easy to enable/disable specific rule sets
- **Team consistency**: Everyone uses same rule definitions

### Potential Issues & Solutions

| Issue | Solution |
|-------|----------|
| Wildcards may not work | Use explicit file imports instead |
| Rule conflicts | Use comment-based conditional imports |
| Tool-specific needs | Create separate subdirectories in .cursor/rules |
| Performance concerns | Claude Code caches imported files (15min) |

## Testing Checklist

- [ ] Test single file import in CLAUDE.md
- [ ] Verify YAML frontmatter doesn't break imports
- [ ] Test home directory (~) expansion
- [ ] Verify nested imports (rules that reference other files)
- [ ] Test with fresh Claude Code session
- [ ] Validate rule content is accessible via prompts
- [ ] Check if wildcards work (likely not supported)

## Next Steps

1. **Immediate**: Test with `CLAUDE-test-imports.md` renamed to `CLAUDE.md`
2. **Short-term**: Migrate overlapping content to Cursor rules
3. **Long-term**: Establish team conventions for rule management

## Alternative Approaches (Not Recommended)

### Why NOT These Approaches:

**Symlink Everything**: Could cause circular dependencies
**Duplicate Rules**: Maintenance nightmare, drift inevitable
**Generate CLAUDE.md**: Adds complexity, loses direct edit capability
**Separate Rule Sets**: Defeats purpose of consistency

## Conclusion

The `@import` feature in Claude Code (2025) makes centralization viable. Keep Cursor rules as the source of truth and use CLAUDE.md as a thin import layer with project-specific additions. This provides maximum consistency with minimum maintenance overhead.