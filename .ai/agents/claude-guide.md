# Claude/Terminal Agent Guide

The Task Magic system uses these conventions for managing projects and tasks.

## File Structure

```
.ai/
├── INDEX.md                          # List of all projects
├── projects/{project-name}/
│   ├── plan.md                      # Project plan (PRD)
│   ├── TASKS.md                     # Task checklist
│   ├── tasks/                       # Individual task files
│   │   └── task{id}_description.md  # Task details
│   ├── context/                     # Background docs
│   └── handoffs/                    # Session transfers
└── memory/                          # Archived work
```

## Task File Format

Each task uses YAML frontmatter:

```yaml
---
id: 1                        # Unique ID (or "1.1" for sub-tasks)
title: 'Task Title'
status: pending              # pending|inprogress|completed|failed
priority: medium             # critical|high|medium|low
feature: 'Feature Name'
dependencies: [3, 5]         # Task IDs this depends on
created_at: "2024-01-20T10:00:00Z"
started_at: null
completed_at: null
error_log: null
---

## Description
Brief task summary

## Details
- Specific requirements
- Implementation steps

## Test Strategy
How to verify completion
```

## Common Operations

### List Projects

Read `.ai/INDEX.md`

### View Tasks

Read `.ai/projects/{project}/TASKS.md`

### Start a Task

1. Find first pending task in TASKS.md
2. Check dependencies are completed
3. Update task file: `status: inprogress`
4. Update TASKS.md: change `[ ]` to `[-]`

### Complete a Task

1. Update task file: `status: completed`
2. Update TASKS.md: change `[-]` to `[x]`

### Create Tasks

1. Determine next ID from existing tasks
2. Create task file in `tasks/` directory
3. Add entry to TASKS.md

### Archive Tasks

1. Move completed/failed task files to `.ai/memory/tasks/`
2. Append summary to `.ai/memory/TASKS_LOG.md`
3. Remove from TASKS.md

## TASKS.md Format

```markdown
- [ ] **ID 1: Task Title** (Priority: high)

  > Dependencies: 3, 5
  > Task description here

- [-] **ID 2: Another Task** (Priority: medium)

  > In progress task

- [x] **ID 3: Completed Task** (Priority: low)
  > This task is done
```

Icons:

- `[ ]` = Pending
- `[-]` = In Progress
- `[x]` = Completed
- `[!]` = Failed

## Best Practices

1. Always check dependencies before starting tasks
2. Keep TASKS.md synchronized with task files
3. Use descriptive filenames: `task1_implement_auth.md`
4. Archive completed work to keep active lists clean
5. Create handoff files when switching sessions

## Timestamps

Use ISO format: `YYYY-MM-DDTHH:MM:SSZ`
Example: `2024-01-20T15:30:00Z`
