---
id: 11
title: "Update Memory Rules"
status: completed
priority: high
feature: Task Magic Enhancement
dependencies: []
assigned_agent: null
created_at: "2025-06-05T23:43:53Z"
started_at: "2025-06-06T21:02:43Z"
completed_at: "2025-06-06T21:04:51Z"
error_log: null
---

## Description

Update memory.mdc for new directory structure

## Details

- Modify `rules/task-magic/memory.mdc` to:
  - Support archiving from project-scoped paths
  - Update archival source paths (.ai/projects/{project}/tasks/)
  - Maintain global memory destination (.ai/memory/)
  - Update log format to include project context
  - Support both task and plan archival with project info
- Ensure backwards compatibility during transition
- Update archival commands and examples

## Test Strategy

- Test task archival from project directories
- Verify log entries include project context
- Confirm memory paths work correctly
- Validate backwards compatibility

## Agent Notes

This updates memory rule to handle project-scoped archival while keeping memory global.

**Started working on this task** - Will update memory.mdc to support project-scoped archival.

**COMPLETED** - Successfully updated memory.mdc with:

- Project-scoped archival source paths (.ai/projects/{project}/tasks/)
- Global memory destination maintained (.ai/memory/)
- Updated log formats with project context for cross-project learning
- Backwards compatibility with legacy .ai/tasks/ and .ai/plans/ paths
- Enhanced archival procedures and file naming conventions
