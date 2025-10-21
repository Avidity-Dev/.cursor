---
allowed-tools: mcp__Parallel__create_task, Write, Bash, Read
description: Capture visual ideas and bug reports with screenshot context
---

# Inbox Screenshot: Capture Visual Ideas

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Working directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Inbox project ID: 262 (Inbox System)

## Task: Capture Screenshot-Based Idea

Capture ideas that are based on visual content, UI issues, design concepts, or anything that requires visual context.

### Input
Description and context: `$ARGUMENTS`

### Process

1. **Parse screenshot input**:
   - Extract description of what the screenshot shows
   - Identify issue type (bug, feature, design, documentation)
   - Detect platform/browser context if mentioned
   - Look for visual problem indicators (alignment, color, sizing)

2. **Handle screenshot file**:
   - Look for recent screenshot files in common locations:
     - `~/Desktop/Screenshot*.png`
     - `~/Downloads/Screenshot*.png`
     - `/tmp/Screenshot*.png`
   - If found, copy to inbox folder with consistent naming
   - Generate relative path for markdown linking

3. **Generate visual-specific metadata**:
   - ID: `inbox-screenshot-{timestamp}`
   - Auto-tag with `#visual`, `#screenshot`
   - Add platform tags if detected (`#ios`, `#web`, `#desktop`)
   - Categorize by type (`#bug`, `#ui`, `#design`, `#feature`)

4. **Create visual inbox file**:
   ```yaml
   ---
   id: inbox-screenshot-{timestamp}
   created: {ISO timestamp}
   tags: [visual, screenshot, detected, tags]
   status: unprocessed
   urgency: {normal|high based on bug severity}
   source: screenshot-capture
   visual_context:
     screenshot_file: {filename if found}
     platform: {web|mobile|desktop|unknown}
     browser: {detected from description}
     device: {detected device type}
     issue_type: {bug|feature|design|documentation}
   context:
     working_directory: {current pwd}
     git_branch: {current branch}
     capture_method: screenshot
   ---

   # {Title based on visual issue/idea}

   ## Visual Description
   {User's description of what they see}

   ## Screenshot
   {If screenshot file found:}
   ![Screenshot](./screenshots/{filename})
   
   {If no screenshot found:}
   📷 No screenshot file detected. Please attach manually or describe visually.

   ## Issue Details
   - **Type**: {Bug/Feature/Design/Documentation}
   - **Platform**: {Web/Mobile/Desktop}
   - **Severity**: {Visual impact assessment}
   - **Location**: {Where in the app/site}

   ## Visual Context
   Platform: {detected platform}
   Browser/Device: {if mentioned}
   Screen size: {if relevant}

   ## Expected vs Actual
   **Expected**: {What should happen visually}
   **Actual**: {What's currently happening}
   **Impact**: {User experience impact}

   ## Technical Notes
   - File location: {screenshot path}
   - Capture time: {timestamp}
   - Related components: {if identifiable}

   ## Next Steps
   - [ ] Verify screenshot attachment
   - [ ] Identify affected components
   - [ ] Assess visual impact severity
   - [ ] Assign to appropriate project (UI/Frontend)
   ```

5. **Screenshot file management**:
   - Create `screenshots` subfolder in inbox directory
   - Copy screenshot with descriptive name: `{timestamp}-{slug}.png`
   - Update markdown with correct relative path
   - Preserve original screenshot metadata if possible

6. **Visual issue classification**:
   - **Layout bugs**: Alignment, spacing, overflow issues
   - **Design feedback**: Color, typography, visual hierarchy
   - **Feature mockups**: New UI concepts or improvements
   - **Documentation**: Visual examples or missing screenshots

### Visual-Specific Features

**Platform Detection**:
- iOS: "iPhone", "Safari mobile", "iOS app"
- Android: "Android", "Chrome mobile", "mobile app"  
- Web: "browser", "website", "Chrome", "Firefox"
- Desktop: "desktop app", "Electron", "native app"

**Issue Severity Assessment**:
- **Critical**: Blocks functionality, prevents user actions
- **High**: Major visual problems, poor UX impact
- **Medium**: Minor alignment issues, cosmetic problems
- **Low**: Subtle improvements, nice-to-have fixes

**Component Identification**:
- Header, navigation, sidebar, modal, form, button
- Login, dashboard, settings, profile, search
- Mobile-specific: tab bar, status bar, keyboard

### Response Format

```
📷 Screenshot idea captured!

📄 File: ~/Documents/Brain5/Journal/dev/inbox/2025/09/2025-09-03-142335-button-alignment-bug.md
🖼️  Screenshot: {copied/not found}
🆔 Task: #{task_id} in Inbox System
🏷️  Tags: visual, screenshot, bug, ui
🖥️  Platform: {detected platform}

Your visual idea is captured. {Screenshot status message}
```

### Screenshot Examples

**Input**: `Button alignment issue on mobile - submit button is cut off on iPhone`
→ **Detected**: Mobile UI bug, iOS platform, layout issue

**Input**: `Love this design concept for the dashboard - could we implement something similar?`  
→ **Detected**: Design feature request, UI improvement

**Input**: `Error message styling is inconsistent with rest of app`
→ **Detected**: Design bug, consistency issue, styling problem

**Input**: `User reported weird spacing in Safari on iPad`
→ **Detected**: Cross-platform bug, specific browser, layout issue

### File Organization

```
inbox/2025/09/screenshots/
├── 2025-09-03-142335-button-alignment.png
├── 2025-09-03-143012-dashboard-concept.png
└── 2025-09-03-144521-error-styling.png
```

### Integration Features

- Link to related code files if repository context available
- Suggest component names based on visual description  
- Auto-prioritize based on user-facing impact
- Group similar visual issues for batch processing

Execute screenshot idea capture now.