---
allowed-tools: mcp__Parallel__get_tasks, mcp__Parallel__get_project_completion_stats, Bash, Glob
description: Analytics and statistics for inbox capture and processing patterns
---

# Inbox Stats: Analytics Dashboard

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Inbox project ID: 262 (Inbox System)

## Task: Generate Inbox Statistics

Provide comprehensive analytics about idea capture and processing patterns.

### Process

1. **Get inbox task data**:
   - Use `mcp__Parallel__get_tasks` for project 262
   - Include all statuses and creation dates
   - Get task completion statistics

2. **Analyze file system data**:
   - Count files in `~/Documents/Brain5/Journal/dev/inbox/` folders
   - Calculate file creation patterns by date
   - Identify orphaned files (files without database entries)

3. **Calculate key metrics**:

   **Capture Metrics**:
   - Total items captured (all time)
   - Items captured last 7 days
   - Items captured last 30 days
   - Average items per day/week
   - Peak capture times/days

   **Processing Metrics**:
   - Items processed vs. captured
   - Average time from capture to processing
   - Processing completion rate
   - Items aging (> 1 week, > 1 month unprocessed)

   **Content Analysis**:
   - Most common tags
   - Most common urgency levels
   - Average idea length (words)
   - Source distribution (command, voice, etc.)

4. **Display dashboard**:
   ```
   📊 INBOX SYSTEM ANALYTICS
   =========================================
   
   📈 CAPTURE STATISTICS
   • Total items captured: {total}
   • Last 7 days: {week} ({avg}/day avg)
   • Last 30 days: {month} ({avg}/week avg)
   • Peak day: {date} ({count} items)
   
   ⚡ PROCESSING HEALTH  
   • Processing rate: {processed}/{total} ({percentage}%)
   • Average processing time: {avg_days} days
   • Items aging > 1 week: {aging_week}
   • Items aging > 1 month: {aging_month}
   
   🏷️  TOP TAGS (last 30 days)
   1. #{tag1}: {count1} items
   2. #{tag2}: {count2} items  
   3. #{tag3}: {count3} items
   
   🎯 URGENCY BREAKDOWN
   • Critical: {critical} ({critical_pct}%)
   • High: {high} ({high_pct}%)
   • Normal: {normal} ({normal_pct}%)
   • Low: {low} ({low_pct}%)
   
   📱 CAPTURE SOURCES
   • Claude command: {cmd} ({cmd_pct}%)
   • Voice transcription: {voice} ({voice_pct}%)
   • Screenshots: {screenshot} ({screenshot_pct}%)
   ```

5. **Provide insights and recommendations**:
   ```
   💡 INSIGHTS & RECOMMENDATIONS
   
   🎯 Processing Health: {health_status}
   {health_advice}
   
   📅 Optimal Review Schedule:  
   Based on your {avg_items}/week capture rate, 
   recommend reviewing every {recommended_days} days.
   
   🏷️  Tag Hygiene:
   Consider consolidating: {suggested_merges}
   Most valuable tags: {top_value_tags}
   
   ⚡ Next Actions:
   • {action1}
   • {action2}  
   • {action3}
   ```

### Advanced Analytics

**Trend Analysis**:
- Capture trends over time (increasing/decreasing)
- Seasonal patterns (days of week, times of day)
- Correlation between capture and processing

**Quality Metrics**:
- Conversion rate to actionable tasks
- Ideas that led to completed work
- Time from idea to implementation

**Predictive Insights**:
- Forecast processing time needed
- Identify ideas likely to become stale
- Suggest optimal review timing

### Health Indicators

**Green (Healthy)**:
- Processing rate > 80%
- Average processing time < 1 week
- Aging items < 10%

**Yellow (Needs Attention)**:
- Processing rate 60-80%
- Average processing time 1-2 weeks
- Aging items 10-20%

**Red (Action Required)**:
- Processing rate < 60%
- Average processing time > 2 weeks  
- Aging items > 20%

### Detailed Breakdowns

If user requests more details, provide:

**Daily Activity**:
```
📅 DAILY BREAKDOWN (Last 14 days)
Sep 03: ████████ 8 items (2 processed)
Sep 02: ██████ 6 items (4 processed)
Sep 01: ████ 4 items (3 processed)
...
```

**Tag Analysis**:
```
🏷️  TAG DEEP DIVE
#feature: 15 items (avg processing: 3.2 days)
#bug: 12 items (avg processing: 1.8 days)  
#urgent: 8 items (avg processing: 0.9 days)
...
```

**Aging Report**:
```
⏰ AGING ITEMS REPORT
🚨 Critical (>30 days): 2 items
⚠️  Warning (>14 days): 5 items  
👀 Watch (>7 days): 8 items
```

### Export Options

Offer to export data:
- CSV format for spreadsheet analysis
- JSON format for programmatic use
- Markdown report for documentation

Execute the statistics analysis now.