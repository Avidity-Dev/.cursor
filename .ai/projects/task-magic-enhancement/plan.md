# PRD: Task Magic Enhancement

## 1. Product overview

### 1.1 Document title and version

- PRD: Task Magic Enhancement - Multi-Project Support and System Separation
- Version: 1.0

### 1.2 Product summary

The Task Magic Enhancement project addresses fundamental limitations in the current Task Magic system by introducing multi-project support, clearer separation between the project management system and its governing rules, and improved AI agent discovery mechanisms. This enhancement transforms Task Magic from a single-project tool into a scalable, tool-agnostic project management system that can be used by any AI agent or human developer.

The core insight driving this enhancement is that Task Magic is actually two distinct things: a project management system (files and structure) and a set of rules (instructions for AI agents). By clearly separating these concerns, we enable better portability, clearer purpose, and support for multiple concurrent projects while maintaining backwards compatibility.

## 2. Goals

### 2.1 Business goals

- Enable teams to manage multiple concurrent projects without confusion or namespace collisions
- Create a tool-agnostic project management system that can be adopted by teams using different AI tools
- Improve developer productivity by providing better context preservation and project discovery
- Reduce onboarding time for new team members through self-documenting structure

### 2.2 User goals

- Easily discover and navigate between multiple active projects
- Use Task Magic with any AI assistant (Cursor, Claude, Codeium) or manually
- Preserve project context and background information beyond just tasks and plans
- Share project management structure with team members regardless of their tools

### 2.3 Non-goals

- Changing the fundamental file-based approach of Task Magic
- Creating a web UI or database-backed system
- Automating project creation without user intent
- Breaking compatibility with existing single-project setups

## 3. User personas

### 3.1 Key user types

- AI-assisted developers using Cursor or similar tools
- Terminal-based developers using Claude or other command-line AI
- Human developers working without AI assistance
- Project managers overseeing multiple initiatives

### 3.2 Basic persona details

- **AI Developer**: Uses Cursor daily, manages 3-5 concurrent projects, relies on .mdc rules
- **Terminal Developer**: Prefers command-line tools, uses Claude API, needs clear conventions
- **Manual Developer**: Reviews and updates tasks directly, needs quick reference guides
- **Project Manager**: Oversees team progress, needs high-level project visibility

### 3.3 Role-based access

- **Developer**: Full read/write access to all project files
- **Reviewer**: Read access to plans and task status, limited write access
- **Observer**: Read-only access to INDEX.md and project summaries

## 4. Functional requirements

- **Multi-Project Support** (Priority: High)
  - Project-scoped directory structure under `.ai/projects/`
  - Unique namespaces for each project's tasks and plans
  - Global memory system shared across projects
- **Project Discovery** (Priority: High)

  - Central INDEX.md registry listing all active projects
  - Project-specific PROJECT.md files for navigation
  - Tool-agnostic discovery mechanism

- **Context Preservation** (Priority: High)

  - Dedicated `context/` folders for background information
  - Support for architecture decisions, dependencies, analysis
  - Persistent storage of investigation results

- **Tool Compatibility** (Priority: High)

  - Agent-specific guide files in `.ai/agents/`
  - Clear separation of system from rules
  - Support for manual operation without AI

- **Metadata System** (Priority: Medium)

  - YAML frontmatter in all files
  - Standardized fields for project, type, tags, status
  - Relationship tracking between files

- **Shared Resources** (Priority: Medium)
  - Cross-project templates in `shared/templates/`
  - Reusable workflows and patterns
  - Common code snippets and solutions

## 5. User experience

### 5.1 Entry points & first-time user flow

- New users start by reading `.ai/SYSTEM.md` for system overview
- Tool-specific users directed to appropriate guide in `.ai/agents/`
- First project creation guided by clear conventions

### 5.2 Core experience

- **Step 1**: Check `.ai/INDEX.md` to see all active projects
  - Quick table view with status and tags
  - Direct links to project plans
- **Step 2**: Navigate to specific project directory

  - PROJECT.md provides project-specific overview
  - Clear file organization within project

- **Step 3**: Work with project files using appropriate tool
  - Cursor users tag task-magic rules
  - Claude users follow conventions in guide
  - Humans use quick reference

