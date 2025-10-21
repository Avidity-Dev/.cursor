# Create Executive Progress Update

## Overview

Generate a crisp, leadership-focused progress update following the executive update format. This format emphasizes status, impact, and business value over technical implementation details.

## Steps

1. **Gather work completed**

   - Identify major services, features, or initiatives completed
   - Note key improvements or platform enhancements
   - Focus on production-ready or significant milestone achievements

2. **Structure the update**

   - Start with a clear heading: `# Engineering Progress Update`
   - Group related work into logical sections (e.g., "Core Services Productionized")
   - Use consistent subsection formatting for each deliverable

3. **Format each deliverable**

   - **Service/Feature Name** as H3 (`###`)
   - **Status:** line (e.g., "Production-ready", "In Progress", "Completed")
   - **Impact:** line stating business value in plain language
   - Bulleted list (3-4 items max) of key highlights
   - Keep bullets concise - one line per bullet

4. **Add platform/infrastructure improvements**

   - Create separate section: `## Platform Improvements`
   - List cross-cutting improvements as simple bullets
   - Focus on what matters: observability, quality, automation

5. **Review for executive audience**
   - Remove technical jargon and implementation details
   - Lead with outcomes and business impact
   - Ensure status is clear and unambiguous
   - Keep it scannable - leadership should grasp progress in 60 seconds

## Template

```markdown
# Engineering Progress Update

## Core Services Productionized

### [Service/Feature Name]

**Status:** [Production-ready | In Progress | Completed]  
**Impact:** [One sentence describing business value]

- Key capability or improvement
- Performance or quality enhancement
- Scalability or maintainability benefit

### [Another Service/Feature]

**Status:** [Status]  
**Impact:** [Business value]

- Highlight 1
- Highlight 2
- Highlight 3

## Platform Improvements

- Infrastructure or tooling enhancement
- Quality or observability improvement
- Documentation or operational guide
```

## Checklist

- [ ] Each deliverable has clear status
- [ ] Impact statements focus on business value, not technical details
- [ ] Bullets are concise (one line each, 3-4 max per section)
- [ ] Technical jargon removed or explained
- [ ] Update is scannable in 60 seconds or less
- [ ] Consistent formatting throughout
- [ ] Saved in `docs/reports/` directory with descriptive filename

## Examples

### ✅ Good Impact Statement

**Impact:** Observable, maintainable data pipeline with quality safeguards

### ❌ Poor Impact Statement

**Impact:** Converted Python scripts to clean architecture with dbt models and validation checks

### ✅ Good Bullet

- dbt-based transformation pipeline with comprehensive validation checks

### ❌ Poor Bullet (too technical)

- Implemented ConfigurableValidator with SchemaValidator and BusinessRuleValidator using factory pattern for dynamic validation rule loading from YAML configuration files

## Common Pitfalls

- **Too much technical detail** - Leadership doesn't need to know about specific patterns or technologies
- **Vague status** - Use clear states like "Production-ready" not "mostly done"
- **Missing impact** - Always explain why this matters to the business
- **Too long** - If bullets exceed one line, split or simplify
- **Inconsistent format** - Use the same structure for every deliverable
