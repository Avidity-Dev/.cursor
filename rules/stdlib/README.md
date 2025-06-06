# Cursor Stdlib Rule Pack

> **Transform Cursor from a reactive tool into an autonomous coding agent through systematic rule creation**

This is a comprehensive "standard library" (stdlib) of Cursor rules based on Geoffrey Huntley's revolutionary approach to AI-driven development. Instead of treating Cursor as just an IDE or search tool, these rules enable you to build a programmable system that learns from every interaction and solves entire classes of problems permanently.

## 🚀 Quick Start

1. Clone or copy these rules into your project's `.cursor/rules/` directory
2. Start using high-level requirements instead of low-level "implement XYZ" requests
3. When you solve a problem or make a mistake, ask Cursor to write a rule capturing the learning
4. Watch as your development environment becomes increasingly intelligent over time

## 📚 Core Concepts

### The Stdlib Approach

Traditional Cursor usage:

```
❌ "Implement a login function"
❌ "Fix this bug"
❌ "Add error handling"
```

Stdlib-powered Cursor usage:

```
✅ "Build a user authentication system with OAuth2, JWT tokens, and role-based permissions"
✅ "Study @SPECS.md and @.cursor rules, then implement what's missing"
✅ "Create a rule that captures how we handle API errors"
```

### Key Principles

1. **Cursor Writes Its Own Rules** - When you solve a problem, ask Cursor to write a rule preventing it from happening again
2. **Compose Like Unix Pipes** - Rules should be atomic and composable, working together to solve complex problems
3. **Continuous Learning** - Every mistake is a future rule; every discovery is shareable knowledge
4. **High-Level Thinking** - Focus on outcomes and requirements, not implementation details

## 📁 Rule Categories

### Foundation Rules

- `cursor-stdlib-foundation.mdc` - Core principles for using Cursor as an autonomous agent
- `rule-writing-meta.mdc` - How to write and evolve Cursor rules
- `learning-capture.mdc` - System for turning mistakes into permanent knowledge

### Automation Rules

- `auto-commit-conventional.mdc` - Automatic conventional commits after successful operations
- `auto-license-header.mdc` - Add license headers to new files automatically

### Development Workflow

- `requirements-driven-development.mdc` - Systematic approach to implementing features
- Additional workflow rules can be added for testing, deployment, etc.

## 🎯 Usage Patterns

### 1. Starting a New Feature

```bash
# First, discuss requirements with Cursor
"Let's build a notification system. Requirements:
1. Support email, SMS, and push notifications
2. Queue-based with retry logic
3. Template system for messages
4. Analytics and delivery tracking"

# Ask Cursor to document the requirements
"Write these requirements to specs/notification-system.md with numbered items and acceptance criteria"

# Begin implementation
"Study @specs/notification-system.md and @.cursor rules, implement the notification system"
```

### 2. Learning from Mistakes

```bash
# When something goes wrong
"That didn't work - the API is returning 404"

# Fix it, then capture the learning
"Write a Cursor rule that ensures all our API endpoints include trailing slashes,
store it in .cursor/rules/api-conventions.mdc"
```

### 3. Scaling with Concurrent Development

```bash
# Set up multiple work trees
git worktree add ../project-ui ui-development
git worktree add ../project-api api-development

# Launch separate Cursor instances for each domain
# Each works on non-overlapping specifications
```

## 🔧 Building Your Own Stdlib

### Step 1: Start with Foundation Rules

Begin by asking Cursor to create basic organizational rules:

```bash
"Create a Cursor rule that specifies where all rules should be stored
and how they should be named"
```

### Step 2: Add Project-Specific Knowledge

```bash
"Create a rule that captures our project's API conventions based on
the patterns in the /api directory"

"Write a rule specifying that we use Nix for builds, not Bazel,
with common Nix commands we use"
```

### Step 3: Capture Patterns as You Work

```bash
# After implementing something successfully
"Create a rule that captures the pattern for [what you just did]"

# After fixing a bug
"Update the [relevant-rule] to prevent [the bug] from happening again"
```

### Step 4: Evolve and Refine

```bash
# Periodically review and improve
"Look at all rules in @.cursor/rules. What's missing?
What doesn't follow best practices?"

# Consolidate similar rules
"Combine the error-handling rules into a single comprehensive rule"
```

## 📈 Advanced Techniques

### The Loopback Workflow

The key to hands-free development:

```bash
"Study @SPECS.md for functional specifications.
Study @.cursor for technical requirements
Implement what is not implemented
Create tests
Run build and verify the application works"
```

### Specification Domains

Organize your application into domains that can be developed concurrently:

```
src/
├── core/          # Implement first
├── ai/mcp_tools/  # Can be developed in parallel
├── ui/            # Can be developed in parallel
└── api/           # Can be developed in parallel
```

### Continuous Integration with Rules

Rules can trigger actions:

- Auto-format code on save
- Run tests after changes
- Commit when tests pass
- Deploy when builds succeed

## 🎓 Learning Resources

- [Original Blog Post: You are using Cursor AI incorrectly](https://ghuntley.com/stdlib/)
- [Follow-up: From Design doc to code](https://ghuntley.com/specs/)
- [Groundhog Project](https://github.com/ghuntley/groundhog) - Example implementation

## 🤝 Contributing

When contributing new rules:

1. Follow the existing naming convention: `category-specific-purpose.mdc`
2. Include concrete examples and anti-patterns
3. Make rules atomic and focused on one problem
4. Test the rule in practice before submitting
5. Update this README if adding new categories

## 💡 Tips for Success

1. **Start Small** - Don't try to create 100 rules on day one. Build them as you work.
2. **Be Specific** - Vague rules lead to vague results. Include exact commands and examples.
3. **Update Frequently** - When a rule fails, update it immediately with the learning.
4. **Think in Systems** - Look for patterns and create rules that solve entire categories of problems.
5. **Trust the Process** - It may feel uncomfortable letting go of low-level control, but the results speak for themselves.

## 🚦 Getting Started Checklist

- [ ] Copy rules to `.cursor/rules/` in your project
- [ ] Read through each rule to understand the patterns
- [ ] Try the loopback workflow on a small feature
- [ ] Create your first custom rule after solving a problem
- [ ] Ask Cursor to review and improve your rules
- [ ] Share your learnings and contribute back

---

> **Remember**: Every interaction with Cursor is an opportunity to build permanent knowledge. The goal is to reach a point where you can "unleash 1000 concurrent cursors" on your backlog, achieving weeks of work in hours.

Built with inspiration from [Geoffrey Huntley's](https://ghuntley.com) pioneering work on AI-driven development.