### 5.3 Advanced features & edge cases

- Migration of existing single-project setups
- Archiving completed projects
- Cross-project task dependencies
- Bulk operations across projects

### 5.4 UI/UX highlights

- Self-documenting file structure
- Consistent naming conventions
- Clear visual hierarchy in markdown files
- Tool-appropriate interaction patterns

## 6. Narrative

A developer managing multiple projects opens their workspace and immediately sees all active initiatives in the INDEX.md file. They navigate to their current project, where the context folder reminds them of key architectural decisions made last week. Using their preferred AI tool with the appropriate guide, they seamlessly create new tasks that reference this context. When switching projects, the clear structure prevents confusion, and when a colleague using a different AI tool joins, they can immediately contribute using their own tool's guide. The system grows with the team, preserving knowledge and maintaining clarity across all projects.

## 7. Success metrics

### 7.1 User-centric metrics

- Time to discover and navigate between projects (target: <30 seconds)
- Successful task creation without rule confusion (target: >95%)
- Context retrieval accuracy when switching projects
- User satisfaction with multi-project management

### 7.2 Business metrics

- Number of concurrent projects managed successfully
- Reduction in project setup time
- Team adoption rate across different tools
- Knowledge retention through context folders

### 7.3 Technical metrics

- File operation performance with multiple projects
- Search/discovery speed in large project sets
- Rule loading time in Cursor
- Cross-tool compatibility issues

## 8. Technical considerations

### 8.1 Integration points

- Cursor's .mdc rule system for rule files
- File system for all storage (no database)
- Git for version control compatibility
- Markdown processors for rendering

### 8.2 Data storage & privacy

- All data stored in local `.ai/` directory
- No cloud storage or external dependencies
- Sensitive information in context folders under user control
- Standard file permissions apply

### 8.3 Scalability & performance

- Directory structure scales to 100+ projects
- File-based approach may slow with 1000+ tasks per project
- INDEX.md manual maintenance at scale
- Memory system growth over time

### 8.4 Potential challenges

- Manual synchronization of INDEX.md
- Ensuring consistent metadata headers
- Migration complexity for existing projects
- Training users on new structure

## 9. Milestones & sequencing

### 9.1 Project estimate

- Medium: 2-3 weeks for full implementation

### 9.2 Team size & composition

- Small Team: 1-2 people (1 Developer with Task Magic expertise)

### 9.3 Suggested phases

- **Phase 1**: Foundation and Structure (3-4 days)
  - Key deliverables: Create enhanced directory structure, agent guides, SYSTEM.md
- **Phase 2**: Rule Updates (4-5 days)
  - Key deliverables: Update existing rules for project paths, create project.mdc, context.mdc
- **Phase 3**: Migration and Testing (3-4 days)
  - Key deliverables: Migration guide, test with multiple projects, documentation

## 10. User stories

### 10.1 Multi-Project Developer

- **ID**: US-001
- **Description**: As a developer, I want to manage multiple projects simultaneously so that I can switch contexts without confusion.
- **Acceptance Criteria**:
  - Can view all active projects in INDEX.md
  - Each project has isolated task IDs and files
  - Can navigate between projects without conflicts

### 10.2 Tool-Agnostic Usage

- **ID**: US-002
- **Description**: As a Claude user, I want clear conventions for Task Magic so that I can use it without Cursor-specific rules.
- **Acceptance Criteria**:
  - Agent guide provides complete conventions
  - Can create and manage tasks without .mdc files
  - File formats are self-explanatory

### 10.3 Context Preservation

- **ID**: US-003
- **Description**: As a developer, I want to store project context and decisions so that I can reference them when implementing tasks.
- **Acceptance Criteria**:
  - Each project has a context/ folder
  - Can store analysis, dependencies, decisions
  - Context is easily discoverable by AI agents

### 10.4 Project Discovery

- **ID**: US-004
- **Description**: As an AI agent, I want to discover what projects exist so that I can help users navigate and manage them.
- **Acceptance Criteria**:
  - INDEX.md provides central registry
  - Metadata headers enable relationship tracking
  - Can identify project boundaries clearly
