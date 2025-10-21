---
allowed-tools: mcp__Parallel__get_tasks, mcp__Parallel__search_tasks, mcp__Parallel__update_task_status, mcp__Parallel__create_task, mcp__Parallel__list_projects, Read, Glob
description: Review and process captured inbox items interactively
---

# Inbox Review: Process Captured Ideas

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Inbox project ID: 262 (Inbox System)

## Task: Review Inbox Items

Interactive review of all unprocessed inbox items to convert them into actionable tasks or archive them.

### Process

1. **Get all inbox items** using `mcp__Parallel__get_tasks`:
   - Project ID: 262 (Inbox System)  
   - Filter for status: "pending" (or tasks containing "INBOX ITEM" in description)
   - Include descriptions to show previews

2. **Display each item** with:
   - Task ID and title
   - Age (days since creation)
   - First line preview
   - Extracted tags (if any)
   - Current priority/urgency

3. **For each item, provide options**:
   ```
   Item #1234: Add WebDAV sync support (3 days ago) #feature
   Preview: "Add support for WebDAV synchronization to enable server-side..."
   
   Options:
   [c] Convert to task (assign to project)
   [a] Archive (not actionable)
   [d] Defer (snooze for later)
   [v] View full content
   [e] Edit (open file)
   [s] Skip (leave in inbox)
   [q] Quit review
   
   Choice: _
   ```

4. **Handle each choice**:

   **Convert (c)**:
   - Show list of active projects
   - Prompt for project selection
   - Create new task in selected project
   - Update original inbox task as "completed" with reference
   - Link inbox file to new task

   **Archive (a)**:
   - Update status to "completed" 
   - Add note: "Archived - not actionable"
   - Update inbox file with archived status

   **Defer (d)**:
   - Prompt for defer period (1 day, 1 week, 1 month)
   - Add reminder note for future review
   - Keep status as pending

   **View (v)**:
   - Read and display full inbox file content
   - Return to options menu

   **Edit (e)**:
   - Open file for editing (show path)
   - Pause for user to make changes
   - Continue with options

5. **Show progress** throughout:
   ```
   📊 Inbox Review Progress
   
   ✅ Processed: 3 items
   📋 Remaining: 7 items  
   🎯 Converted to tasks: 2
   🗃️  Archived: 1
   ⏰ Deferred: 0
   ```

6. **Final summary**:
   ```
   🎉 Inbox Review Complete!
   
   📈 Session Results:
   - Items processed: 10
   - Converted to tasks: 7  
   - Archived: 2
   - Deferred: 1
   - Remaining: 0
   
   Next review suggested: {date based on frequency}
   ```

### Advanced Features

**Bulk Operations**:
- Option to select multiple items for same action
- Smart suggestions based on content analysis
- Show related items (similar tags/content)

**Filtering Options**:
- Review only items older than X days
- Review only items with specific tags
- Review by urgency level

**Smart Suggestions**:
- Suggest likely project based on content
- Flag potential duplicates
- Highlight high-value items for priority processing

### Error Handling

- Handle missing inbox files gracefully  
- Recovery if project assignments fail
- Undo recent actions if needed
- Graceful exit on user interrupt

### Usage Tips

Display these tips before starting review:

```
💡 Inbox Review Tips:

🚀 Speed up processing:
- Use 'c' for clearly actionable items
- Use 'a' for ideas that aren't worth pursuing
- Use 'v' only when preview isn't clear

🎯 Project assignment:
- Think about who would work on this
- Consider which codebase it affects  
- Choose active projects over pending ones

⚡ Batch similar items:
- Group related ideas when possible
- Convert similar bugs to same project
- Archive outdated duplicate ideas
```

Begin the inbox review process now.