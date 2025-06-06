---
id: 9
title: "Update Task Magic Rules for Projects"
status: pending
priority: critical
feature: Task Magic Enhancement
dependencies: []
assigned_agent: null
created_at: "2025-06-05T23:43:53Z"
started_at: null
completed_at: null
error_log: null
---

## Description

Update tasks.mdc to support project-scoped paths

## Details

- Modify `rules/task-magic/tasks.mdc` to:
  - Support `.ai/projects/{project}/tasks/` paths
  - Update TASKS.md location to project-specific
  - Adjust file search patterns for project scope
  - Update examples to show project paths
  - Maintain backwards compatibility for migration
- Update task ID generation to be project-scoped
- Ensure memory paths remain global

## Test Strategy

- Test task creation in a project directory
- Verify task IDs don't conflict across projects
- Confirm TASKS.md updates work per project
- Validate backwards compatibility with existing structure

## Agent Notes

This is a critical update that enables the multi-project support. Must be careful to maintain backwards compatibility during transition.
