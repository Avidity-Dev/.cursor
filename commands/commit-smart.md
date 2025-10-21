---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git recommit:*), Bash(git log:*)
description: Automatically commit changes in logical groups with smart analysis
---

# Smart Commit Grouping

## Current Repository State

- Git status: !`git status --porcelain`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Task

Analyze all changes in the repository and commit them in logical groups. Follow these steps:

1. **Analyze all changes** - Review the git status and diffs to understand what has changed

   **CRITICAL: Verify file operations before committing:**

   - Check for renames: `git status --porcelain | grep "^R"`
     - Renamed files show as `R  old_path -> new_path`
     - DO NOT say files were "deleted" - they were RENAMED
   - For modified files with >100 line deletions:
     - Run `git diff --cached <file> | head -50` to see actual changes
     - Check if file still has content: `wc -l <file>`
     - Understand if this is a refactor, deletion, or content move
     - DO NOT assume a file is deleted just because it has many deletions
     - Look for whether content was moved to other files

2. **Group files logically** by type:

   - Documentation (_.md, docs/_)
   - Tests (tests/_, \_\_test.py, test_\*.py)
   - Migrations (_/migrations/_, _migration_.sql, _migrate_.py)
   - Configuration (_.json, _.toml, _.yaml, _.yml, .\*)
   - Source code (src/\*)
   - Scripts (scripts/_, _.sh)
   - Other files

3. **For each group with changes**:

   - Stage the files in that group using `git add`
   - **Analyze the actual changes** - Run `git diff --cached --stat` AND review sample diffs
   - For files with significant changes, check `git diff --cached <file> | head -30`
   - Create a descriptive commit message following conventional commit format:
     - Use appropriate type: feat, fix, docs, test, chore, refactor
     - Include a concise but descriptive summary
     - Add details about what changed, including:
       - Number of files changed
       - Key modifications made
       - Lines added/removed
   - Commit using `git recommit` to handle pre-commit hook modifications automatically

4. **Commit message format**:

   ```
   <type>: <description>

   <detailed summary of changes>

   Files updated:
   - <key files list>
   ```

5. **Important**:
   - Skip empty groups (no files to commit)
   - Use `git recommit` instead of `git commit` to automatically handle pre-commit hook modifications
   - Provide feedback about each commit created
   - Show a summary at the end
   - **Be accurate in commit messages:**
     - Say "refactor" or "extract" when moving content between files, NOT "delete"
     - Say "rename" when files are renamed, NOT "delete and create"
     - Say "modify" or "update" when files have large deletions but still exist
     - Verify your descriptions match the actual git operations

Execute this task now, creating logical commits for all pending changes using `git recommit`.
