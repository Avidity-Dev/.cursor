---
allowed-tools: Read, Write
description: Toggle automatic task creation for work requests
---

# Auto Task Creation Toggle

## Current Settings
- CLAUDE.md location: !`test -f CLAUDE.md && echo "Project" || echo "Not found"`
- Current auto-task setting: !`grep -q "AUTO_CREATE_TASKS" CLAUDE.md 2>/dev/null && grep "AUTO_CREATE_TASKS" CLAUDE.md || echo "Not configured"`

## Task: Toggle Automatic Task Creation

Control whether I should automatically create tasks when you request work that doesn't have an existing task.

### Input
Command: `$ARGUMENTS` (options: on, off, status)

### Process

1. **Check current setting** in CLAUDE.md

2. **Based on the argument**:
   - `on` or no argument: Enable automatic task creation
   - `off`: Disable automatic task creation
   - `status`: Just show current setting

3. **Update CLAUDE.md** with the configuration:
   ```markdown
   ## Automatic Task Creation
   AUTO_CREATE_TASKS: [enabled/disabled]

   When enabled, I will:
   - Detect when work is requested without an existing task
   - Automatically create a pending task in the housekeeping project
   - Update task status as work progresses
   - Add detailed implementation notes when completed
   ```

4. **Confirm the change** by showing:
   - Previous setting
   - New setting
   - What this means for future work requests

### Behavior When Enabled

When AUTO_CREATE_TASKS is enabled, I will:
1. **Detect work requests** (vs questions) by looking for:
   - Imperative statements ("Create...", "Fix...", "Add...")
   - Request for changes to code/files
   - Implementation or modification tasks

2. **Create a task automatically**:
   - Project: housekeeping (unless context suggests otherwise)
   - Status: pending → in_progress → completed
   - Priority: Based on request urgency
   - Description: Detailed notes about implementation

3. **Track the work properly**:
   - Update status when starting
   - Add implementation details when done
   - Reference the task number in commits

### Usage Examples
- `/project:auto-task on` - Enable automatic task creation
- `/project:auto-task off` - Disable automatic task creation
- `/project:auto-task status` - Check current setting

Execute the requested action now.
