# Create Pull Request

## Overview

Create a well-structured pull request using GitHub CLI with proper description, avoiding shell parsing issues that can occur with complex markdown in command-line arguments.

## Steps

1. **Prepare branch**

   - Ensure all changes are committed and pushed
   - Verify branch is up to date with main/base branch
   - Check that tests are passing locally

2. **Use simple title and description for CLI**

   - Keep PR title concise and descriptive
   - Use simple description without backticks or complex formatting
   - Avoid special characters that confuse shell parsing

3. **Create PR with basic info**

   ```bash
   gh pr create --title "feat: brief description" --body "Simple description without complex formatting"
   ```

4. **Enhance PR description via web interface**
   - Open PR in GitHub web interface
   - Add detailed markdown formatting safely
   - Include code blocks, tables, and complex formatting
   - Add screenshots, links, and rich content

## Common Shell Parsing Issues to Avoid

- **Backticks** (`) in descriptions - shell interprets as command substitution
- **Parentheses** in long strings - can cause parsing errors
- **Very long command lines** - exceed shell limits
- **Nested quotes** - confuse shell quote parsing
- **Special characters** like `$`, `&`, `|` in descriptions

## PR Creation Checklist

- [ ] Branch pushed to remote
- [ ] Simple, clear title chosen
- [ ] Basic description prepared (no backticks/complex formatting)
- [ ] PR created successfully with `gh pr create`
- [ ] Enhanced description added via web interface
- [ ] Appropriate reviewers assigned
- [ ] Labels and milestone added if needed
- [ ] Related issues linked

## Alternative Approach for Complex Descriptions

If you need to include complex formatting immediately:

1. **Create description file**

   ```bash
   cat > /tmp/pr-description.md << 'EOF'
   ## Your complex markdown here
   - With `code blocks`
   - And special characters
   EOF
   ```

2. **Use file for body**
   ```bash
   gh pr create --title "Your title" --body-file /tmp/pr-description.md
   ```

This avoids all shell parsing issues while allowing rich formatting.
