---
id: 26.2
title: "Update Task Archival Process for Project Memory"
status: pending
priority: high
feature: "Memory System Enhancement"
dependencies:
  - 26.1
assigned_agent: null
created_at: "2025-06-06T22:09:56Z"
started_at: null
completed_at: null
error_log: null
---

## Description

Modify the task archival logic to archive tasks to project-specific memory location instead of global memory.

## Details

- Update task archival commands to move tasks to `.ai/projects/{project-name}/memory/tasks/` instead of `.ai/memory/tasks/`
- Modify the archival process to update project-specific MEMORY.md instead of just global TASKS_LOG.md
- Ensure backwards compatibility for workspace-level tasks (non-project tasks)
- Update archival logic to:
  - Detect if task belongs to a project (based on current directory or context)
  - Route to appropriate memory location (project vs global)
  - Update both project memory and global logs appropriately
- Test that existing global archival still works for non-project tasks
- Ensure project memory archival updates project MEMORY.md with task summaries

## Test Strategy

- Test archiving a project task to verify it goes to project memory
- Test archiving a non-project task to verify it goes to global memory
- Verify project MEMORY.md is updated when project tasks are archived
- Confirm global TASKS_LOG.md still functions for workspace-level tasks
- Test that archival commands work correctly in both contexts
