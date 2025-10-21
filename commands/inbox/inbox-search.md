---
allowed-tools: mcp__Parallel__search_tasks, mcp__Parallel__search_documents, Grep, Read, Glob
description: Search and filter inbox items by content, tags, dates, and status
---

# Inbox Search: Find Captured Ideas

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Inbox project ID: 262 (Inbox System)

## Task: Search Inbox Items

Search across all inbox items using various filters and criteria.

### Input
User query: `$ARGUMENTS`

### Search Types

1. **Full-text search**: Search content of all inbox items
2. **Tag search**: Find items with specific tags (#urgent, #feature, #bug)
3. **Mention search**: Find items with specific mentions (@research, @team)
4. **Date range**: Find items from specific time periods
5. **Status filter**: Filter by processing status
6. **Urgency filter**: Filter by priority/urgency level

### Process

1. **Parse search query** to identify:
   ```
   Query types:
   - Text: "memory leak" → full-text search
   - Tags: "#urgent" → tag filter
   - Mentions: "@research" → mention filter  
   - Dates: "last-week", "2025-09", "today" → date range
   - Status: "unprocessed", "archived" → status filter
   - Combined: "#urgent memory leak last-week" → multiple filters
   ```

2. **Search database first**:
   - Use `mcp__Parallel__search_tasks` for text content
   - Filter by project ID 262 (Inbox System)
   - Apply additional filters based on query type

3. **Search files if needed**:
   - Use Grep to search markdown files in `~/Documents/Brain5/Journal/dev/inbox/`
   - Pattern: Look for tags, content, metadata
   - Date-based folder filtering for performance

4. **Combine and deduplicate results**:
   - Merge database and file search results
   - Remove duplicates by task ID or file path
   - Sort by relevance and recency

5. **Display results**:
   ```
   🔍 Inbox Search Results for: "{query}"
   
   Found {count} items:
   
   📄 #{task_id} - {title} ({age} ago)
      Tags: {tags}
      Preview: "{first_line_preview}"
      File: inbox/2025/09/2025-09-03-142335-title.md
   
   📄 #{task_id} - {title} ({age} ago)
      Tags: {tags}
      Preview: "{first_line_preview}"
      File: inbox/2025/08/2025-08-15-091234-another.md
   
   Options:
   [v] View item #{id}
   [r] Review all found items
   [s] Search again
   [q] Quit
   ```

### Advanced Search Features

**Date Range Parsing**:
- `today` → items from today
- `yesterday` → items from yesterday  
- `last-week` → items from past 7 days
- `last-month` → items from past 30 days
- `2025-09` → items from September 2025
- `2025-09-03` → items from specific date

**Smart Query Processing**:
- Auto-extract tags and mentions
- Handle synonyms (urgent = high priority)
- Fuzzy matching for typos
- Context-aware search (current project, recent files)

**Result Filtering**:
- Sort by: date, relevance, urgency, tags
- Group by: tags, date, project converted to
- Highlight matching terms in previews

### Search Examples

**Input**: `memory leak`
→ Full-text search across all inbox content

**Input**: `#urgent`  
→ Find all items tagged as urgent

**Input**: `@research last-month`
→ Find research items from the past month

**Input**: `#bug authentication`
→ Find bugs related to authentication

**Input**: `unprocessed #feature`
→ Find unprocessed feature requests

### Performance Optimizations

- **File system optimization**: Search recent folders first
- **Database indexing**: Use task search efficiently  
- **Result limiting**: Show top 20 results, paginate rest
- **Caching**: Remember recent search results

### Usage Tips

```
💡 Search Tips:

🎯 Use specific tags:
- #bug, #feature, #urgent, #research
- @team, @ui, @backend, @mobile

📅 Date shortcuts:
- today, yesterday, last-week, last-month
- 2025-09 (month), 2025-09-03 (specific date)

🔗 Combine filters:
- "#urgent last-week" → urgent items from past week
- "#bug authentication" → auth-related bugs
- "@research unprocessed" → unprocessed research items

⚡ Quick actions:
- Use 'r' to review all search results
- Use 'v' to view individual items
```

Execute the search now based on the user's query.