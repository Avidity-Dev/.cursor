# Task Magic Project Management System

This is a file-based project management system designed to work with any AI agent or human developer.

## Core Concepts

- **Projects**: Self-contained initiatives in `.ai/projects/`
- **Tasks**: Work items with status tracking
- **Context**: Background information and analysis
- **Memory**: Historical archive of completed work
- **Shared Resources**: Templates, workflows, and patterns used across projects

## Directory Structure

```
.ai/
├── INDEX.md                   # Master registry of all projects
├── projects/                  # Project-scoped organization
│   └── {project-name}/
│       ├── plan.md           # Project plan (PRD)
│       ├── tasks/            # Project tasks
│       ├── context/          # Background analysis
│       ├── handoffs/         # Session handoffs
│       └── PROJECT.md        # Project-specific index
├── shared/                   # Cross-project resources
│   ├── templates/           # Reusable code templates
│   ├── workflows/           # Standard processes
│   └── patterns/            # Common solutions
├── memory/                  # Global archive
│   ├── tasks/              # Archived task files
│   ├── plans/              # Archived plan files
│   ├── TASKS_LOG.md        # Task archive log
│   └── PLANS_LOG.md        # Plan archive log
├── agents/                  # Tool-specific guides
│   ├── cursor-guide.md     # Cursor AI instructions
│   ├── claude-guide.md     # Claude/terminal instructions
│   └── human-guide.md      # Human developer reference
└── SYSTEM.md               # This file
```

## File Formats

### Task Files

- Location: `.ai/projects/{project}/tasks/task{id}_description.md`
- Format: Markdown with YAML frontmatter
- Naming: `task{id}_descriptive_name.md` where `{id}` is sequential
- Sub-tasks: `task{parent_id}.{sub_id}_descriptive_name.md`

### Plan Files

- Location: `.ai/projects/{project}/plan.md`
- Format: Structured markdown following PRD template
- Purpose: Define what and why for each project

### Context Files

- Location: `.ai/projects/{project}/context/`
- Format: Markdown documents
- Purpose: Background analysis, dependencies, architecture decisions

### Metadata Headers

All files should include YAML frontmatter:

```yaml
---
project: project-name
id: unique-id
type: plan|task|context|template
related: [related-file-ids]
tags: [relevant, tags]
status: active|completed|archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
agent: cursor|claude|human
---
```

## For Tool-Specific Instructions

See `.ai/agents/` directory for guides tailored to your development tool.
