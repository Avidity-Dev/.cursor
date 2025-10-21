# Critical Code Review Command

When you need a thorough, critical review of code (like a senior developer would do), use this command.

## Quick Command

```
Please do a critical code review of [PR/file/feature]. Look for over-engineering, unnecessary complexity, and whether it's actually needed. Be brutally honest.
```

## Full Command Template

```
Please review [PR #X / this code / this feature] with a critical eye, like a senior developer would:

A) Do we actually need this? Is there evidence of a real problem being solved?
B) Is the code solid? Look for bugs, edge cases, and maintenance issues.
C) What would you change or simplify? Be specific.

Consider:
- YAGNI (You Aren't Gonna Need It)
- Premature optimization
- Over-engineering vs pragmatic solutions
- Maintenance burden
- Bug surface area
- Whether simpler alternatives exist

Be brutally honest - this is for learning and improvement.
```

## Specific Review Types

### Performance Optimization Review
```
Please critically review this performance optimization:
- Is there evidence of actual performance problems?
- Are there benchmarks showing the issue?
- Could simpler solutions (like indexes or connection pooling) solve it?
- What's the complexity cost vs performance gain?
```

### Architecture Review
```
Please critically review this architecture/design:
- Is this solving a real problem or a theoretical one?
- How many layers of abstraction are actually needed?
- What's the simplest solution that could work?
- What are the maintenance implications?
```

### Feature Addition Review
```
Please critically review this new feature:
- Do users actually need this?
- Could existing features solve this use case?
- What's the total cost of ownership?
- Are there simpler alternatives?
```

## What to Look For

### Red Flags
- No tests for complex code
- String matching for critical logic
- Reinventing existing solutions
- Excessive abstraction layers
- No evidence of the problem
- Resume-driven development

### Good Practices to Acknowledge
- Well-designed database schemas/indexes
- Clear, simple solutions
- Good error handling
- Appropriate test coverage
- Evidence-based decisions

## Example Usage

### Example 1: Caching System
```
Please do a critical code review of this caching implementation. It adds 2000+ lines to solve "slow queries" but our queries are already <10ms.
```

### Example 2: New Framework
```
Please critically review this proposal to add GraphQL. Our REST API works fine and we have 3 endpoints total. Be honest about whether we need this.
```

### Example 3: Abstraction Layers
```
Please review this Repository pattern implementation. It adds 5 layers between the controller and database for basic CRUD. What would you actually do?
```

## Review Template Structure

The review should follow this structure:

### 1. Problem Analysis
- What problem is this trying to solve?
- Is there evidence this problem exists?
- How severe/frequent is the problem?

### 2. Solution Assessment  
- Is this the simplest solution?
- What alternatives exist?
- What's the complexity vs benefit tradeoff?

### 3. Code Quality Issues
- **🔴 Blockers**: Security, data loss, broken functionality
- **🟡 Major**: Performance, maintainability, missing tests
- **🟢 Minor**: Style, documentation, nice-to-haves

### 4. What I'd Do Instead
- Specific alternative implementation
- Why it's better
- Migration path if needed

### 5. Recommendation
- **Accept**: Merge as-is
- **Accept with changes**: Specific required fixes
- **Reject**: Not needed or wrong approach

## Why This Matters

- Prevents over-engineering
- Reduces maintenance burden
- Keeps codebases simple
- Teaches pragmatic engineering
- Saves time and resources

## Example Review Output

```
## Critical Review: User Caching System PR

### 1. Problem Analysis
- **Claimed problem**: "Slow queries" 
- **Evidence**: None provided
- **Actual measurements**: Queries already <10ms

### 2. Solution Assessment
- Adds 2,100+ lines of caching code
- No simpler alternatives tried (indexes, connection pooling)
- Complexity cost >> performance benefit

### 3. Code Quality Issues

🔴 **Blockers**
- Cache invalidation uses string matching (line 135) - will break with similar table names
- No connection pooling - defeats the purpose

🟡 **Major Issues**
- Zero tests for 2,100 lines
- Premature optimization without evidence
- In-memory cache won't scale

### 4. What I'd Do Instead
```python
# 1. Just add connection pooling (50 lines max)
class ConnectionPool:
    async def acquire(self): ...
    async def release(self, conn): ...

# 2. Apply the indexes (they're actually good!)
# 3. Measure again before adding complexity
```

### 5. Recommendation: **Reject**
Extract the indexes (migration 005), discard the rest. Revisit only with performance data.
```

## Related Commands

- `reject-pr.md` - For formally rejecting PRs