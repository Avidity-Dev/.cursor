# Guide: Importing Tasks from a CSV File into Linear

This guide outlines how to instruct the AI to import tasks from a CSV file into your Linear workspace using the available Linear integration tools.

## Prerequisites

1.  **A CSV File**: Your data should be in a CSV format, with each row representing a task and columns representing task attributes (e.g., Title, Description, Due Date).
2.  **Linear Access**: Ensure you have the necessary permissions in your Linear workspace.

## Steps to Instruct the AI for CSV Import

### 1. Prepare Your CSV Data

*   **Identify Key Columns**: Determine which columns in your CSV will map to Linear task fields. Common fields include:
    *   Task Title
    *   Task Description
    *   Assignee (you might need their Linear User ID)
    *   Due Date (must be in ISO format, e.g., `YYYY-MM-DD`)
    *   Priority (0 for None, 1 for Urgent, 2 for High, 3 for Medium, 4 for Low)
    *   Labels (you'll need Label IDs)
    *   State (you'll need the State ID, e.g., for '''Todo''', '''In Progress''')
*   **Provide the CSV**: You can either paste the CSV data directly in the chat or provide a path to the file if the AI has access to it.

### 2. Identify Necessary Linear IDs

Before tasks can be created, you'll need some identifiers from your Linear workspace. You can ask the AI to help you find these using the following tools:

*   **Team ID (`teamId`)**: This is **mandatory** for creating tasks.
    *   To find it, ask the AI to use `mcp_linear_list-teams` and identify the correct team.
*   **Assignee ID (`assigneeId`)** (Optional):
    *   If you want to assign tasks, you'll need the Linear User ID for each assignee. These usually need to be looked up in Linear directly or via its API, as there isn't a direct "get user by email/name" tool available here.
*   **Label IDs (`labelIds`)** (Optional):
    *   If you want to apply labels, ask the AI to help find these. This might involve you checking your Linear workspace for label names and then potentially the AI looking them up if a suitable tool becomes available, or you providing the IDs directly.
*   **Project ID (`projectId`)** (Optional):
    *   If tasks belong to a specific project, ask the AI to use `mcp_linear_get-projects` to find the `projectId`.
*   **Cycle ID (`cycleId`)** (Optional):
    *   If tasks belong to a specific cycle, ask the AI to use `mcp_linear_get-cycles` to find the `cycleId`.
*   **State ID (`stateId`)** (Optional):
    *   To set a specific workflow state (e.g., '''Todo''', '''In Progress'''), you'll need the `stateId`. These are specific to your team's workflow setup in Linear.

### 3. Instruct AI to Create Tasks

Once you have your CSV data and the necessary IDs:

*   **Specify the Mappings**: Clearly tell the AI how your CSV columns map to the parameters of the `mcp_linear_create-task` tool.
    *   Example: "For each row in the CSV:
        *   The '''Task Name''' column should be the `title`.
        *   The '''Details''' column should be the `description`.
        *   The '''Target Team ID''' is `your-team-id-here`.
        *   The '''Finish By''' column is the `dueDate`."
*   **Iterate and Create**: The AI will then conceptually iterate through each row of your CSV and use the `mcp_linear_create-task` tool to create a task in Linear.

**Example Instruction to AI (after providing CSV and getting IDs):**

"Please create Linear tasks from the provided CSV data.
- The `teamId` is '''abc-123-def-456'''.
- Map the CSV '''Summary''' column to the task `title`.
- Map the CSV '''Full Description''' column to the task `description`.
- Map the CSV '''Deadline''' column to the `dueDate`.
- If there's an '''Assign To User ID''' column in the CSV, use it for `assigneeId`."

### 4. Verification

*   After the AI reports completion, manually check your Linear workspace to ensure tasks have been created and populated correctly.
*   If there are issues, provide feedback to the AI with specific examples.

## Key Linear Tools for This Process

*   `mcp_linear_list-teams`: To find `teamId`.
*   `mcp_linear_get-projects`: To find `projectId`.
*   `mcp_linear_get-cycles`: To find `cycleId`.
*   `mcp_linear_create-task`: The primary tool for creating each task.

Remember to be clear and provide all necessary information (CSV data, column mappings, IDs) to the AI for a smooth import process. 