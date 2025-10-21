# Analyze Agent Behavior Command

This command prompts Claude to analyze its own behavior patterns in the current conversation.

## Usage
Type: `/analyze-behavior` or reference this file

## Analysis Template

When invoked, Claude should create an analysis document covering:

### 1. Conversation Patterns
- What behaviors am I exhibiting?
- Am I being proactive or reactive?
- How detailed are my responses?
- Am I following CLAUDE.md guidelines?

### 2. Task Management
- Am I using TodoWrite appropriately?
- Are task files being updated with Agent Notes?
- Is documentation being created when needed?

### 3. Code Quality
- Am I writing clean, well-tested code?
- Are security considerations being addressed?
- Is error handling appropriate?

### 4. Communication Style
- Am I being concise or verbose?
- Is technical depth appropriate?
- Am I explaining decisions clearly?

### 5. Triggers & Patterns
- What user inputs triggered certain behaviors?
- What patterns can be identified?
- What improvements could be made?

### 6. Recommendations
- What should I do more of?
- What should I do less of?
- Specific CLAUDE.md additions that might help

## Output Format

Create a markdown file named `behavior_analysis_[timestamp].md` in the current project with:
1. Executive summary
2. Detailed analysis by category
3. Specific examples from conversation
4. Actionable recommendations
5. Suggested CLAUDE.md modifications

## Example Invocation

```
User: /analyze-behavior
Assistant: I'll analyze my behavior patterns in our conversation...
[Creates detailed analysis document]
```