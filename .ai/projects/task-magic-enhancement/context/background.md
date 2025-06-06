# Task Magic Enhancement - Background & Context

## Problem Statement

The original Task Magic system had several limitations:

1. **Mixed Concerns**: The system description and rules were intermingled in `.cursor/rules/.task-magic/`
2. **Single Project Focus**: No built-in support for managing multiple concurrent projects
3. **AI Discovery Issues**: No clear mechanism for AI agents to discover what projects exist
4. **Tool Lock-in**: Heavily tied to Cursor's `.mdc` rule format

## Key Insights from Discussion

### Conceptual Separation

- Task Magic is TWO things: a project management system AND rules for using it
- The system (`.ai/`) should be tool-agnostic
- The rules (`.cursor/rules/task-magic/`) should be Cursor-specific

### Directory Naming

- Originally `.task-magic` (hidden directory)
- Renamed to `task-magic` because it's already in hidden `.cursor/` directory
- Avoids double-hidden directory anti-pattern

### Inspiration

The enhancement was inspired by another assistant's approach that included:

- `context/` folders for background analysis
- `templates/` for reusable patterns
- Project-scoped organization
- Metadata headers for discovery

## Design Decisions

### 1. Project Registry (INDEX.md)

- Central discovery point for all projects
- Simple markdown table format
- Links to project-specific files

### 2. Agent Guides

- Different tools need different instructions
- `cursor-guide.md` points to `.mdc` rules
- `claude-guide.md` provides direct conventions
- `human-guide.md` offers quick reference

### 3. Context Folders

- Each project gets a `context/` directory
- Stores analysis, decisions, dependencies
- Information that doesn't fit in tasks or plans

### 4. Metadata Headers

- YAML frontmatter in all files
- Enables better search and relationships
- Standard fields: project, id, type, tags, status

## Migration Strategy

1. Keep existing `.ai/` structure initially
2. Wrap in `projects/current/` when ready
3. New projects use enhanced structure immediately
4. Gradual migration preserves continuity
