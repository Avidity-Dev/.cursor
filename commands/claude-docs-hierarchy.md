---
allowed-tools: Read, Write, Edit, LS, Glob, Grep, TodoWrite
description: Analyze and create hierarchical CLAUDE.md documentation structure
---

# CLAUDE.md Hierarchy Manager

Create and maintain hierarchical CLAUDE.md files that get more specific as you go deeper into the directory tree.

## Usage

`/claude-docs-hierarchy [analyze|create|update|all] [--max-depth=3] [--auto-confirm]`

- `analyze` (default) - Report current structure and suggest improvements  
- `create` - Create missing CLAUDE.md files (interactive)
- `update` - Update existing files to follow hierarchy principles
- `all` - Full analysis, then interactive create/update
- `--max-depth=N` - Limit directory traversal depth (default: 3)
- `--auto-confirm` - Skip interactive confirmations (use with caution)

## Task: Manage CLAUDE.md Documentation Hierarchy

**Always start with analysis phase - never create files without showing the plan first**

### 1. Repository Analysis Phase

**Scan repository structure (max depth from --max-depth, default 3):**
- Use LS and Glob to map directories within depth limit
- Identify existing CLAUDE.md files and their locations
- Detect repository type (monorepo vs single-project)
- Find key implementation directories (src/, lib/, packages/, etc.)

**Smart Directory Classification:**

**✅ Auto-Include (will always suggest):**
- Root directory (/)
- Primary source directories (src/, lib/, packages/)
- Major functional areas with 3+ subdirectories or 5+ files
- Directories containing build configs (package.json, Cargo.toml, pyproject.toml, etc.)

**❓ Ask User (interactive confirmation):**
- Individual modules within primary directories
- Test directories (tests/, test/, spec/, __tests__)  
- Documentation directories (docs/, documentation/)
- Example/demo directories
- Directories with 2-4 files that seem substantial

**❌ Auto-Skip (never suggest):**
- Hidden directories (.git/, .vscode/, node_modules/, __pycache__/)
- Build output (dist/, build/, target/, out/)
- Cache directories (tmp/, temp/, cache/)
- Directories with <2 files
- Purely configuration directories (only config files, no implementation)

**Current State Assessment:**
- Read existing CLAUDE.md files to understand current documentation
- Identify redundancy between parent and child CLAUDE.md files
- Map content distribution and find gaps
- Note what's working well vs what needs improvement

### 2. Present Analysis Results

**Show structured analysis report:**
```
📁 Repository Analysis Results
===============================

Current CLAUDE.md files:
✅ ./CLAUDE.md (exists - project root)
❌ src/CLAUDE.md (missing - suggested)

Directory suggestions:
✅ ./CLAUDE.md (auto-include - project root)
✅ src/CLAUDE.md (auto-include - primary source dir, 3 subdirs) 
❓ src/api/CLAUDE.md (ask - module with 5 files) - Create? [y/N]
❓ src/db/CLAUDE.md (ask - module with 8 files) - Create? [y/N]
❓ tests/CLAUDE.md (ask - test directory) - Create? [y/N]
❌ config/CLAUDE.md (auto-skip - config only)
❌ node_modules/ (auto-skip - dependencies)

Depth: 2/3 levels (--max-depth=3)
```

**If not analyze-only mode, get user confirmations:**
- For each "❓" directory, ask user y/N to include
- Show context: file count, purpose, why it's suggested
- Allow bulk answers: "y for all modules", "n for all tests"
- Confirm final list before proceeding

### 3. Hierarchy Design Phase

**Apply Hierarchy Principles:**

**Root Level CLAUDE.md:**
- Project overview and purpose
- When to work at root vs subdirectories
- Project-wide workflows and commands
- High-level architecture (not implementation details)
- Navigation pointers to subdirectories

**Mid-Level CLAUDE.md (e.g., src/):**
- Module relationships and dependencies
- When to work in each subdirectory
- Cross-module architecture and patterns
- Commands that span multiple modules
- Clear pointers to specific modules

**Leaf-Level CLAUDE.md (e.g., src/module/):**
- Implementation-specific details
- Module-specific commands and workflows
- Architecture and patterns within the module
- Development guidelines for this specific area
- Pointers back to parent for broader context

### 3. Content Distribution Rules

**Avoid Redundancy:**
- Each piece of information should live at exactly one level
- Parent files summarize and point to children for details
- Children assume you've read parent for context
- Implementation details always go in the most specific relevant location

**Navigation Pattern:**
```markdown
**For [broader context], see `../CLAUDE.md`**
**For [specific details], see `subdirectory/CLAUDE.md`**
```

**Command Distribution:**
- Project-wide commands → Root CLAUDE.md
- Cross-module commands → Mid-level CLAUDE.md
- Module-specific commands → Leaf CLAUDE.md

### 4. Implementation Phase

**Only proceed if user confirmed the plan or --auto-confirm was used**

**For each confirmed directory level:**

