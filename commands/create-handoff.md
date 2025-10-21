# Agent Handoff Generator

Generate a structured handoff document to seamlessly transfer context and requirements to the next agent working on a project.

## Usage

This command will prompt you for key information to create a comprehensive handoff document that captures:
- Project context and current status
- What's been completed (with achievements)
- Current challenges or compromises made
- Next task requirements
- Implementation guidance
- Testing strategy
- Success criteria

## Command

```bash
# Prompt for handoff information
echo "=== AGENT HANDOFF GENERATOR ==="
echo ""

# Get basic project info
read -p "Project name: " project_name
read -p "Project ID (if applicable): " project_id
read -p "Task/phase being handed off: " task_name

echo ""
echo "=== COMPLETION STATUS ==="
read -p "What major work has been completed? " completed_work
read -p "Key achievements (optional): " achievements
read -p "Were any tests modified? (y/n): " tests_modified

echo ""
echo "=== CURRENT SITUATION ==="
read -p "Are there any current problems or compromises? (optional): " current_problems
read -p "Any critical context the next agent must know? (optional): " critical_context

echo ""
echo "=== NEXT TASK ==="
read -p "What is the next task/goal? " next_task
read -p "Priority level (high/medium/low): " priority
read -p "Key files to modify (comma-separated): " key_files

echo ""
echo "=== IMPLEMENTATION DETAILS ==="
read -p "Any specific implementation requirements? (optional): " implementation_details
read -p "What should be tested? (optional): " testing_requirements

# Generate the handoff document
cat << EOF

# ${task_name} - Agent Handoff

## Project Context

You are continuing work on **${project_name}**${project_id:+ (Project ${project_id})}. This handoff provides complete context for seamless continuation of the work.

## What Has Been Completed ✅

### ${completed_work}
- **Status**: COMPLETED
${achievements:+- **Key Achievements**: ${achievements}}
${tests_modified:+$([ "$tests_modified" = "y" ] && echo "- **Tests Modified**: Some test modifications were required - see details below")}

## Current Situation${current_problems:+ ⚠️}

${current_problems:+**Current Challenges/Compromises:**
${current_problems}

}${critical_context:+**Critical Context:**
${critical_context}

}## Your Task: ${next_task} 🎯

### Priority: ${priority}

### Requirements
${implementation_details:+- ${implementation_details}}
- Maintain backward compatibility with existing code
- Follow established patterns and conventions
- Update tests as needed

### Key Files to Modify
${key_files}

${testing_requirements:+### Testing Strategy
${testing_requirements}

}## Parallel System Integration ⚡

${project_id:+Track your progress using the Parallel MCP system:

\`\`\`python
# Check current project status
mcp__Parallel__get_tasks(project_id=${project_id})

# Create new task for this work
mcp__Parallel__create_task(
    project_id=${project_id},
    title="${next_task}",
    priority="${priority}"
)

# Update status and add notes as you work
mcp__Parallel__update_task_status(task_id=NEW_TASK_ID, status="in_progress")
mcp__Parallel__add_completion_notes(
    task_id=NEW_TASK_ID,
    implementation_details="What you implemented and how",
    decisions_made="Key technical decisions",
    test_results="Testing and verification performed"
)
\`\`\`

}## Success Criteria

- [ ] ${next_task} implemented correctly
- [ ] All existing tests continue to pass
${testing_requirements:+- [ ] ${testing_requirements}}
- [ ] Code follows project conventions and patterns
- [ ] Documentation updated as needed
${project_id:+- [ ] Task status updated in Parallel system with completion notes}

## Important Notes

- **DO NOT break existing functionality** - this is production code
- Read through existing code to understand patterns before making changes
- If you encounter unexpected behavior, investigate the root cause
- Document any compromises or trade-offs made during implementation

## Next Steps for YOU

1. Review the current codebase to understand the existing structure
${project_id:+2. Create/update task in Parallel system to track your work}
2. Implement the required changes following the specifications
3. Test thoroughly to ensure no regressions
4. Update documentation and add completion notes
5. Verify all success criteria are met

---

**Note**: This handoff was generated on $(date) using the create-handoff command.

EOF
```

## Tips for Effective Handoffs

1. **Be specific** about what was completed and what needs to be done next
2. **Include context** about why decisions were made or compromises chosen
3. **Highlight critical issues** that the next agent must be aware of
4. **Provide clear success criteria** so progress can be measured
5. **Include relevant file paths** and function names for quick orientation

## Example Usage

After running the command and providing the prompts, you'll get a structured markdown document that can be copied and used as the starting context for the next agent, ensuring smooth project continuation with full understanding of the current state and requirements.