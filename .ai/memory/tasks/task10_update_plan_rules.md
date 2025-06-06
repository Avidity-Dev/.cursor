---
id: 10
title: "Update Plan Rules for Projects"
status: completed
priority: critical
feature: Task Magic Enhancement
dependencies: []
assigned_agent: null
created_at: "2025-06-05T23:43:53Z"
started_at: "2025-06-06T21:00:29Z"
completed_at: "2025-06-06T21:02:06Z"
error_log: null
---

## Description

Update plan.mdc to support project directory structure

## Details

- Modify `rules/task-magic/plan.mdc` to:
  - Support `.ai/projects/{project}/plan.md` paths
  - Update PRD location references
  - Adjust file search patterns for project scope
  - Update examples to show project-scoped plans
  - Maintain backwards compatibility for migration
- Update plan templates and examples
- Ensure global INDEX.md can reference project plans

## Test Strategy

- Test plan creation in a project directory
- Verify plan references work correctly
- Confirm project isolation
- Validate backwards compatibility

## Agent Notes

This updates the plan rule to work with project-scoped directories.

**Started working on this task** - Will update plan.mdc to support project-scoped plan.md files.

**COMPLETED** - Successfully updated plan.mdc with:

- Project-scoped planning structure (.ai/projects/{project}/plan.md)
- Project context detection logic
- Backwards compatibility with legacy .ai/plans/ structure
- Updated filename conventions and agent responsibilities
- Global INDEX.md registry for project discovery
