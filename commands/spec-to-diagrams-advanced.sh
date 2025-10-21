#!/bin/bash

# spec-to-diagrams-advanced.sh - Generate architectural diagrams using specialized agent
# Usage: claude spec-to-diagrams-advanced <spec-file-path> [output-file-path]

SPEC_FILE="$1"
OUTPUT_FILE="${2:-${SPEC_FILE%.*}_architecture_diagrams.md}"

if [ -z "$SPEC_FILE" ]; then
    echo "Usage: claude spec-to-diagrams-advanced <spec-file-path> [output-file-path]"
    echo "Example: claude spec-to-diagrams-advanced _parallel/ingestion_spec.md"
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: Specification file '$SPEC_FILE' not found"
    exit 1
fi

echo "🔍 Analyzing specification: $SPEC_FILE"
echo "🤖 Using specialized documentation agent..."
echo "📊 Generating comprehensive architectural diagrams..."
echo "💾 Output file: $OUTPUT_FILE"

# Create the advanced prompt for the documentation agent
PROMPT="Please analyze the attached specification document and create a comprehensive set of Mermaid diagrams that visualize the architecture and implementation details.

Your approach should be:

1. **Read and understand the spec thoroughly** - identify key architectural concepts, data flows, components, and relationships

2. **Create 6-8 different diagram types** that each tell a different part of the story:
   - System/module structure (graph/flowchart)
   - Data processing pipeline (flowchart with subgraphs) 
   - Layered architecture showing dependencies (graph TB)
   - Sequence diagrams for complex interactions
   - Class/type diagrams for key contracts
   - Timeline/Gantt charts for implementation phases
   - Error handling hierarchy (graph TD)
   - Compatibility/migration strategy (if applicable)

3. **For each diagram**:
   - Choose the most appropriate Mermaid diagram type
   - Use clear, descriptive titles
   - Include explanatory text before each diagram
   - Focus on the most important architectural insights
   - Make complex concepts visual and intuitive

4. **Output format**: Create a well-structured markdown file with:
   - Clear headings for each diagram section
   - Brief explanations of what each diagram shows
   - A summary section highlighting key architectural benefits
   - Professional formatting suitable for technical documentation

5. **Quality criteria**:
   - Diagrams should be immediately understandable
   - Each diagram should provide unique value/perspective
   - Together they should give a complete picture of the system
   - Focus on architecture, not implementation details

Please read this specification file and create comprehensive architectural diagrams: $SPEC_FILE"

# Use Claude with the documentation-specialized prompt
claude --no-stream "$PROMPT" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Successfully generated comprehensive diagrams in: $OUTPUT_FILE"
    echo ""
    echo "📋 Typical diagram types generated:"
    echo "   🏗️  Overall system architecture and module structure"
    echo "   🔄 Data processing pipeline and flow visualization"
    echo "   📚 Layered architecture with clear separation of concerns"
    echo "   ⏱️  Sequence diagrams for complex interactions"
    echo "   📊 Type/contract diagrams for API interfaces"
    echo "   🗓️  Implementation timeline and migration phases"
    echo "   ⚠️  Error handling and exception hierarchies"
    echo "   🔄 Backward compatibility and migration strategies"
    echo ""
    echo "🔍 View the generated diagrams:"
    echo "   code $OUTPUT_FILE"
    echo ""
    echo "💡 Tip: These diagrams work great in VS Code with Mermaid preview extensions"
else
    echo "❌ Error generating diagrams"
    exit 1
fi