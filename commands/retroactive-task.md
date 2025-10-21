---
allowed-tools: mcp__Parallel__list_projects, mcp__Parallel__get_tasks, mcp__Parallel__create_task
description: Add a completed task retroactively to track work that was already done
---

# Retroactive Task Creation

## Current Context
- Current directory: !`pwd`
- Git status: !`git status --porcelain | head -5`
- Last commit: !`git log --oneline -1`

## Task: Create a Retroactive Task

You need to create a completed task to track work that has already been done.

### Input
The user has provided: `$ARGUMENTS`

### Process

1. **Parse the input** to understand:
   - What work was completed
   - Which project it belongs to (default to "housekeeping" if unclear)
   - Any specific details about the implementation

2. **Find the appropriate project**:
   - If the work is clearly related to a specific project, use that
   - Otherwise, use the "housekeeping" project (id: 49)
   - List available projects if needed

3. **Create the completed task** with:
   - Clear, descriptive title
   - Status: "completed"
   - Priority: Assess based on the work (default: "medium")
   - Comprehensive description including:
     - What was implemented/changed
     - Key files modified
     - Reasoning behind decisions
     - Any challenges overcome
     - Testing/verification done

4. **Format the description** using markdown with sections like:
   ```markdown
   ## What was done:
   [Summary of changes]

   ## Key decisions:
   [Important choices made]

   ## Files affected:
   - file1.py: [what changed]
   - file2.md: [what changed]

   ## Benefits:
   [Why this work was valuable]
   ```

5. **Confirm creation** by showing:
   - The project selected
   - The task title
   - The task number assigned
   - A brief summary of what was tracked

### Example Usage
- `/project:retroactive-task Fixed database migration numbering`
- `/project:retroactive-task Implemented enum validation system for status fields`
- `/project:retroactive-task Refactored authentication to use JWT tokens`

Execute this retroactive task creation now based on the provided input.
