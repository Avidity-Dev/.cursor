# Proposed Enhancement to Task Magic System

## Conceptual Clarity: Separating System from Rules

Task Magic is actually TWO things:

1. **A Project Management System** (files and structure for tracking work)
2. **A Set of Rules** (instructions for AI agents on how to use the system)

This enhancement proposes clearly separating these concerns:

- **`.ai/`** - The project management system (tool-agnostic)
- **`.cursor/rules/task-magic/`** - Rules for how Cursor interacts with the system
- **`.ai/agents/`** - Guides for other tools (Claude, Codeium, humans)

## Current vs Enhanced Structure

### Current Structure (Mixed Concerns)

```
.cursor/rules/task-magic/       # Rules and system description mixed
├── tasks.mdc                   # Rule: how to manage tasks
├── plan.mdc                    # Rule: how to create plans
├── README.md                   # System: describes project management
└── _index.mdc                  # Rule: overview for AI

.ai/                           # Single project focus
├── plans/
│   ├── PLAN.md
│   └── features/
├── tasks/
├── memory/
├── handoffs/
└── TASKS.md
```

### Enhanced Structure (Clear Separation)

```
.cursor/rules/task-magic/       # ONLY rules for Cursor
├── tasks.mdc                   # Rule: how to manage tasks in .ai/
├── plan.mdc                    # Rule: how to create plans in .ai/
├── project.mdc                 # Rule: how to create new projects
├── context.mdc                 # Rule: how to manage context folders
└── _index.mdc                  # Rule: overview of task-magic rules

.ai/                           # The actual project management SYSTEM
├── INDEX.md                   # Master registry of all projects
├── projects/                  # Project-scoped organization
│   ├── test-coverage/
│   │   ├── plan.md           # Created using plan.mdc rule
│   │   ├── tasks/            # Managed using tasks.mdc rule
│   │   ├── context/          # NEW: Background analysis
│   │   ├── handoffs/
│   │   └── PROJECT.md        # Project-specific index
│   └── entity-resolution/
│       ├── plan.md
│       ├── tasks/
│       ├── context/
│       └── PROJECT.md
├── shared/                    # NEW: Cross-project resources
│   ├── templates/            # Reusable code templates
│   ├── workflows/            # Standard processes
│   └── patterns/             # Common solutions
├── memory/                   # Global memory (unchanged)
├── agents/                   # NEW: Tool-specific guides
│   ├── cursor-guide.md       # "Use @.cursor/rules/task-magic/"
│   ├── claude-guide.md       # Instructions for terminal agents
│   └── human-guide.md        # Quick reference for developers
└── SYSTEM.md                 # Describes the project management system
```

## Key Enhancements

### 1. Project Registry (INDEX.md)

```markdown
# AI Project Registry

## Active Projects

| Project           | ID      | Status   | Lead Files                                 | Tags              |
| ----------------- | ------- | -------- | ------------------------------------------ | ----------------- |
| Test Coverage     | tcp-001 | active   | [plan](projects/test-coverage/plan.md)     | #testing #quality |
| Entity Resolution | er-001  | planning | [plan](projects/entity-resolution/plan.md) | #algorithms       |

## Project Discovery

- Use `@.ai/INDEX.md` to see all projects
- Use `@.ai/projects/{project-name}/` to focus on specific project

## For AI Agents

- Cursor: See `.ai/agents/cursor-guide.md`
- Claude/Others: See `.ai/agents/claude-guide.md`
- Humans: See `.ai/agents/human-guide.md`
```

### 2. Context Folders

Each project gets a `context/` folder for:

- Background analysis
- External dependencies
- Risk assessments
- Technical debt notes
- Architecture decisions
- Investigation results
- Performance benchmarks

### 3. Agent Guides

New `.ai/agents/` folder contains tool-specific instructions:

**cursor-guide.md**:

```markdown
# Cursor Agent Guide

To work with the Task Magic system:

1. Use `@.cursor/rules/task-magic/_index.mdc` for overview
2. Tag specific rules when needed:
   - `@.cursor/rules/task-magic/tasks.mdc` for task operations
   - `@.cursor/rules/task-magic/plan.mdc` for planning
3. The rules will guide you on file formats and procedures
```

**claude-guide.md**:

```markdown
# Claude/Terminal Agent Guide

The Task Magic system uses these conventions:

1. Tasks: Create in `.ai/projects/{project}/tasks/task{id}_description.md`
2. Format: YAML frontmatter with status, priority, dependencies
3. Always update `.ai/projects/{project}/TASKS.md` when changing tasks
4. See `.ai/SYSTEM.md` for full conventions
```

### 4. Metadata Headers

Add to all files for better AI discovery:

```yaml
---
project: test-coverage
id: tcp-001
type: plan|task|context|template
related: [tcp-task-001, tcp-context-001]
tags: [testing, coverage, quality]
status: active|completed|archived
created: 2024-01-15
updated: 2024-01-20
agent: cursor|claude|human
---
```

### 5. System Documentation

New `.ai/SYSTEM.md` file describes the project management system itself:

```markdown
# Task Magic Project Management System

This is a file-based project management system designed to work with any AI agent or human developer.

## Core Concepts

- Projects: Self-contained initiatives in `.ai/projects/`
- Tasks: Work items with status tracking
- Context: Background information and analysis
- Memory: Historical archive of completed work

## File Formats

[Details about YAML frontmatter, naming conventions, etc.]

## For Tool-Specific Instructions

See `.ai/agents/` for your tool
```

## Migration Strategy

1. **Create `.ai/SYSTEM.md`** documenting the project management system
2. **Create `.ai/agents/`** with tool-specific guides
3. **Add `.ai/INDEX.md`** for project discovery
4. **Update `.cursor/rules/task-magic/README.md`** to clarify it describes rules, not the system
5. **Wrap current .ai/ content** in `projects/current/`
6. **New projects** use enhanced structure

## Benefits of Separation

1. **Tool Agnostic**: Any AI or human can use `.ai/` by reading the appropriate guide
2. **Clear Purpose**: Rules configure behavior, `.ai/` contains actual work
3. **Portability**: Share `.ai/` with teams using different tools
4. **Discoverability**: INDEX.md and agent guides make system self-documenting
5. **Scalability**: Multi-project support with clear boundaries

## Rule Updates Needed

1. Update `_index.mdc` to clarify it governs rules, not the system
2. Add `project.mdc` for creating new projects in `.ai/projects/`
3. Update `tasks.mdc` to support project-scoped paths
4. Add `context.mdc` for managing context folders
5. Update all rules to reference `.ai/` paths instead of assuming single project
