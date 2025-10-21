#!/bin/bash

# spec-to-diagrams.sh - Generate architectural diagrams from specification documents
# Usage: claude spec-to-diagrams <spec-file-path> [output-file-path]

SPEC_FILE="$1"
OUTPUT_FILE="${2:-${SPEC_FILE%.*}_diagrams.md}"

if [ -z "$SPEC_FILE" ]; then
    echo "Usage: claude spec-to-diagrams <spec-file-path> [output-file-path]"
    echo "Example: claude spec-to-diagrams _parallel/ingestion_spec.md"
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: Specification file '$SPEC_FILE' not found"
    exit 1
fi

# Create the Claude prompt
PROMPT="I need you to analyze this specification document and create comprehensive Mermaid diagrams to help understand the architecture and implementation.

Please create diagrams that cover:

1. **System Structure** - Overall module/package organization
2. **Data Flow** - How data moves through the system
3. **Layered Architecture** - Separation of concerns and dependencies
4. **Processing Pipeline** - Step-by-step data transformation
5. **API Contracts** - Key types, interfaces, and data structures
6. **Implementation Timeline** - Migration phases or development stages
7. **Error Handling** - Exception hierarchy and error flows
8. **Backward Compatibility** - How legacy systems are supported (if applicable)

For each diagram:
- Use appropriate Mermaid diagram types (flowchart, sequenceDiagram, classDiagram, gantt, graph, etc.)
- Include clear titles and explanatory text
- Focus on the most important architectural concepts
- Make complex concepts visual and easy to understand

Generate a comprehensive markdown file with multiple diagrams and explanations, similar to how you would document a complex software architecture.

Here's the specification to analyze:

\`\`\`
$(cat "$SPEC_FILE")
\`\`\`"

echo "🔍 Analyzing specification: $SPEC_FILE"
echo "📊 Generating architectural diagrams..."
echo "💾 Output file: $OUTPUT_FILE"

# Use Claude to generate the diagrams
claude --no-stream "$PROMPT" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Successfully generated diagrams in: $OUTPUT_FILE"
    echo ""
    echo "📋 Generated diagrams typically include:"
    echo "   • System structure and module organization"
    echo "   • Data flow and processing pipelines" 
    echo "   • Layered architecture visualization"
    echo "   • API contracts and type definitions"
    echo "   • Implementation timeline and phases"
    echo "   • Error handling and exception flows"
    echo ""
    echo "🔍 View the diagrams: code $OUTPUT_FILE"
else
    echo "❌ Error generating diagrams"
    exit 1
fi