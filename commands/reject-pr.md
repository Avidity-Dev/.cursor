# Reject PR Command

When you need to reject a PR, follow the structured workflow to ensure proper documentation and feedback.

## Quick Command

```
Please help me reject PR #[NUMBER] using the PR rejection workflow. 

The main issues are:
- [Issue 1]
- [Issue 2]

Good parts worth saving:
- [Good part 1]
```

## Full Command Template

```
Please help me reject PR #[NUMBER]. Here's my assessment:

**Good aspects:**
- [What they did well]
- [Useful concepts/code]

**Problems:**
- [Main issue]
- [Secondary issues]

**Rejection category:** [premature-optimization|over-engineering|wrong-approach|missing-requirements|needs-tests]

Please:
1. Create a detailed PR comment
2. Create an Architecture Decision Record
3. Tag the branch appropriately  
4. Extract any salvageable code (especially: [specific files if known])
5. Close the PR

Follow the workflow in docs/workflows/pr-rejection-workflow.md
```

## Examples

### Example 1: Premature Optimization
```
Please help me reject PR #42. It adds caching to the user service but we have no performance issues. The cache invalidation logic looks buggy. The connection pooling idea is good though - please extract that part.
```

### Example 2: Over-Engineering
```
Please help me reject PR #99. It introduces 5 layers of abstraction for a simple CRUD API. The validation logic in src/validators/ is solid and worth keeping. Main issue: too complex for our needs.
```

### Example 3: Wrong Approach
```
Please help me reject PR #12. They're trying to solve the sync problem with polling, but we need webhooks. The error handling code is excellent - please save that. Be encouraging, they clearly put in effort.
```

## Workflow Location

The full workflow documentation is at: `docs/workflows/pr-rejection-workflow.md`

## Why This Matters

- Rejected PRs often contain good ideas
- Contributors deserve clear feedback
- Future team members need context
- Learning opportunities shouldn't be wasted