# Plan: Enhance Plan Mode with git worktree and date tracking

## Overview

This command enhances Cursor's Plan Mode workflow by adding git worktree isolation and automatic date tracking. Use this command when you're already in Plan Mode and want to set up an isolated development environment with proper date tracking in the plan document.

## How This Works with Plan Mode

1. **You invoke** Plan Mode (e.g., Cmd+Shift+P → "Plan")
2. **You type** `/plan` in the Plan Mode chat
3. **This command** sets up worktree + adds date tracking frontmatter
4. **Plan Mode** creates the actual plan structure and tasks
5. **You work** in Plan Mode's interactive editor as usual
6. **Everything happens** in the isolated worktree (if you chose to create one)

## Prerequisites

- You should already be in Cursor's Plan Mode
- A plan document should be open or about to be created
- You have a clear feature/project name for branch naming

## Steps

### 1. **Ask about git worktree**

Ask the user: **"Would you like to create a git worktree for this planning work? (yes/no)"**

**If yes:**

- Get or suggest a descriptive branch name based on the plan (e.g., `plan/feature-name`)
- Create the worktree:

```bash
git worktree add worktrees/{branch-name} -b {branch-name}
```

- Inform the user: "Created worktree at `worktrees/{branch-name}/`. All file operations will use this worktree."
- Note: The worktree has its own working directory separate from the main branch

**If no:**

- Continue with the main working directory

### 2. **Get current date**

Capture the current date in ISO 8601 format:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

Store this timestamp for the plan frontmatter.

### 3. **Add date tracking frontmatter**

If the plan document is being created or doesn't have frontmatter yet, add YAML frontmatter with date tracking:

**Frontmatter structure:**

```yaml
---
date_created: "2025-10-09T14:30:00Z"
date_completed: null
title: "{Plan Title}"
status: "in_progress"
---
```

**Notes:**

- Add this at the very top of the plan document
- Plan Mode will handle the actual plan structure and content
- The frontmatter is just for lifecycle tracking

### 4. **Continue with Plan Mode**

- Let Plan Mode handle the plan creation and structure
- The user can now work in the Plan Mode interface as usual
- All work happens in the isolated worktree (if created)

### 5. **Completion workflow**

When the user indicates the plan is complete or they're ready to implement:

- Get the current date:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

- Update the frontmatter:
  - Set `date_completed` to the current timestamp
  - Update `status` to `"completed"` or `"ready"` as appropriate

**If using a worktree:**

Remind the user about next steps:

```bash
# When ready to merge and remove the worktree:
# 1. Commit your changes
git add .
git commit -m "Add plan for {feature-name}"

# 2. Switch back to main branch
cd /Users/michaelhood/git/mastermind

# 3. Merge the branch (if desired)
git merge {branch-name}

# 4. Remove the worktree
git worktree remove worktrees/{branch-name}
```

### 6. **Summary**

Provide the user with:

- Confirmation of worktree location (if created)
- Path to the plan file with frontmatter
- Reminder that they can continue using Plan Mode normally
- Next steps for implementation or worktree management

## Checklist

- [ ] User preference for git worktree captured
- [ ] Git worktree created if requested (under `worktrees/`)
- [ ] Current date captured using bash `date` command
- [ ] YAML frontmatter added to plan with `date_created` and `date_completed`
- [ ] User informed they can continue with Plan Mode
- [ ] Date tracking updated when plan is completed
- [ ] User reminded about worktree cleanup (if applicable)

## Common Pitfalls

- **Don't forget to ask about worktree**: This should be the first question after understanding the plan context
- **Always use bash for dates**: Use `date -u +"%Y-%m-%dT%H:%M:%SZ"` for consistent ISO 8601 format
- **Don't skip frontmatter**: Date tracking via frontmatter is required, even though Plan Mode handles structure
- **Worktree path awareness**: If using a worktree, all file operations should target the worktree directory
- **Update date_completed**: Capture the completion timestamp when the plan is finalized
- **Let Plan Mode do its job**: Don't try to create the plan structure manually; just add frontmatter and let Plan Mode handle the rest

## Example Frontmatter

**When starting a plan:**

```yaml
---
date_created: "2025-10-09T14:30:00Z"
date_completed: null
title: "HCP Matching V2 Implementation"
status: "draft"
---
```

**When completing a plan:**

```yaml
---
date_created: "2025-10-09T14:30:00Z"
date_completed: "2025-10-15T09:45:00Z"
title: "HCP Matching V2 Implementation"
status: "completed"
---
```

## Notes

- This command is designed to **enhance** Cursor's Plan Mode, not replace it
- The core enhancements are: git worktree isolation + automatic date tracking
- Plan Mode handles the actual plan structure, tasks, and implementation details
- This command just sets up the environment and adds lifecycle metadata
- The worktree feature allows isolated planning and implementation without affecting the main branch
- Date tracking enables project timeline analysis and planning velocity metrics

## Example Workflow

**Typical usage:**

1. Open Cursor's Plan Mode (Cmd+Shift+P → "Plan")
2. In Plan Mode chat, type: `/plan`
3. Agent asks: "Would you like to create a git worktree for this planning work?"
4. You answer: "yes"
5. Agent creates `worktrees/plan/my-feature/` and switches to it
6. Agent captures current date and adds frontmatter to the plan
7. You continue working in Plan Mode, creating tasks and implementation steps
8. When done, agent updates `date_completed` in frontmatter
9. You commit, merge, and clean up the worktree

**Result:** You get an isolated development environment with proper date tracking, and Plan Mode handles all the planning structure for you.
