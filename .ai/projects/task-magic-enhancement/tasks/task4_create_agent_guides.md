---
id: 4
title: "Create Agent Guides"
status: completed
priority: high
feature: Task Magic Enhancement
dependencies: [1]
assigned_agent: null
created_at: "2025-06-05T23:43:53Z"
started_at: "2025-06-05T23:43:53Z"
completed_at: "2025-06-05T23:43:53Z"
error_log: null
---

## Description

Create tool-specific guides for Cursor, Claude, and human developers

## Details

- Create `.ai/agents/cursor-guide.md` for Cursor users
  - Reference .mdc rules
  - Provide common operations examples
  - List rule locations
- Create `.ai/agents/claude-guide.md` for terminal AI users
  - Document conventions without .mdc dependencies
  - Provide task file format
  - Include operation instructions
- Create `.ai/agents/human-guide.md` for manual users
  - Quick reference format
  - Visual task status icons
  - Directory structure overview

## Test Strategy

- Verify all three guide files exist
- Confirm each guide is self-contained
- Test that instructions match actual system behavior
- Validate examples work as documented

## Agent Notes

Successfully created three comprehensive guides tailored to different user types. Each guide provides appropriate level of detail for its target audience.
