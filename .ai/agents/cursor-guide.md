# Cursor Agent Guide

To work with the Task Magic system in Cursor:

## Quick Start

1. Use `@.cursor/rules/task-magic/_index.mdc` for system overview
2. Tag specific rules when needed:
   - `@.cursor/rules/task-magic/tasks.mdc` for task operations
   - `@.cursor/rules/task-magic/plan.mdc` for planning
   - `@.cursor/rules/task-magic/memory.mdc` for archiving
   - `@.cursor/rules/task-magic/handoff.mdc` for session transfers

## Common Operations

### View All Projects

```
@.ai/INDEX.md show me all active projects
```

### Work on Tasks

```
@.cursor/rules/task-magic/tasks.mdc @.ai/projects/task-magic-enhancement/TASKS.md show tasks
@.cursor/rules/task-magic/tasks.mdc start next task
```

### Create Plans

```
@.cursor/rules/task-magic/plan.mdc create a plan for [feature]
```

### Archive Completed Work

```
@.cursor/rules/task-magic/memory.mdc archive completed tasks
```

## File Locations

- Project plans: `.ai/projects/{project-name}/plan.md`
- Task lists: `.ai/projects/{project-name}/TASKS.md`
- Individual tasks: `.ai/projects/{project-name}/tasks/`
- Context docs: `.ai/projects/{project-name}/context/`
- Handoffs: `.ai/projects/{project-name}/handoffs/`

## Best Practices

1. Always tag the appropriate rule before operations
2. Keep TASKS.md synchronized with task files
3. Create handoffs when switching contexts
4. Use context folders for background information
5. Archive completed tasks regularly

## Rules Reference

The `.cursor/rules/task-magic/` directory contains:

- `_index.mdc` - System overview (auto-loaded)
- `tasks.mdc` - Task management procedures
- `plan.mdc` - Planning procedures
- `memory.mdc` - Archive procedures
- `handoff.mdc` - Context transfer procedures
- `expand.mdc` - Task expansion guidance
- `project.mdc` - Project creation (when added)
