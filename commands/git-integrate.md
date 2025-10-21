---
allowed-tools: Bash, Read, Grep, TodoWrite, LS
description: Integrate a feature branch from worktree into main repository
---

# Git Feature Branch Integration

## Current Context
- Main repo status: !`cd /Users/michaelhood/git/parallel && git status --short | head -10`
- Active worktrees: !`cd /Users/michaelhood/git/parallel && git worktree list`
- Current branch: !`cd /Users/michaelhood/git/parallel && git branch --show-current`
- Pending migrations: !`ls -la /Users/michaelhood/git/parallel/worktrees/*/src/parallel_db/migrations/*.sql 2>/dev/null | grep -v "No such" | tail -5 || echo "None found"`

## Task: Integrate Feature Branch from Worktree

Automate the integration of a feature branch from a worktree into the main branch.

### Input
Branch or worktree to integrate: `$ARGUMENTS`

If no argument provided, list available worktrees and ask which to integrate.

### Process

1. **Identify the feature branch**:
   - Parse `$ARGUMENTS` to find branch name or worktree path
   - If empty, list worktrees with `git worktree list` and prompt for selection
   - Extract branch name from worktree info

2. **Pre-flight checks**:
   ```bash
   # Check worktree status
   cd /Users/michaelhood/git/parallel/worktrees/[branch-name]
   git status

   # Ensure no uncommitted changes
   # Check for migration files
   ls src/parallel_db/migrations/*.sql

   # Check main repo status
   cd /Users/michaelhood/git/parallel
   git status
   ```

3. **Prepare main repository**:
   - If uncommitted changes exist in main:
     - Show the changes with `git diff --stat`
     - Options:
       a. Stash changes: `git stash push -m "Pre-integration stash"`
       b. Commit changes: `git add -A && git commit -m "WIP: Pre-integration commit"`
       c. Abort if changes conflict with feature branch

4. **Fetch and merge the feature branch**:
   ```bash
   cd /Users/michaelhood/git/parallel
   git fetch origin
   git checkout main
   git merge feature/[branch-name] --no-ff -m "Merge feature branch: [branch-name]"
   ```

5. **Apply database migrations** (if any):
   - Check for new migration files in `src/parallel_db/migrations/`
   - For each new migration:
     ```bash
     psql -h localhost -U michaelhood -d parallel_db < src/parallel_db/migrations/[migration].sql
     ```
   - Record which migrations were applied

6. **Run verification tests**:
   ```bash
   # Run Python tests
   python -m pytest tests/ -v --tb=short

   # Test MCP server starts
   timeout 5 python -m parallel_mcp || echo "Server started successfully"
   ```

7. **Push to remote** (after confirmation):
   ```bash
   git push origin main
   ```

8. **Clean up**:
   - Remove the worktree:
     ```bash
     git worktree remove worktrees/[branch-name]
     ```
   - Delete the local feature branch:
     ```bash
     git branch -d feature/[branch-name]
     ```
   - Delete remote feature branch (optional):
     ```bash
     git push origin --delete feature/[branch-name]
     ```
   - If stashed, remind to pop stash:
     ```bash
     git stash pop
     ```

### Safety Features

1. **Create backup tag** before merge:
   ```bash
   git tag -a "pre-merge-[branch-name]-$(date +%Y%m%d)" -m "Backup before merging [branch-name]"
   ```

2. **Rollback instructions** if something goes wrong:
   - Reset to backup tag
   - Restore database from backup
   - Re-create worktree if needed

3. **Confirmations required** for:
   - Handling uncommitted changes
   - Applying migrations
   - Pushing to remote
   - Deleting branches

### Usage Examples
- `/git:integrate project-status-automation` - Integrate specific branch
- `/git:integrate worktrees/project-status-automation` - Integrate by worktree path
- `/git:integrate` - Interactive mode, choose from list

### Output Format
Show progress with clear status messages:
- ✅ Step completed successfully
- ⚠️ Warning or decision needed
- ❌ Error occurred
- 🔄 In progress

### Post-Integration Checklist
After successful integration:
1. Update project status in Parallel database
2. Create release notes if applicable
3. Notify team members if collaborative project
4. Update documentation if APIs changed

Execute the integration process now based on the provided input.
