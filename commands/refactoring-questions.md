# Refactoring Questions Command

A comprehensive checklist of questions to ask before implementing any significant refactoring or new component.

## Usage
Type: `/refactoring-questions` or reference this file when planning a refactor

## Framework: Questions to Ask Before Implementation

When planning a significant refactoring or new component, systematically work through these questions:

### 1. Current State Analysis Questions

- [ ] What exact methods in the existing code handle this functionality?
- [ ] What are the input/output contracts of these methods?
- [ ] Are there any hidden dependencies or side effects?
- [ ] What validation logic exists and where is it located?
- [ ] How is error handling currently implemented?

### 2. Architecture & Design Questions

- [ ] Should this component be stateless or stateful?
- [ ] What dependencies does it need?
- [ ] Should it implement an interface/protocol for future flexibility?
- [ ] How will it integrate with the existing architecture?
- [ ] Should certain concerns be separate or combined?

### 3. Functionality Scope Questions

- [ ] What constitutes this component's responsibility vs other concerns?
- [ ] What types of data will it handle?
- [ ] What business rules need to be incorporated?
- [ ] What should be optional vs required functionality?
- [ ] What about caching - is that in scope?

### 4. Technical Implementation Questions

- [ ] What specific operations/algorithms are currently used?
- [ ] Are there performance considerations for large datasets?
- [ ] How should partial failures be handled?
- [ ] What logging and monitoring is needed?
- [ ] Should we preserve original data or mutate in place?

### 5. Testing & Quality Questions

- [ ] What edge cases exist in the current implementation?
- [ ] What test data scenarios need coverage?
- [ ] How do we test external dependencies?
- [ ] What performance benchmarks should we maintain?
- [ ] Are there regression risks?

### 6. Integration Questions

- [ ] How will other components use this?
- [ ] Will multiple services need this functionality?
- [ ] How does this fit with planned future components?
- [ ] Are there any circular dependencies to avoid?
- [ ] What's the migration strategy?

## Output Format

When using this command, create a document answering these questions:

```markdown
# Refactoring Analysis: [Component Name]

## 1. Current State Analysis
- **Existing methods**: [List methods]
- **Contracts**: [Input/output types]
- **Dependencies**: [Hidden dependencies found]
- **Validation**: [Current validation logic]
- **Error handling**: [Current approach]

## 2. Architecture & Design
- **State management**: [Stateless/Stateful decision]
- **Dependencies needed**: [List]
- **Interface design**: [Protocol/ABC needed?]
- **Integration points**: [How it fits]
- **Separation of concerns**: [What to separate]

[Continue for all sections...]

## Recommendations
- [Key decisions made]
- [Risks identified]
- [Implementation approach]
```

## When to Use

- Before any major refactoring
- When creating new services/components
- When extracting functionality
- During architecture reviews
- When planning technical debt reduction

## Example Application

For a TextSimilarityService refactor:
1. Identify all text similarity methods in repositories
2. Document their contracts (vectorizers, similarity types)
3. Check for hidden dependencies (model loading, caching)
4. Design stateless service with clear interface
5. Plan migration strategy for existing code