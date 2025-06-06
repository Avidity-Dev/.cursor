---
id: 12
title: "Update Index Rule"
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

Update \_index.mdc to clarify system vs rules separation

## Details

- Modify `rules/task-magic/_index.mdc` to:
  - Clearly state Task Magic is TWO things
  - Explain .ai/ is the system (tool-agnostic)
  - Explain rules/ contains Cursor-specific instructions
  - Update component descriptions for new structure
  - Add reference to INDEX.md for project discovery
- Emphasize fetching appropriate rules
- Update examples to use project paths

## Test Strategy

- Verify \_index.mdc loads automatically in Cursor
- Confirm clarity of system vs rules explanation
- Test that rule fetching guidance is accurate
- Validate all component descriptions are updated

## Agent Notes

This is the entry point for Cursor users, so clarity about the separation of concerns is critical.
