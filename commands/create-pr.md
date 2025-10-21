# Create Pull Request

## Overview

Create a well-structured pull request using GitHub CLI with proper description, avoiding shell parsing issues that can occur with complex markdown in command-line arguments.

**For PR content and writing guidelines, see:** [pr-writing-guidelines.mdc](mdc:.cursor/rules/general/pr-writing-guidelines.mdc)

## Recommended Workflow

### 1. Prepare Branch

- Ensure all changes are committed and pushed
- Verify branch is up to date with base branch
- Check that tests are passing locally

### 2. Write PR Description (recommended)

Write your PR description in a file following the [PR writing guidelines](mdc:.cursor/rules/general/pr-writing-guidelines.mdc):

```bash
# Create description file in docs/plans/ for documentation
cat > docs/plans/PR<number>_<brief_name>.md << 'EOF'
## Overview
Brief paragraph...

## Changes
...

## Rationale
...

## Breaking Changes
None.
EOF
```

**Note:** The file should start with `## Overview`, not a title. The title is passed separately via `--title` flag.

Benefits:

- Avoids all shell parsing issues
- Allows rich markdown formatting
- Documents PR for future reference
- Can be reviewed and edited before creating PR

### 3. Create PR with Description File

```bash
gh pr create \
  --base main \
  --title "Brief descriptive title" \
  --body-file docs/plans/PR<number>_<brief_name>.md
```

### 4. Verify and Adjust

- Review PR in GitHub web interface
- Make any final adjustments to description
- Assign reviewers, add labels
- Link related issues

## Alternative: Simple PR Creation

For simple PRs where a file isn't needed:

```bash
gh pr create \
  --base main \
  --title "Brief title" \
  --body "Simple single-line description"
```

Then enhance via web interface if needed.

## Common Shell Parsing Issues to Avoid

- **Backticks** (`) in descriptions - shell interprets as command substitution
- **Parentheses** in long strings - can cause parsing errors
- **Very long command lines** - exceed shell limits
- **Nested quotes** - confuse shell quote parsing
- **Special characters** like `$`, `&`, `|` in descriptions

## PR Creation Checklist

**Before creating:**

- [ ] All changes committed and pushed to remote
- [ ] Tests passing locally
- [ ] PR description written (following [guidelines](mdc:.cursor/rules/general/pr-writing-guidelines.mdc))

**When creating:**

- [ ] Clear, specific title chosen
- [ ] Correct base branch specified
- [ ] Description file created in `docs/plans/` (for complex PRs)
- [ ] PR created successfully with `gh pr create --body-file`

**After creating:**

- [ ] PR reviewed in web interface
- [ ] Reviewers assigned
- [ ] Labels added
- [ ] Related issues linked
- [ ] Milestone set (if applicable)

## Quick Reference

**Create PR with file:**

```bash
gh pr create --base main --title "Title" --body-file docs/plans/PR123_feature.md
```

**Create simple PR:**

```bash
gh pr create --base main --title "Title" --body "Simple description"
```

**Update PR description:**

```bash
gh pr edit 123 --body-file docs/plans/PR123_feature.md
```

**Change base branch:**

```bash
gh pr edit 123 --base main
```
