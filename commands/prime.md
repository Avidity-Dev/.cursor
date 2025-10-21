# Context Prime: $ARGUMENTS

Load project context efficiently:

1. Parse arguments: project-name [--tests] [--no-src]

   - Default: include project files + source files
   - --tests: also include test files
   - --no-src: exclude source files

2. Execute these commands:

LIST: \_parallel/projects/{project-name}/

READ: \_parallel/projects/{project-name}/plan.md
READ: \_parallel/projects/{project-name}/progress_log.md
READ: \_parallel/projects/{project-name}/STATUS.md
READ: \_parallel/projects/{project-name}/TASKS.md
LIST: \_parallel/projects/{project-name}/tasks/
LIST: \_parallel/projects/{project-name}/memory/

3. Scan the content I just read for file paths mentioned in the text (patterns like src/_, tests/_, scripts/_, notebooks/_, etc.) and for each valid path found:

   - If it starts with "src/" and --no-src was NOT specified: READ that file
   - If it starts with "tests/" and --tests WAS specified: READ that file
   - For all other paths: READ that file

4. Finally:
   - READ: README.md
   - LIST: src/ (unless --no-src specified)
   - LIST: tests/ (if --tests specified)

Example usage:

- `/project:prime matching-service-integration` - Prime with project files and src (default)
- `/project:prime matching-service-integration --tests` - Include test files
- `/project:prime matching-service-integration --no-src --tests` - Only project and test files
