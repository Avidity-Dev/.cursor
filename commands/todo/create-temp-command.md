---
allowed-tools: Write, mcp__Parallel__get_task, mcp__Parallel__search_tasks, mcp__Parallel__get_project
description: Create a task-focused command for a specific Parallel task
---

Create a temporary Claude slash command for task_number $1 in project_id $2.

You will place the generated command in `.claude/commands/temp/[PROJECT_ID]_[TASK_NUMBER]_[TASK_NAME].md` in the project directory (NOT user directory).

## Command Generation Guidelines

When creating the Claude slash command:

1. **Fetch task details** using `mcp__Parallel__get_task(task_number=$1, project_id=$2)` and `mcp__Parallel__get_project(project_id=$2)`
2. **Create the command** using the template below
3. **Replace ALL placeholders** with actual values from the task data
4. **Customize description** to be task-specific and actionable
5. **Tailor sections** based on task type (bug fix, feature, refactoring, etc.)
6. **Include relevant file paths** and code examples from the task description
7. **Set appropriate success criteria** based on task requirements

## Frontmatter Best Practices

- **allowed-tools**: Include only tools actually needed for this specific task
- **description**: Make it specific and actionable, not generic
- Use format: `[Brief task description] - Complete task [TASK_ID] in project [PROJECT_SLUG]`

## Template to Use

````markdown
---
allowed-tools: mcp__Parallel__update_task_status, mcp__Parallel__add_completion_notes, mcp__Parallel__add_progress_comment, mcp__Parallel__get_project_completion_stats, Bash, Read, Write, Edit, MultiEdit, Grep, Glob
description: [TASK_DESCRIPTION] - Complete task [TASK_ID] in project [PROJECT_SLUG]
---

# Task Command Template: [TASK_NAME]

## Parallel Project Context

- **Project ID**: [PROJECT_ID] ([PROJECT_SLUG])
- **Task Number**: [TASK_NUMBER]
- **Global Task ID**: [TASK_ID]
- **Priority**: [Low|Medium|High|Critical]
- **Use Parallel MCP tools** to track progress

## Problem Statement

[Describe the specific problem or requirement that needs to be addressed]

## Your Mission

### 1. Update task status

```python
mcp__Parallel__update_task_status(task_id=[TASK_ID], status="in_progress")
```

### 2. [PRIMARY_OBJECTIVE_1]

**[Sub-section description]**

- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

### 3. [PRIMARY_OBJECTIVE_2]

**[Implementation details]**

```python
# Example code or approach
[CODE_EXAMPLE]
```

**Files to [modify|examine|create]:**

- [File path 1]: [What to do]
- [File path 2]: [What to do]

### 4. [ADDITIONAL_OBJECTIVES]

**Current [issue|pattern] to [improve|fix]:**

```python
# BAD: [Description of problematic code]
[BAD_CODE_EXAMPLE]
```

**Better approach:**

```python
# GOOD: [Description of improved code]
[GOOD_CODE_EXAMPLE]
```

### 5. [TESTING_AND_VALIDATION]

**[Testing strategy]:**

- [Test requirement 1]
- [Test requirement 2]
- [Performance/quality metric to verify]

### 6. Complete the task

**[Final verification steps]:**

```bash
# Commands to run for testing/validation
[COMMAND_EXAMPLES]
```

```python
mcp__Parallel__add_completion_notes(
    task_id=[TASK_ID],
    implementation_details="[What was implemented and how]",
    decisions_made="[Key architectural or design decisions]",
    challenges_solved="[Problems encountered and solutions]",
    test_results="[Testing outcomes and metrics]"
)
mcp__Parallel__update_task_status(task_id=[TASK_ID], status="completed")
```

## Success Criteria

- [Measurable success criterion 1]
- [Measurable success criterion 2]
- [Performance or quality requirement]
- [Functional requirement confirmation]
````
