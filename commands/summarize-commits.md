# Summarize Git Commits

## Overview

Generates a comprehensive summary of git commits from the past N days, showing what work was accomplished during that time period.

## Parameters

- **days** (required): Number of days to look back in commit history (e.g., 1, 2, 7, 30)

## Steps

1. **Retrieve commit history**

   First get a concise list of commits:

   ```bash
   git log --since="{days} days ago" --oneline --decorate
   ```

2. **Get detailed commit information**

   Then retrieve detailed stats with file changes:

   ```bash
   git log --since="{days} days ago" --stat --pretty=format:"%h - %s (%ar)" | cat
   ```

3. **Analyze and summarize the commits**

   Review the output and create a structured summary that includes:

   - **Major themes**: Identify overarching work areas (e.g., feature development, refactoring, bug fixes)
   - **Categorized accomplishments**: Group related commits together
   - **Impact metrics**: Count commits, lines changed, files affected
   - **Key deliverables**: Highlight completed features or major milestones
   - **Context**: Explain how changes fit together and their business impact

4. **Format the summary**

   Structure the summary with clear sections:

   - Overview paragraph
   - Major theme/focus area
   - Detailed breakdown by category
   - Impact metrics (commits, lines changed, files affected)
   - Key deliverables checklist

## Example Usage

**User request:** "Summarize my commits from the past 2 days"

- Replace `{days}` with `2`
- Run both git commands
- Analyze the output and provide a structured summary

**User request:** "What have I done this week?"

- Replace `{days}` with `7`
- Follow the same process

## Output Structure Template

```markdown
## Summary of Your Work (Past N Days)

[Brief overview paragraph]

### **Major Theme: [Primary Focus Area]**

#### **1. [Category Name]** (timeframe)

- [Accomplishment details]
- [Metrics: X files, Y lines]

#### **2. [Category Name]** (timeframe)

- [Accomplishment details]

### **Impact Metrics:**

- **X commits** [branch status if relevant]
- **~X lines** of new code/documentation added
- **~X lines** refactored/reorganized
- [Other relevant metrics]

### **Key Deliverables:**

✅ [Major achievement 1]
✅ [Major achievement 2]
✅ [Major achievement 3]

[Closing insight or context about the work]
```

## Checklist

- [ ] Retrieved concise commit list with `git log --oneline`
- [ ] Retrieved detailed stats with `git log --stat`
- [ ] Identified major themes and patterns in the commits
- [ ] Grouped related commits into logical categories
- [ ] Calculated impact metrics (commits, lines, files)
- [ ] Highlighted key deliverables and accomplishments
- [ ] Provided context about how changes fit together
- [ ] Used clear, structured formatting for readability

## Common Patterns to Look For

### Commit Message Prefixes

- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code restructuring
- `docs:` - Documentation updates
- `chore:` - Maintenance tasks
- `test:` - Testing updates
- `ci:` - CI/CD changes

### Thematic Grouping

- Infrastructure work (database, deployment, CI/CD)
- Feature development (new capabilities)
- Code quality (refactoring, standardization)
- Bug fixes and corrections
- Documentation and guides
- Testing and validation

### Impact Assessment

- Look for large file changes that indicate major refactoring
- Identify cross-cutting changes that affect multiple layers
- Note creation of new models, services, or infrastructure
- Recognize housekeeping and cleanup work

## Tips

- **Be comprehensive**: Capture all the work, not just the biggest commits
- **Show connections**: Explain how commits relate to each other
- **Provide context**: Help the user understand the business value
- **Use metrics**: Numbers help quantify the effort
- **Celebrate wins**: Acknowledge significant accomplishments
- **Note branch status**: Mention if commits are ahead/behind origin
