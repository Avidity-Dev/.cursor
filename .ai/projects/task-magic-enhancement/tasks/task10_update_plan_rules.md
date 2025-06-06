---
id: 10
title: "Update Plan Rules for Projects"
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

Update plan.mdc to support project directory structure

## Details

- Modify `rules/task-magic/plan.mdc` to:
  - Support `.ai/projects/{project}/plan.md` paths
  - Remove requirement for global PLAN.md
  - Update directory structure examples
  - Adjust file creation logic for projects
- Each project should have its own plan.md
- Update archival paths for project-scoped plans

## Test Strategy

- Test plan creation within a project
- Verify plans are created in correct location
- Confirm no conflicts with other projects
- Validate plan archival works correctly

## Agent Notes

This update removes the global PLAN.md requirement and makes plans project-scoped, which better aligns with multi-project support.
