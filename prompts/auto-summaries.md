# Strategies for Generating Code Change Summaries

## Original Query
I'd like to create a prompt (that will go in the prompts folder) to generate a summary of what I did recently. My strategy at the moment is to use git diff to see what changes have been made since the last commit, and have you summarize that and put the summary into a file. Can you think of any other strategies? They would have to give you knowledge of what was done recently to my code.

## Suggested Strategies

### 1. Leverage `git log` with Patch Option
Use `git log` with the `-p` flag to include diffs in the commit logs. You can then parse this output for summaries.

```bash
git log -1 -p > prompts/recent_changes_summary.txt
```

### 2. Use `git log` with Custom Formatting
Customize the `git log` output to include only relevant information, making it easier to generate summaries.

```bash
git log -1 --pretty=format:"%h - %an, %ar : %s" > prompts/recent_changes_summary.txt
```

### 3. Automate with Git Hooks
Set up a post-commit hook to automatically generate a summary after each commit.

```bash
# .git/hooks/post-commit
#!/bin/sh
git show --stat HEAD > ../prompts/recent_changes_summary.txt
```

Make it executable:

```bash
chmod +x .git/hooks/post-commit
```

### 4. Integrate with Continuous Integration (CI)
Use CI tools like GitHub Actions to generate and store summaries on each push.

```yaml
# .github/workflows/summary.yml
name: Generate Change Summary

on:
  push:
    branches:
      - main

jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Summary
        run: git log -1 --pretty=format:"%h - %an: %s" > prompts/recent_changes_summary.txt
      - name: Upload Summary
        uses: actions/upload-artifact@v2
        with:
          name: change-summary
          path: prompts/recent_changes_summary.txt
```

### 5. Use GitHub/GitLab APIs
Fetch recent commits using APIs and generate summaries programmatically.

```python
# summary_generator.py
import requests

repo = "username/repo"
token = "your_token"
url = f"https://api.github.com/repos/{repo}/commits"

headers = {"Authorization": f"token {token}"}
response = requests.get(url, headers=headers)
commits = response.json()

with open('prompts/recent_changes_summary.txt', 'w') as f:
    for commit in commits[:1]:
        message = commit['commit']['message']
        f.write(f"{commit['sha'][:7]} - {message}\n")
```

Run the script:

```bash
python summary_generator.py
```

### 6. Adopt Conventional Commits
Structure your commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification. This makes it easier to parse and generate meaningful summaries.

```bash
git commit -m "feat(auth): add JWT authentication"
git commit -m "fix(ui): resolve button alignment issue"
```

You can then use tools like `commitlint` or `semantic-release` to automate summary generation based on these messages.
