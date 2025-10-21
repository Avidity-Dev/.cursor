# Conversation Analysis Command

Deep analysis of conversation patterns to identify triggers and optimize agent behavior.

## Usage
Type: `/conversation-analysis` or reference this file

## Analysis Framework

### 1. Trigger Identification
Analyze what user inputs led to specific behaviors:

```python
trigger_patterns = {
    "detailed_documentation": [
        "User asked: 'did you add details to the task file?'",
        "User said: 'imagine you are a senior dev'"
    ],
    "proactive_behavior": [
        "User showed appreciation: 'btw it's a good thing!'",
        "User asked for analysis: 'why do you think that is?'"
    ]
}
```

### 2. Behavior Metrics

Track quantifiable behaviors:
- Files created vs modified
- Documentation files created
- Task updates with/without notes
- Test coverage
- Security considerations raised

### 3. Response Analysis

#### Conciseness Score
- Measure: Lines of response / Information conveyed
- Target: High information density

#### Completeness Score  
- Did I answer all parts of the question?
- Did I anticipate follow-up questions?

#### Technical Depth
- Surface level / Appropriate / Too deep
- Match to user's apparent expertise

### 4. Pattern Recognition

Look for:
- Repeated user corrections
- Consistent praise/criticism patterns  
- Topics that generate longer responses
- Commands/tools used most frequently

### 5. Improvement Opportunities

Generate specific recommendations:
- "Add to CLAUDE.md: [specific text]"
- "Change behavior: [from X to Y]"
- "Watch for pattern: [description]"

## Output Example

```markdown
# Conversation Analysis - [Date]

## Executive Summary
- Conversation length: X messages
- Dominant patterns: Detailed documentation, security awareness
- Key trigger: Senior dev roleplay request
- Recommendation: Maintain current documentation standards

## Detailed Findings

### Positive Patterns
1. **Comprehensive task documentation**
   - Trigger: User feedback on task details
   - Result: All subsequent tasks included Agent Notes
   
### Areas for Improvement
1. **Initial assumptions**
   - Issue: Updated project CLAUDE.md instead of user
   - Fix: Always clarify scope before file modifications

## Behavioral Model
Based on this conversation, optimal behavior includes:
- Think like: Senior developer doing code review
- Document like: Team lead handing off project
- Communicate like: Experienced mentor

## Suggested CLAUDE.md Addition
"When unsure about scope (user vs project), always ask for clarification."
```

## Auto-Triggers

Consider running this analysis when:
- Conversation exceeds 20 exchanges
- User asks about agent behavior
- Multiple corrections needed
- Preparing conversation summary