---
allowed-tools: mcp__Linear__create_issue
description: Create a Linear issue in the AI & Advanced Analytics team
---

# Create Linear Issue

## Context

- Team: AI & Advanced Analytics
- Guidelines: See `.cursor/rules/mcp_usage/linear-mcp-usage.mdc`
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`

## Task: Create Linear Issue

Create a well-structured issue in the AI & Advanced Analytics team following Linear best practices.

### Input

Issue details: `$ARGUMENTS`

### Process

1. **Parse the input** to determine:

   - Title (clear, action-oriented summary)
   - Description (detailed context and requirements)
   - Priority (0=None, 1=Urgent, 2=High, 3=Normal, 4=Low)
   - Labels (if mentioned)

2. **Create the issue** with:

   - **Team**: "AI & Advanced Analytics" (required)
   - **Title**: Clear, concise summary of the work
   - **Description**: Include:
     - Context and background
     - Specific requirements
     - Acceptance criteria
     - Any relevant technical details
   - **Priority**: Only set if explicitly mentioned
   - **Labels**: Apply relevant labels if specified

3. **Confirm creation** by showing:
   - Issue number and URL
   - Title created
   - Status and priority (if set)

### Examples

Input: `Add support for batch processing in data pipeline`
→ Creates: Issue in AI & Advanced Analytics team with clear title and description

Input: `Fix memory leak in model training workflow - HIGH PRIORITY`
→ Creates: High priority issue with detailed description

Input: `Research alternative vector database options for similarity search #research`
→ Creates: Issue with research label

Execute the issue creation now based on the provided description.
