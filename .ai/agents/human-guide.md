# Human Developer Guide

Quick reference for working with the Task Magic system.

## TL;DR

- **Projects live in**: `.ai/projects/{project-name}/`
- **View all projects**: `.ai/INDEX.md`
- **View tasks**: `.ai/projects/{project}/TASKS.md`
- **Task details**: `.ai/projects/{project}/tasks/task{id}_*.md`

## Task Status Icons

In TASKS.md files:

- `[ ]` = Not started
- `[-]` = In progress
- `[x]` = Completed
- `[!]` = Failed

## Quick Commands

### With Cursor

```
# View projects
@.ai/INDEX.md

# View tasks
@.ai/projects/my-project/TASKS.md

# Work on tasks
@rules/task-magic/tasks.mdc start next task
```

### Manual Operations

1. **Start a task**: Edit task file, change `status: pending` to `status: inprogress`
2. **Complete a task**: Change to `status: completed`
3. **Update TASKS.md**: Keep the checklist in sync

## Directory Structure

```
.ai/projects/my-project/
├── plan.md          # What we're building and why
├── TASKS.md         # Task checklist
├── tasks/           # Individual task files
├── context/         # Background docs, analysis
└── handoffs/        # Session transfer notes
```

## Creating a New Project

1. Add entry to `.ai/INDEX.md`
2. Create `.ai/projects/{name}/` directory
3. Add `plan.md` with project details
4. Create `TASKS.md` with initial tasks
5. Add task files in `tasks/` directory

## Task Dependencies

Tasks can depend on other tasks:

```yaml
dependencies: [1, 3] # Must complete tasks 1 and 3 first
```

## Archiving

Move completed work to `.ai/memory/`:

- Tasks → `.ai/memory/tasks/`
- Plans → `.ai/memory/plans/`
- Update logs: `TASKS_LOG.md`, `PLANS_LOG.md`

## Tips

- Use descriptive task filenames
- Keep tasks focused and testable
- Document context for future reference
- Create handoffs when pausing work
- Archive regularly to keep things clean