1. **Determine Appropriate Content:**
   - What is unique to this level?
   - What commands are relevant here?
   - What architecture details belong here?
   - What navigation is needed?

2. **Create/Update CLAUDE.md:**
   - Use appropriate template based on directory type and depth
   - Include navigation links to parent and children
   - Focus on level-appropriate details
   - Add clear "when to work here" guidance
   - **Preserve any existing valuable content**

3. **Apply Smart Templates:**

**Root Template:**
```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview
[High-level description - what this project does]

**For implementation details, see `[main-src-dir]/CLAUDE.md`**

## When to Work Where

### Repository Root Level
Work here when dealing with:
- [Project-wide concerns]

### Implementation Level (`[src-dir]/`)
Navigate to `[src-dir]/CLAUDE.md` when working on:
- [Implementation concerns]

## Project-Wide Workflows
[Commands that work across the whole project]

## System Architecture
[High-level architecture, not implementation details]

## Development Navigation
- **[Area]**: See `[dir]/CLAUDE.md` for details
```

**Mid-Level Template:**
```markdown
# CLAUDE.md

This file provides guidance for working in the `[directory]` area.

## Project Overview
[Brief description of this area's role]

**For overall project context, see `../CLAUDE.md`**
**For [specific module] details, see `[module]/CLAUDE.md`**

## Module Relationships
[How modules in this area relate]

## When to Work in Each Module
[Guidance on which module to work in for different tasks]

## Cross-Module Operations
[Commands and workflows that span modules]

## Architecture Overview
[Architecture at this level]

## Module Documentation
- **[Module]**: See `[module]/CLAUDE.md` for details
```

**Leaf-Level Template:**
```markdown
# CLAUDE.md

This file provides guidance for working with [specific module/area].

## Project Overview
[Module description and purpose]

**For overall architecture and module relationships, see `../CLAUDE.md`**

## Common Development Commands
[Module-specific commands]

## Architecture
[Module-specific architecture and patterns]

## Key Implementation Details
[Details specific to this module]

## Development Guidelines
[Guidelines specific to this area]
```

### 5. Quality Checks

**Verify Hierarchy:**
- No redundant information between levels
- Clear navigation paths up and down
- Each level has appropriate scope
- Commands are at the right level

**Content Quality:**
- Each CLAUDE.md provides value at its level
- Information is current and accurate
- Templates are customized to the specific context
- Navigation links work correctly

### 6. Summary Report

**Provide comprehensive summary:**
```
📋 CLAUDE.md Hierarchy Results
==============================

Files processed:
✅ Created: src/CLAUDE.md (module relationships)
✅ Updated: ./CLAUDE.md (added navigation, removed redundancy)  
✅ Created: src/api/CLAUDE.md (API implementation details)
⏭️  Skipped: tests/ (user declined)

Changes made:
• Removed duplicate MCP tools list from root CLAUDE.md
• Added navigation links between all levels
• Established clear "when to work where" guidance
• Preserved existing task automation content

Hierarchy depth: 2 levels
Next steps: Review generated files and customize as needed
```

**Quality verification:**
- Verify no information duplication between levels
- Confirm navigation links work correctly  
- Check that each level provides appropriate value
- Suggest any additional improvements needed

## Examples

### Monorepo Structure:
```
project/
├── CLAUDE.md (project overview, when to work where)
├── src/CLAUDE.md (module relationships, cross-module patterns)
├── src/module1/CLAUDE.md (module1 specifics)
├── src/module2/CLAUDE.md (module2 specifics)
└── tests/CLAUDE.md (testing approach, test organization)
```

### Single Project:
```
project/
├── CLAUDE.md (project overview, overall development)
├── lib/CLAUDE.md (core implementation details)
└── examples/CLAUDE.md (example usage and patterns)
```

## Interactive Workflow Examples

### Example 1: Full Analysis
```
User: /claude-docs-hierarchy analyze
Assistant: [Shows analysis report with ✅❓❌ classifications]
          "Found 3 auto-include, 4 ask-user, 2 auto-skip directories"
```

### Example 2: Create Mode  
```
User: /claude-docs-hierarchy create
Assistant: [Shows analysis] 
          "src/api/CLAUDE.md (8 files, API module) - Create? [y/N]"
User: y
Assistant: "tests/CLAUDE.md (test directory) - Create? [y/N]"  
User: n
Assistant: [Creates confirmed files, shows summary]
```

### Example 3: Depth Limiting
```
User: /claude-docs-hierarchy all --max-depth=2
Assistant: "Limited to 2 levels: stopping at src/module/ (not src/module/subdir/)"
```

## Best Practices

1. **Always start with analyze** - understand before changing
2. **Use depth limits** - avoid creating too many files (default: 3 levels)
3. **Be selective** - not every directory needs a CLAUDE.md
4. **Preserve valuable content** - existing information is often worth keeping
5. **Review generated files** - customize templates to your specific context
6. **Test navigation** - verify links between levels work correctly