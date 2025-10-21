---
allowed-tools: mcp__Parallel__create_task, mcp__Parallel__get_tasks
description: Quickly create a housekeeping task for miscellaneous work
---

# Quick Housekeeping Task

## Context
- Project: Housekeeping (id: 49)
- Purpose: Track miscellaneous tasks and ad-hoc work
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`

## Task: Create Housekeeping Task

Create a task in the housekeeping project for tracking miscellaneous work.

### Input
Task description: `$ARGUMENTS`

### Process

1. **Parse the task description** to determine:
   - Title (first line or summary)
   - Priority (look for: urgent, critical, high, medium, low)
   - Status (default: pending, unless "completed" is mentioned)
   - Whether this is retroactive (already done) or new work

2. **Create the task** in housekeeping project (id: 49) with:
   - **Title**: Clear, action-oriented summary
   - **Status**:
     - "completed" if past tense or mentions "done/fixed/completed"
     - "pending" otherwise
   - **Priority**:
     - "critical" if mentions urgent/critical/blocking
     - "high" if mentions important/high/asap
     - "low" if mentions minor/trivial/cleanup
     - "medium" otherwise
   - **Description**: Expand on the title with:
     - Context about why this is needed
     - Specific requirements or constraints
     - Expected outcome

3. **For retroactive tasks** (already completed):
   - Set status to "completed"
   - Add implementation notes to description
   - Include what was changed and why

4. **Confirm creation** by showing:
   - Task number assigned
   - Title created
   - Status and priority set
   - Quick link to view all housekeeping tasks

### Examples

Input: `Fix typo in README`
→ Creates: Low priority pending task

Input: `Fixed database migration numbering issue`
→ Creates: Medium priority completed task (retroactive)

Input: `URGENT: Fix production deployment blocker`
→ Creates: Critical priority pending task

Input: `Add logging to authentication module - needed for debugging`
→ Creates: High priority pending task with context

### Quick Tips
- Use past tense for completed work
- Include "urgent" or "critical" for high priority
- Add context after a dash or colon
- Multiple tasks? Separate with semicolons

Execute the task creation now based on the provided description.
