---
id: 11
title: "Update Memory Rules"
status: pending
priority: high
feature: Task Magic Enhancement
dependencies: []
assigned_agent: null
created_at: "2025-06-05T23:43:53Z"
started_at: null
completed_at: null
error_log: null
---

## Description

Update memory.mdc for new directory structure

## Details

- Modify `rules/task-magic/memory.mdc` to:
  - Support archiving from project directories
  - Maintain global memory location
  - Update path examples throughout
  - Add project context to archive entries
- Ensure archive logs include project information
- Update file movement commands for new paths

## Test Strategy

- Test archiving tasks from a project
- Verify tasks move to global memory
- Confirm logs include project context
- Validate memory consultation works across projects

## Agent Notes

Memory remains global to preserve cross-project learning, but must be updated to handle project-scoped source paths.
