# Task Magic: Automagically create tasks for vibe coding projects

This system helps you manage your software projects by defining plans, breaking them down into actionable tasks, and keeping a memory of what's been done, all while working seamlessly with AI agents like Cursor.

One of the key goals is to avoid the "AI loop of death." ☠️

By breaking down work into smaller, focused tasks (each with a clear start, end, and test strategy), AI agents can tackle them effectively without losing context and making dumb mistakes.

The system provides permanent context through the `.ai/memory/` folder. This allows AI coding agents to see what has been built before and understand the how and why, helping them to ship new tasks more effectively.

## How it works

Task Magic is a file-based system. This means all your project plans, tasks, and history are stored in plain text files (mostly Markdown) right in your project's `.ai/` directory. This makes it easy to version control, track changes, and for AI agents to read and understand your project.

The system supports **multiple projects** with isolated workspaces and shared memory for cross-project learning.

There are four main parts to Task Magic:

1.  **Plans (`.ai/projects/{project}/plan.md`)**:

    - **Purpose**: This is where you define the "what" and "why" of your project or specific features. Think of these as your Product Requirements Documents (PRDs).
    - **Key files**:
      - `.ai/projects/{project}/plan.md`: The comprehensive PRD for your project.
      - `.ai/projects/{project}/context/{feature}-plan.md`: Detailed PRDs for specific features within the project.
      - `.ai/INDEX.md`: Global registry of all projects for discovery.
    - **AI interaction**: AI agents use these plans to understand the scope and requirements, helping to generate tasks.

2.  **Tasks (`.ai/projects/{project}/tasks/` & `.ai/projects/{project}/TASKS.md`)**:

    - **Purpose**: This is where the actual work items live. AI agents (or you) can break down plans into individual, manageable tasks.
    - **Key files & structure**:
      - `.ai/projects/{project}/tasks/task{id}_description.md`: Each task gets its own Markdown file. It includes details like status (pending, inprogress, completed), priority, dependencies, a description, and how to test it.
      - `.ai/projects/{project}/TASKS.md`: This is your project's master checklist. It's a human-friendly overview of all tasks in the project's tasks directory, showing their status at a glance. **This file and the individual task files are kept in sync by the AI.**
    - **AI interaction**: AI agents can create tasks from plans, update their status as they work on them, and help you manage dependencies.

3.  **Memory (`.ai/memory/`)**:

    - **Purpose**: Completed and failed tasks, as well as old plans, are archived here. This provides a valuable history for the AI to learn from and for you to reference across all projects.
    - **Key files**:
      - `.ai/memory/tasks/`: Archived task files from all projects.
      - `.ai/memory/TASKS_LOG.md`: A global log of when tasks were archived.
      - `.ai/memory/plans/`: Archived plan files from all projects.
      - `.ai/memory/PLANS_LOG.md`: A global log for archived plans.
    - **AI interaction**: The AI can consult the memory to understand how similar things were done in the past, or why a certain approach was taken.

4.  **Handoffs (`.ai/handoffs/`)**:
    - **Purpose**: Handoff files ensure smooth context transfer between AI assistant sessions or threads when working on a specific task. They provide a concise summary of current status, key findings, immediate next steps, and relevant files.
    - **Key files**:
      - `.ai/handoffs/task{id}_handoff{iteration}.md`: Task-specific handoff files named according to the task they pertain to.
    - **Content**: Each handoff includes project context, current situation & key findings, immediate next actions & goals, key files, and success criteria.
    - **AI interaction**: When switching between AI sessions or ending work before task completion, handoffs allow new AI instances to quickly understand context and continue productively.

## Working with AI agents (Cursor)

Task Magic is designed to work closely with AI agents. Here's how rules and context are handled:

- **The Index Rule (`_index.mdc`) - Your Rule Dispatcher**:

  - The file `.cursor/rules/task-magic/_index.mdc` serves as the **rule dispatcher** - it's **automatically included in every AI conversation** and tells the AI which specific rules to fetch based on your requests and detected conditions.
  - **Key Role**: The index doesn't contain detailed instructions, but rather **guides the AI to fetch the right specialized rules** for your specific needs.
  - **Always Active**: Unlike other rules that are fetched on-demand, the index is always present to help the AI navigate the rule system.
  - **Detection**: The index includes logic to detect legacy Task Magic structures and guide migration to the enhanced system.

- **Specialized Rules (fetched on-demand)**:

  - Other rule files (e.g., `tasks.mdc`, `plan.mdc`, `legacy.mdc` located in `.cursor/rules/task-magic/`) define specific behaviors or knowledge for the AI.
  - **Automatic Fetching**: The AI uses the index to determine which rules are needed and fetches them automatically.
  - **Manual Override**: You can explicitly @-tag specific rules if needed.

- **Your role: Guiding the AI with @-tags (when needed)**:
  - While the AI is usually good at figuring out which rules to use via the index, you can manually tag specific rules or files.
  - **For best results, @-tag specific rule files or directories in your prompts when you want to be explicit:**
    - `@task-magic/tasks create tasks for this feature`
    - `@task-magic/plan generate a plan for X`
    - `@task-magic/legacy help me migrate from the old system`
    - `@.ai/projects/my-project/TASKS.md what is the status of my project?`
    - `@.ai/projects/my-project/plan.md can you review this plan?`
  - This helps ensure the AI looks at the exact information you want it to.

## Getting started

1.  **Initialize `.ai/` structure**: If these directories don't exist, the AI will typically create them as needed when you ask it to create a plan or task. You can also create them manually:
    - `.ai/INDEX.md` (global project registry)
    - `.ai/projects/{your-project-name}/plan.md` (start with a simple project title and overview)
    - `.ai/projects/{your-project-name}/TASKS.md` (can start with just `# Project Tasks`)
    - `.ai/memory/TASKS_LOG.md` (can start with `# Task Archive Log`)
    - `.ai/handoffs/` (directory for task handoff files)
2.  **Create a plan**: Ask your AI assistant to create a new project plan using the planning rule (e.g., `@task-magic/plan create a plan for user authentication`).
3.  **Generate tasks**: Once a plan is ready, ask the AI to generate tasks from it (e.g., `@task-magic/tasks generate tasks for the user-authentication feature`).
4.  **Work on tasks**: Tell the AI to start working on tasks. It will update the project's `TASKS.md` and the individual task files as it progresses.
5.  **Create handoffs**: When switching AI sessions or ending work before task completion, ask the AI to create a handoff file to maintain context.
6.  **Archive**: Periodically, ask the AI to archive completed or failed tasks to keep your active task list clean.

## Migration from Legacy System

If you have an existing Task Magic setup with `.ai/tasks/` and `.ai/plans/PLAN.md`, the AI will automatically detect this and offer to migrate you to the enhanced project-scoped system. The migration preserves all your work while providing better organization and multi-project support.

By using Task Magic, you get a structured, AI-friendly way to manage your projects, ensuring both you and your AI assistants are always on the same page.
