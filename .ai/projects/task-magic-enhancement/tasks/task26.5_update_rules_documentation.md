---
id: 26.5
title: "Update Task Magic Rules Documentation"
status: pending
priority: medium
feature: "Memory System Enhancement"
dependencies:
  - 26.2
  - 26.3
assigned_agent: null
created_at: "2025-06-06T22:09:56Z"
started_at: null
completed_at: null
error_log: null
---

## Description

Update task-magic/memory.mdc and related rules to document the new hierarchical memory structure and processes.

## Details

- Update `.cursor/rules/task-magic/memory.mdc` to document:
  - New hierarchical memory structure
  - Project-specific memory archival process
  - Global memory aggregation system
  - How to navigate between project and global memories
- Update related task magic rules that reference memory:
  - task-magic/tasks.mdc (archival process changes)
  - Any other rules that reference the memory system
- Document best practices for:
  - When to use project vs global memory
  - How to write effective project memory summaries
  - Memory aggregation guidelines
- Create examples and templates for memory documentation
- Update rule interconnections to reflect new memory hierarchy
- Ensure documentation is clear for both AI agents and human users

## Test Strategy

- Review updated documentation for completeness and clarity
- Verify all memory processes are properly documented
- Test that examples and templates are useful and accurate
- Confirm rule interconnections are correct
- Validate documentation covers both AI and human use cases
