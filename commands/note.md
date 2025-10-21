---
allowed-tools: Write, Bash, Read
description: Create a structured note in Obsidian vault with timestamp and metadata
---

# Note: Create Obsidian Vault Note

## Context

- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Working directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Vault path (absolute): ~/Documents/Brain5/Journal/dev/
- **IMPORTANT**: Vault is most oftenNOT in current repository - always use absolute path

## Task: Create Structured Note

Create a well-structured note in your Brain5 Obsidian vault with proper metadata, linking, and organization.

### Input

Note content: `$ARGUMENTS`

**Default Behavior**: If no arguments are provided, create a note summarizing the current conversation, including:

- Key topics discussed
- Important decisions or conclusions reached
- Technical details or implementations covered
- Any action items or next steps mentioned
- Relevant code changes or files discussed

**Multiple Topics Check**: When defaulting to the current conversation, if the conversation included multiple distinct topics or concepts, ask the user:

```
I notice this conversation covered multiple topics:
1. [Topic 1 name]
2. [Topic 2 name]
3. [Topic 3 name]

Would you like:
A) A single note covering all topics
B) Separate notes for each topic

Please respond with A or B.
```

### Process

1. **Determine note content**:

   - If `$ARGUMENTS` is empty/blank:
     - Analyze the current conversation for distinct topics
     - If multiple distinct topics exist, ask user for preference (single note vs. separate notes)
     - If user chooses separate notes, create one note per topic
     - If user chooses single note or only one topic exists, create a comprehensive summary
   - If `$ARGUMENTS` is provided: Use the provided content

