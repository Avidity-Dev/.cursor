---
allowed-tools: mcp__Parallel__create_task, Write, Bash
description: Capture code snippets and technical ideas with syntax highlighting
---

# Inbox Code: Capture Code Ideas

## Context

- Current time: !`date +"%Y-%m-%d %H:%M:%S"`
- Working directory: !`pwd`
- Git branch: !`git branch --show-current 2>/dev/null || echo "not a git repo"`
- Inbox project ID: 262 (Inbox System)

## Task: Capture Code-Based Idea

Capture code snippets, technical solutions, algorithm ideas, or implementation concepts that need to be preserved for later development.

### Input

Code description and snippet: `$ARGUMENTS`

### Process

1. **Parse code input**:

   - Extract code snippets from input (look for code blocks, indented sections)
   - Identify programming language from context or file extensions
   - Detect technical concepts (algorithms, patterns, libraries)
   - Classify type (snippet, solution, refactor, optimization)

2. **Language detection**:

   - Look for language indicators: "python", "javascript", "sql", etc.
   - Analyze code syntax patterns for auto-detection
   - Check file extension mentions (.py, .js, .rs, etc.)
   - Default to current project language if unclear

3. **Generate code-specific metadata**:

   - ID: `inbox-code-{timestamp}`
   - Auto-tag with `#code` and detected language
   - Add concept tags (`#algorithm`, `#optimization`, `#refactor`)
   - Include complexity indicators (`#simple`, `#complex`)

4. **Create code inbox file**:

   ````yaml
   ---
   id: inbox-code-{timestamp}
   created: {ISO timestamp}
   tags: [code, {detected_language}, {concept_tags}]
   status: unprocessed
   urgency: {based on technical priority}
   source: code-capture
   code_context:
     language: {detected_language}
     type: {snippet|solution|refactor|optimization|algorithm}
     complexity: {simple|medium|complex}
     dependencies: [list of mentioned libraries/frameworks]
     related_files: [mentioned file paths]
   context:
     working_directory: {current pwd}
     git_branch: {current branch}
     repository: {repo name if in git}
     capture_method: code-snippet
   ---

   # {Title based on code concept}

   ## Code Concept
   {User's description of the code idea}

   ## Code Snippet
   ```{detected_language}
   {code from user input}
   ````

   ## Technical Details

   - **Language**: {detected_language}
   - **Type**: {snippet|solution|refactor|optimization}
   - **Complexity**: {assessment}
   - **Dependencies**: {libraries/frameworks mentioned}

   ## Context

   Repository: {current repo if applicable}
   Branch: {current branch}
   Related files: {mentioned files}

   ## Implementation Notes

   {Technical considerations, gotchas, requirements}

   ## Usage Example

   ```{language}
   {Example of how to use this code}
   ```

   ## Alternative Approaches

   {Other ways to solve the same problem}

   ## Next Steps

   - [ ] Test code snippet in appropriate environment
   - [ ] Check for existing similar implementations
   - [ ] Consider edge cases and error handling
   - [ ] Integrate into appropriate project

   ```

   ```

5. **Code-specific processing**:

   - **Syntax validation**: Basic syntax checking if possible
   - **Dependency extraction**: Find import/require statements
   - **Pattern recognition**: Identify common patterns (observer, factory, etc.)
   - **Performance hints**: Flag potential performance considerations

6. **Create database entry**:
   - Project ID: 262 (Inbox System)
   - Title: Descriptive name of the code concept
   - Description: Include code, context, and technical details
   - Priority: Based on complexity and urgency indicators
   - Mark as "CODE INBOX ITEM" for filtering

### Code-Specific Features

**Language Detection**:

- Python: `def`, `import`, `.py`, `python`
- JavaScript: `function`, `const`, `.js`, `javascript`
- TypeScript: `interface`, `type`, `.ts`, `typescript`
- Rust: `fn`, `use`, `.rs`, `rust`
- SQL: `SELECT`, `CREATE`, `.sql`
- Go: `func`, `package`, `.go`
- Shell: `#!/bin/bash`, `.sh`, `bash`

**Code Type Classification**:

- **Snippet**: Small code fragment, utility function
- **Solution**: Complete solution to a specific problem
- **Refactor**: Improved version of existing code
- **Optimization**: Performance improvement idea
- **Algorithm**: Core algorithmic concept
- **Pattern**: Design pattern implementation

**Complexity Assessment**:

- **Simple**: < 10 lines, basic operations, no dependencies
- **Medium**: 10-50 lines, some logic, few dependencies
- **Complex**: > 50 lines, complex logic, many dependencies

### Response Format

```
💻 Code idea captured!

📄 File: ~/Documents/Brain5/Journal/dev/inbox/2025/09/2025-09-03-142335-async-queue-solution.md
🆔 Task: #{task_id} in Inbox System
🏷️  Tags: code, python, algorithm, optimization
⚙️  Language: {detected_language}
🔧 Type: {code_type}

Your code idea is preserved with syntax highlighting and context.
```

### Code Examples

**Input**: `Here's a nice Python async queue solution I found:

```python
import asyncio
async def worker(queue):
    while True:
        item = await queue.get()
        # process item
        queue.task_done()
```

→ **Detected**: Python, async pattern, medium complexity

**Input**: `SQL optimization idea - use window functions instead of subqueries for ranking`
→ **Detected**: SQL, optimization, database performance

**Input**: `JavaScript debounce function for search input:
function debounce(func, delay) { ... }`
→ **Detected**: JavaScript, utility function, UI optimization

**Input**: `Rust zero-copy string parsing using str slices instead of String allocation`
→ **Detected**: Rust, optimization, memory management

### Advanced Features

**Code Analysis**:

- Detect potential security issues in snippets
- Flag deprecated patterns or libraries
- Suggest modern alternatives
- Estimate implementation time

**Integration Helpers**:

- Link to relevant documentation
- Suggest test cases based on code
- Identify files where code might be used
- Check for similar existing code in project

**Learning Tracking**:

- Tag new concepts encountered
- Link to learning resources
- Track technology exploration
- Build personal code pattern library

Execute code idea capture now.
