# Task Magic: Automagically create tasks for vibe coding projects

This system helps you manage your software projects by defining plans, breaking them down into actionable tasks, and keeping a memory of what's been done, all while working seamlessly with AI agents like Cursor.

One of the key goals is to avoid the "AI loop of death." ☠️

By breaking down work into smaller, focused tasks (each with a clear start, end, and test strategy), AI agents can tackle them effectively without losing context and making dumb mistakes.

The system provides permanent context through the `.ai/memory/` folder. This allows AI coding agents to see what has been built before and understand the how and why, helping them to ship new tasks more effectively.

## How it works

Task Magic is a file-based system. This means all your project plans, tasks, and history are stored in plain text files (mostly Markdown) right in your project's `.ai/` directory. This makes it easy to version control, track changes, and for AI agents to read and understand your project.

There are four main parts to Task Magic:

1.  **Plans (`.ai/plans/`)**:

    - **Purpose**: This is where you define the "what" and "why" of your project or specific features. Think of these as your Product Requirements Documents (PRDs).
    - **Key files**:
      - `.ai/plans/PLAN.md`: A global overview of your entire project. It should be a concise summary and index, linking to more detailed feature plans.
      - `.ai/plans/features/{your-feature}-plan.md`: Detailed PRDs for each specific feature you're building. This is where the AI will look for specifics when generating tasks.
    - **AI interaction**: AI agents use these plans to understand the scope and requirements, helping to generate tasks.

2.  **Tasks (`.ai/tasks/` & `.ai/TASKS.md`)**:

    - **Purpose**: This is where the actual work items live. AI agents (or you) can break down plans into individual, manageable tasks.
    - **Key files & structure**:
      - `.ai/tasks/task{id}_description.md`: Each task gets its own Markdown file. It includes details like status (pending, inprogress, completed), priority, dependencies, a description, and how to test it.
      - `.ai/TASKS.md`: This is your master checklist. It's a human-friendly overview of all tasks in the `.ai/tasks/` directory, showing their status at a glance. **This file and the individual task files are kept in sync by the AI.**
    - **AI interaction**: AI agents can create tasks from plans, update their status as they work on them, and help you manage dependencies.

3.  **Memory (`.ai/memory/`)**:
    - **Purpose**: Completed and failed tasks, as well as old plans, are archived here. This provides a valuable history for the AI to learn from and for you to reference.
    - **Key files**:
      - `.ai/memory/tasks/`: Archived task files.
      - `.ai/memory/TASKS_LOG.md`: A log of when tasks were archived.
      - `.ai/memory/plans/`: Archived plan files.
      - `.ai/memory/PLANS_LOG.md`: A log for archived plans.
    - **AI interaction**: The AI can consult the memory to understand how similar things were done in the past, or why a certain approach was taken.

4.  **Handoffs (`.ai/handoffs/`)**:
    - **Purpose**: Handoff files ensure smooth context transfer between AI assistant sessions or threads when working on a specific task. They provide a concise summary of current status, key findings, immediate next steps, and relevant files.
    - **Key files**:
      - `.ai/handoffs/task{id}_handoff{iteration}.md`: Task-specific handoff files named according to the task they pertain to.
    - **Content**: Each handoff includes project context, current situation & key findings, immediate next actions & goals, key files, and success criteria.
    - **AI interaction**: When switching between AI sessions or ending work before task completion, handoffs allow new AI instances to quickly understand context and continue productively.

## Working with AI agents (Cursor)

Task Magic is designed to work closely with AI agents. Here's how rules and context are handled:

- **Automatic context (`_index.md` files)**:

  - Files named `_index.md` (like the one in `.cursor/rules/.task-magic/_index.mdc`) provide a high-level overview of a system or a set of rules.
  - These `_index.md` files are **automatically included in the AI's context** when you're working within a project that uses them. This gives the AI a foundational understanding without you needing to do anything extra.

- **On-demand rules (other `.md` or `.mdc` rule files)**:

  - Other rule files (e.g., `tasks.mdc`, `plans.mdc`, `handoff.mdc` located in `.cursor/rules/.task-magic/`) define specific behaviors or knowledge for the AI.
  - Each of these rule files has a `description` in its header. The AI agent (Cursor) can read these descriptions and **decide dynamically whether a specific rule is relevant** to your current request or the task it's performing.
  - If the AI deems a rule relevant, it will "fetch" and use that rule.

- **Your role: Guiding the AI with @-tags**:
  - While the agent is usually pretty good at figuring out which rules to use, you can manually tag the rules you want to use.
  - **For best results, @-tag specific rule files or directories in your prompts.** For example:
    - `@.cursor/rules/.task-magic/tasks.mdc create tasks for this feature`
    - `@.cursor/rules/.task-magic/plans.mdc generate a plan for X`
    - `@.cursor/rules/.task-magic/handoff.mdc create a handoff for the current task`
    - `@TASKS.md what is the status of my project?` (to refer to the main task checklist)
    - `@.ai/plans/features/my-cool-feature-plan.md can you review this plan?`
  - This helps ensure the AI looks at the exact information you want it to.

## Getting started

1.  **Initialize `.ai/` structure**: If these directories don't exist, the AI will typically create them as needed when you ask it to create a plan or task. You can also create them manually.
    - `.ai/plans/PLAN.md` (start with a simple project title and overview)
    - `.ai/TASKS.md` (can start with just `# Project Tasks`)
    - `.ai/memory/TASKS_LOG.md` (can start with `# Task Archive Log`)
    - `.ai/handoffs/` (directory for task handoff files)
2.  **Create a plan**: Ask your AI assistant to create a new feature plan using the planning rule (e.g., `@.cursor/rules/.task-magic/plans.mdc create a plan for user authentication`).
3.  **Generate tasks**: Once a plan is ready, ask the AI to generate tasks from it (e.g., `@.cursor/rules/.task-magic/tasks.mdc generate tasks for the user-authentication-plan.md`).
4.  **Work on tasks**: Tell the AI to start working on tasks. It will update `.ai/TASKS.md` and the individual task files as it progresses.
5.  **Create handoffs**: When switching AI sessions or ending work before task completion, ask the AI to create a handoff file to maintain context.
6.  **Archive**: Periodically, ask the AI to archive completed or failed tasks to keep your active task list clean.

By using Task Magic, you get a structured, AI-friendly way to manage your projects, ensuring both you and your AI assistants are always on the same page.