2. **Parse the input** to determine:

   - Note title (first line or first few words)
   - Note type (meeting, research, decision, learning, project, etc.)
   - Tags from content (#tag patterns)
   - Links to existing notes ([[Note Name]] patterns)
   - Priority or urgency indicators

3. **Generate note metadata**:

   - Timestamp: Current ISO 8601 timestamp
   - Filename: `YYYY-MM-DD-HHMMSS-{slug}.md`
   - Slug: Title converted to kebab-case, max 50 chars
   - File path (absolute): `~/Documents/Brain5/Journal/dev/{filename}`

3a. **Validate vault location** (CRITICAL - vault is most oftenNOT in current repository):

```bash
# Define the vault path (absolute - frequently NOT in current repo)
VAULT_PATH="$HOME/Documents/Brain5/Journal/dev"

# Check if vault exists (don't create it)
if [ ! -d "$VAULT_PATH" ]; then
    echo "❌ Obsidian vault directory not found at: $VAULT_PATH"
    echo "Please ensure your Obsidian vault is set up correctly"
    exit 1
fi

# Create the note file in the vault
NOTE_FILE="$VAULT_PATH/${TIMESTAMP}-${SLUG}.md"
```

**Important**: The Obsidian vault is at an absolute path and is typically NOT within the current working directory or git repository. Always use the full path `$HOME/Documents/Brain5/Journal/dev` regardless of where the command is executed from.

4. **Detect note type** from content or patterns:

   - **Meeting**: Contains "meeting", "agenda", "attendees"
   - **Research**: Contains "research", "investigate", "explore"
   - **Decision**: Contains "decision", "choose", "decided"
   - **Learning**: Contains "learned", "TIL", "discovered"
   - **Project**: Contains "project", "plan", "roadmap"
   - **Daily**: Contains "today", "daily", date patterns
   - **Conversation**: Auto-generated from chat history (when no arguments provided)
   - **Generic**: Default fallback

5. **Create structured note** with appropriate template:

   ```yaml
   ---
   created: {ISO timestamp}
   modified: {ISO timestamp}
   tags: [note, {detected_type}, {extracted_tags}]
   type: {note_type}
   status: draft
   context:
     working_directory: {current_pwd}
     git_branch: {current_branch}
     capture_source: claude-command
   ---

   # {Note Title}

   {Main content from user}

   ## Context
   - Created: {human_readable_date}
   - Location: {working_directory}
   - Branch: {git_branch}

   ## Key Points
   {Auto-extracted bullet points if applicable}

   ## Related
   {Auto-detected links and references}

   ## Next Actions
   {Extracted action items if any}

   ## References
   {Links to related files or external resources}
   ```

6. **Handle different note types** with specialized sections:

   **Meeting Notes**:

   - Attendees section
   - Agenda items
   - Action items with owners
   - Follow-up section

   **Research Notes**:

   - Research question
   - Findings
   - Sources and references
   - Conclusions

   **Decision Notes**:

   - Decision context
   - Options considered
   - Decision made
   - Rationale
   - Implementation plan

   **Conversation Notes** (when auto-generated):

   - Summary of main discussion topics
   - Key technical details or code discussed
   - Decisions or conclusions reached
   - Files or components mentioned
   - Action items or next steps

7. **Ensure file organization**:
   - Check if file already exists (handle conflicts)
   - Create any necessary parent directories
   - Use safe filename characters
   - Handle long titles gracefully

### Response Format

```
📝 Note created successfully!

📄 File: ~/Documents/Brain5/Journal/dev/2025-09-03-142335-note-title.md
     (Absolute path - stored in Obsidian vault, not current repository)
📂 Type: {detected_note_type}
🏷️  Tags: {extracted_tags}
🔗 Links: {detected_links}

Your note is ready in Obsidian. You can find it in the Journal/dev folder.
```

### Advanced Features

**Smart Linking**:

- Detect references to existing files in vault
- Auto-create backlinks where appropriate
- Suggest related notes based on content

**Content Enhancement**:

- Extract and format bullet points
- Identify and highlight action items
- Parse dates and create calendar references
- Format code blocks with proper syntax

**Integration**:

- Link to related inbox items if relevant
- Connect to project files when working in git repos
- Preserve context for future reference

### Examples

**Input**: (no arguments - defaults to current conversation)

→ **Creates**: Conversation note summarizing the current discussion, including topics covered, technical details, decisions made, and any action items

**Input**: `Meeting with design team about new dashboard layout. Discussed user flow improvements and decided to prototype mobile-first approach.`

→ **Creates**: Meeting note with attendees section, agenda, decisions, and action items

**Input**: `Researching WebDAV implementation options. Found three main libraries: webdav-client, webdav-server, and sardine. Need to compare features and performance.`

→ **Creates**: Research note with research question, findings, and next steps

**Input**: `TIL about Rust's zero-copy string parsing using str slices. Much more efficient than String allocation for temporary parsing.`

→ **Creates**: Learning note with discovery, technical details, and code examples

**Input**: `Daily standup notes - completed authentication refactor, blocked on API rate limiting, planning to tackle caching system next.`

→ **Creates**: Daily note with status updates and planning

### Note Type Templates

**Meeting Template**:

- Meeting type and purpose
- Attendees list
- Agenda items
- Decisions made
- Action items with owners
- Follow-up scheduled

**Research Template**:

- Research question/hypothesis
- Methodology or approach
- Key findings
- Sources and references
- Conclusions and implications
- Next research steps

**Decision Template**:

- Decision context and timeline
- Stakeholders involved
- Options evaluated
- Criteria used
- Decision made and rationale
- Implementation plan
- Success metrics

### Usage Tips

Display helpful tips for effective note-taking:

```
💡 Note Creation Tips:

📝 Run without arguments to capture the current conversation automatically
🏷️  Use hashtags for easy categorization: #meeting #research #decision
🔗 Reference other notes with [[Note Name]] for automatic linking
📋 Start action items with "- [ ]" for task checkboxes
📅 Include dates in natural language for calendar integration
🎯 Be specific in titles for better searchability

Examples:
/note                                                                    # Captures current conversation
/note Weekly team sync - discussed Q4 priorities #meeting
/note [[Project Name]] architecture decision - chose microservices #decision
/note TIL about async/await patterns in Rust #learning #rust
```

Execute note creation now based on the user's input.
