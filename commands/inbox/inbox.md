---
allowed-tools: mcp__Parallel__create_task, mcp__Parallel__get_project, Write, Bash
description: Frictionless idea capture system - capture any idea instantly without project assignment
---

# Inbox: Frictionless Idea Capture

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Working directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Inbox project ID: 262 (Inbox System)

## Task: Capture Idea in Inbox

You need to capture an idea, thought, or task without requiring immediate project assignment or categorization. This is zero-friction capture for later processing.

### Input
User provided: `$ARGUMENTS`

### Process

1. **Parse the input** to extract:
   - Main idea/content
   - Quick tags (words starting with #)
   - Mentions (words starting with @)
   - Urgency indicators (urgent, critical, important)

2. **Generate metadata**:
   - Unique ID: `inbox-{timestamp}` format
   - Timestamp: Current ISO 8601 timestamp
   - Slug: First 3-4 words, kebab-case, max 50 chars
   - File path: `~/Documents/Brain5/Journal/dev/inbox/{YEAR}/{MONTH}/{YYYY-MM-DD-HHMMSS-slug}.md`

3. **Create the inbox file** with this structure:
   ```yaml
   ---
   id: inbox-{timestamp}
   created: {ISO timestamp}
   tags: [extracted, tags, from, input]
   status: unprocessed
   urgency: {normal|high|critical}
   source: claude-command
   context:
     working_directory: {current pwd}
     git_branch: {current branch or null}
     active_file: null
   ---

   # {Title from first line or summary}

   {Main content from user input}

   ## Context
   Captured while working in: {working_directory}
   {Git branch info if available}

   ## Initial Thoughts
   {Any immediate thoughts or context}

   ## Next Steps
   - [ ] Review and assign to appropriate project
   - [ ] Add more details if needed
   - [ ] Convert to actionable task
   ```

4. **Create database entry** using `mcp__Parallel__create_task`:
   - Project ID: 262 (Inbox System)
   - Title: First line or summary of the idea
   - Description: Full content with context
   - Status: "pending" (since "inbox" status may not exist yet)
   - Priority: Based on urgency indicators
   - Add note in description that this is an "INBOX ITEM" for filtering

5. **Ensure directory exists**:
   - Create year and month folders if they don't exist
   - Use `mkdir -p` to create nested directories

6. **Handle edge cases**:
   - Very long input (truncate title, preserve full content)
   - Special characters in filename (sanitize slug)
   - Empty input (prompt for content)
   - File conflicts (add sequential number)

### Response Format

Provide a clear confirmation:

```
✅ Inbox item captured!

📄 File: ~/Documents/Brain5/Journal/dev/inbox/2025/09/2025-09-03-142335-webdav-sync.md
🆔 Task: #{task_id} in Inbox System
🏷️  Tags: feature, sync
⚡ Urgency: normal

Your idea is safely captured for later review. Use /inbox-review to process captured items.
```

### Examples

**Input**: `Add support for WebDAV sync`
→ Creates: Basic idea file with normal priority

**Input**: `#urgent Fix memory leak in background process`  
→ Creates: Bug report with high urgency, tagged as urgent

**Input**: `@research Explore WASM for performance gains - could be game changer`
→ Creates: Research idea with context preserved

**Input**: `#bug @ui Button alignment issue on mobile - submit button is cutoff on iPhone`
→ Creates: Bug report tagged with bug and ui, includes device context

### Implementation Notes

- **Atomic operations**: Create file first, then database entry, to avoid orphaned records
- **Context preservation**: Capture as much environmental context as possible
- **Error handling**: Graceful fallback if Brain5 folder doesn't exist
- **Filename safety**: Sanitize special characters, handle length limits
- **Timestamp precision**: Use milliseconds to avoid conflicts

Execute this inbox capture now based on the user's input.