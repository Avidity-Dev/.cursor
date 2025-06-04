# Code History & Critical Context

This rule is specifically for documenting code after significant development iterations, capturing historical context and marking critical sections.

## When To Apply This Rule
Apply this rule after:
- Lengthy debugging or troubleshooting sessions
- Multiple iterations to solve a complex problem
- Implementing workarounds for limitations in dependencies
- Making performance optimizations

## Historical Context Documentation
At the top of relevant files or functions, add a section like:

```python
"""
Implementation History:
- Initially attempted using approach X, which failed because...
- Current implementation uses approach Y to solve...
- Performance was improved by...
"""
```

## Critical Code Sections
For sections that should not be modified without careful consideration:

1. Mark the beginning and end of critical sections with comments:
```python
# CRITICAL SECTION - DO NOT MODIFY WITHOUT UNDERSTANDING:
# This implementation addresses [specific issue] by [approach]
# Changing this could break [functionality] because [reason]
...code...
# END CRITICAL SECTION
```

2. Document exactly why the code needs to remain as-is:
   - Dependencies on external systems
   - Workarounds for known issues
   - Performance optimizations that may seem counterintuitive
   - Security considerations

## Implementation Decision Records
For complex implementations, include mini decision records:

```python
"""
Decision Record:
Problem: [Describe the problem that needed solving]
Alternatives Considered:
1. [Approach A] - Rejected because [reason]
2. [Approach B] - Rejected because [reason]
Chosen Solution: [Approach C] because [justification]
Trade-offs: [List benefits and drawbacks of the chosen approach]
"""
```

This documentation helps both human developers and AI assistants understand the historical context and decision-making process behind complex code, preventing accidental breaking changes when modifying the codebase.