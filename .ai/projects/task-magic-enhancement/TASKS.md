# Project Tasks

## Completed Tasks (Archived to Memory)

_Tasks 1-13 have been completed and archived to global memory. See `.ai/memory/TASKS_LOG.md` for details._

## Active Tasks

- [ ] **ID 14: Create Context Management Rule** (Priority: medium)

  > Create new context.mdc rule for managing context folders

- [ ] **ID 15: Update README for Rules** (Priority: medium)

  > Dependencies: 9, 10, 11, 12
  > Update task-magic README to clarify it describes rules

- [ ] **ID 16: Create Shared Templates** (Priority: medium)

  > Create reusable templates in shared/templates/

- [ ] **ID 17: Create Shared Workflows** (Priority: medium)

  > Document standard workflows in shared/workflows/

- [ ] **ID 18: Add Metadata Headers** (Priority: low)

  > Dependencies: 1, 2, 3, 4, 5, 6, 7, 8
  > Add YAML frontmatter to all created files

- [ ] **ID 19: Create Migration Guide** (Priority: high)

  > Dependencies: 9, 10, 11, 12, 13, 14
  > Document how to migrate existing .ai/ structure

- [ ] **ID 20: Test Multi-Project Support** (Priority: high)

  > Dependencies: 9, 10, 13
  > Create a second test project to verify isolation

- [ ] **ID 21: Update Handoff Rules** (Priority: medium)

  > Update handoff.mdc for project-scoped handoffs

- [ ] **ID 22: Create Integration Tests** (Priority: medium)

  > Dependencies: 20
  > Test cross-project operations and tool compatibility

- [ ] **ID 23: Create User Documentation** (Priority: medium)

  > Dependencies: 19, 20
  > Create comprehensive user guide for enhanced system

- [ ] **ID 24: Archive Original Proposal** (Priority: low)

  > Dependencies: 11
  > Test archival system with completed planning docs

- [x] **ID 25: Consolidate Legacy System Guidance** (Priority: high)

  > Dependencies: 9, 10, 11
  > Create a single comprehensive rule consolidating all legacy task magic guidance, keeping tasks.mdc and plans.mdc focused on the new enhanced system

- [ ] **ID 25.1: Update Documentation for Legacy Rule** (Priority: medium) _[Follow-up]_

  > Dependencies: 25
  > Update README and index to properly explain rule dispatcher role and legacy detection

- [ ] **ID 26: Implement Hierarchical Project Memory System** (Priority: high) _[Parent Task - Expanded]_

  > Dependencies: 26.6
  > Parent task for implementing hierarchical memory system. Complete when all sub-tasks are finished.

- [ ] **ID 26.1: Create Project Memory Directory Structure** (Priority: critical)

  > Create the basic memory directory structure for the task-magic-enhancement project with tasks/ subdirectory and initial MEMORY.md template

- [ ] **ID 26.2: Update Task Archival Process for Project Memory** (Priority: high)

  > Dependencies: 26.1
  > Modify the task archival logic to archive tasks to project-specific memory location instead of global memory

- [ ] **ID 26.3: Implement Global Memory Aggregation System** (Priority: high)

  > Dependencies: 26.1
  > Create GLOBAL_MEMORY.md and implement logic to aggregate insights from all project memory files

- [ ] **ID 26.4: Enhance INDEX.md with Memory References** (Priority: medium)

  > Dependencies: 26.1, 26.3
  > Update the existing INDEX.md to include references to project memory files and summaries

- [ ] **ID 26.5: Update Task Magic Rules Documentation** (Priority: medium)

  > Dependencies: 26.2, 26.3
  > Update task-magic/memory.mdc and related rules to document the new hierarchical memory structure and processes

- [ ] **ID 26.6: Test Hierarchical Memory System** (Priority: high)

  > Dependencies: 26.2, 26.3, 26.4, 26.5
  > Create sample archived tasks, test archival flows, verify aggregation works, and validate backwards compatibility
