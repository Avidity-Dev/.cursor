# Senior Developer Review Command

## Description
Generates a comprehensive technical review request for senior developer feedback on recent code changes, architectural decisions, and implementation approaches.

## Usage
```
senior-dev-review
```

## What it does
1. **Context Analysis**: Reviews recent commits and modified files
2. **Change Documentation**: Documents what was implemented and why
3. **Problem-Solution Mapping**: Links specific problems to their solutions
4. **Impact Assessment**: Evaluates the effect of changes on the codebase
5. **Question Generation**: Identifies key architectural and technical decisions for review
6. **Testing Status**: Documents current test coverage and validation approach

## Review Framework

### Standard Review Questions
The command generates targeted questions in these key areas:

1. **Architecture**: Interface design, layer separation, dependency management
2. **Implementation Patterns**: Code organization, shared modules, DRY principles
3. **Data Consistency**: Naming conventions, schema alignment, validation approaches
4. **Error Handling**: Exception management, graceful degradation, user experience
5. **Framework Usage**: Library-specific best practices and idiomatic patterns

### Output Structure
- **Context**: Project background and blocking issues addressed
- **Changes Made**: Detailed problem-solution pairs for each fix
- **Files Modified**: Complete list of changed files with change types
- **Testing Status**: Current validation and test coverage
- **Review Questions**: Specific technical decisions requiring senior input
- **Next Steps**: Planned follow-up work and prioritization

## Output
- Structured markdown review request document
- Technical decision points for senior developer input
- Clear documentation of implementation choices and trade-offs