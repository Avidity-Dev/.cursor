---
id: 25
title: "Consolidate Legacy System Guidance"
status: completed
priority: high
feature: Task Magic Enhancement
dependencies:
  - 9
  - 10
  - 11
assigned_agent: null
created_at: "2025-06-06T21:06:08Z"
started_at: "2025-06-06T21:08:32Z"
completed_at: "2025-06-06T21:18:16Z"
error_log: null
---

## Description

Create a single comprehensive rule consolidating all legacy task magic guidance, keeping tasks.mdc and plans.mdc focused on the new enhanced system

## Details

- Review current tasks.mdc and plans.mdc files to identify all legacy system guidance
- Extract all sections that refer to the old .ai/tasks/ and .ai/plans/ structure (non-project-scoped)
- Create a new rule file (e.g., legacy.mdc or task-magic-legacy.mdc) in .cursor/rules/task-magic/
- Move all legacy guidance to this consolidated rule with clear section headers
- Update tasks.mdc and plans.mdc to remove legacy guidance and focus purely on the new project-scoped system
- Ensure the new legacy rule is properly documented with:
  - Clear introduction explaining this is for legacy compatibility
  - Table of contents for easy navigation
  - Proper section organization
  - Notes about when to use legacy vs new system
- Update any cross-references between the rules appropriately
- Add the new rule to the agent_requestable_workspace_rules list in the system

## Test Strategy

- Verify tasks.mdc and plans.mdc only contain new system guidance after cleanup
- Ensure the new legacy rule contains comprehensive guidance for the old system
- Test that the rule can be fetched and accessed properly via the rule system
- Confirm all cross-references between rules are working correctly
- Validate that both new and legacy workflows are properly documented and accessible

## Agent Notes

✅ **Task Completed Successfully**

**Created Migration-Focused Legacy Rule:**

- Created `.cursor/rules/task-magic/legacy.mdc` (10KB, 381 lines)
- Focused entirely on upgrading from legacy to enhanced system
- Provides comprehensive migration guidance, detection, and troubleshooting
- Includes migration scripts and step-by-step processes

**Cleaned Up Core Rules:**

- **tasks.mdc**: Removed all legacy structure references and backwards compatibility sections
- **plan.mdc**: Removed all legacy structure references and backwards compatibility sections
- Both rules now focus purely on the new project-scoped system

**Key Benefits Achieved:**

- Clear separation between new and legacy system guidance
- Migration path is well-documented for users upgrading
- Core rules are cleaner and focused on enhanced system
- Legacy users have comprehensive upgrade guidance available

**Files Modified:**

- `.cursor/rules/task-magic/legacy.mdc` (created)
- `.cursor/rules/task-magic/tasks.mdc` (cleaned up)
- `.cursor/rules/task-magic/plan.mdc` (cleaned up)

The legacy rule can be referenced as `task-magic/legacy` and provides complete guidance for migrating from the old `.ai/tasks/` and `.ai/plans/` structure to the new `.ai/projects/{project}/` structure.

**Follow-up Tasks Created:**

- Task 25.1: Update Documentation for Legacy Rule (Post-completion scope addition)
