---
allowed-tools: mcp__Parallel__create_task, Write, Bash
description: Capture voice-transcribed ideas with audio context preservation
---

# Inbox Voice: Capture Voice Ideas

## Context
- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Working directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Inbox project ID: 262 (Inbox System)

## Task: Capture Voice-Transcribed Idea

Capture ideas that were spoken aloud and transcribed, preserving the conversational nature and context.

### Input
Voice transcription: `$ARGUMENTS`

### Process

1. **Parse voice input**:
   - Handle conversational language patterns
   - Extract key concepts from natural speech
   - Identify action items from rambling thoughts
   - Detect emotional context (excitement, frustration, uncertainty)

2. **Generate voice-specific metadata**:
   - ID: `inbox-voice-{timestamp}`
   - Auto-tag with `#voice`
   - Preserve transcription quality notes
   - Mark uncertain transcriptions with `[unclear]`

3. **Create enhanced inbox file**:
   ```yaml
   ---
   id: inbox-voice-{timestamp}
   created: {ISO timestamp}
   tags: [voice, extracted, tags]
   status: unprocessed  
   urgency: {detected from tone/words}
   source: voice-transcription
   voice_context:
     transcription_quality: {high|medium|low}
     speaking_pace: {fast|normal|slow}
     confidence_level: {high|medium|low}
     unclear_sections: [list of unclear parts]
   context:
     working_directory: {current pwd}
     git_branch: {current branch}
     capture_method: voice
   ---

   # {Cleaned up title from speech}

   ## Original Transcription
   {Raw voice input exactly as transcribed}

   ## Cleaned Summary  
   {Organized version of the rambling thoughts}

   ## Key Points
   - {Main idea 1}
   - {Main idea 2}
   - {Action items identified}

   ## Context
   Captured via voice while working in: {working_directory}
   Speaking pattern: {conversational|structured|excited|frustrated}

   ## Transcription Notes
   - Quality: {assessment}
   - Unclear sections: {marked with [unclear]}
   - Confidence: {overall confidence in accuracy}

   ## Next Steps
   - [ ] Review transcription accuracy
   - [ ] Clean up unclear sections  
   - [ ] Extract concrete action items
   - [ ] Assign to appropriate project
   ```

4. **Voice-specific processing**:
   - **Conversational cleanup**: Convert "um, so like, I think we should..." to "We should..."
   - **Action extraction**: Identify "we need to", "I should", "let's" patterns
   - **Context inference**: Infer technical context from speech patterns
   - **Urgency detection**: Recognize tone indicators ("urgent", "ASAP", "critical")

5. **Create database entry**:
   - Project ID: 262 (Inbox System)
   - Title: Cleaned version of main idea
   - Description: Include both raw transcription and cleaned summary
   - Priority: Based on detected urgency and tone
   - Mark as "VOICE INBOX ITEM" for filtering

### Voice-Specific Features

**Transcription Quality Assessment**:
- High: Clear speech, good recognition, minimal errors
- Medium: Some unclear words, mostly accurate
- Low: Multiple unclear sections, needs review

**Speaking Pattern Recognition**:
- **Stream of consciousness**: Long, rambling thoughts → needs extraction
- **Technical discussion**: Specific terms → preserve accuracy
- **Brainstorming**: Multiple ideas → break into sections
- **Problem solving**: "What if we..." → mark as exploration

**Emotional Context Detection**:
- **Excitement**: "This is amazing!", "Perfect!" → high priority
- **Frustration**: "This is broken", "Why doesn't..." → urgent bug
- **Uncertainty**: "Maybe", "I think", "Not sure" → research needed
- **Confidence**: "Definitely", "We should" → actionable

### Response Format

```
🎤 Voice idea captured!

📄 File: ~/Documents/Brain5/Journal/dev/inbox/2025/09/2025-09-03-142335-voice-sync-idea.md
🆔 Task: #{task_id} in Inbox System  
🏷️  Tags: voice, sync, feature
🎯 Quality: {transcription_quality}
📢 Tone: {detected_emotion}

Your voice idea is captured with context preserved. 
Review transcription accuracy before processing.
```

### Voice Input Examples

**Input**: `Um, so I was thinking, like, we really need to add some kind of, uh, WebDAV sync support because, you know, people want to access their files from different devices and stuff. It's kind of urgent because the client keeps asking about it.`

→ **Cleaned**: "Add WebDAV sync support for multi-device file access. Client has been requesting this feature urgently."

**Input**: `Oh man, this is so frustrating! The memory leak in the background process is killing performance. We need to fix this ASAP before it affects more users.`

→ **Detected**: High urgency, frustration, technical issue requiring immediate attention

**Input**: `I'm not sure about this, but maybe we could explore using WASM for better performance? It might be worth researching, though I don't know if it's worth the complexity.`

→ **Pattern**: Research exploration, uncertainty, needs investigation

### Error Handling

- Handle empty or very short transcriptions
- Deal with technical terms that may be mis-transcribed
- Recover from audio quality issues
- Preserve original even if cleanup fails

Execute voice idea capture now.