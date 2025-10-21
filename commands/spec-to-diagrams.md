# Spec to Architecture Diagrams

Analyze a specification document and generate comprehensive Mermaid diagrams to visualize the architecture, data flow, and implementation details.

## Usage

```bash
claude spec-to-diagrams <spec-file-path> [output-file-path]
```

## What it does

1. **Reads and analyzes** the specification document
2. **Identifies key architectural concepts**:
   - Module/package structure
   - Data flow and processing pipelines
   - Layered architecture patterns
   - API contracts and types
   - Migration/implementation phases
   - Error handling strategies
3. **Generates comprehensive diagrams**:
   - Overall system structure
   - Processing flow diagrams
   - Layered architecture visualization
   - Sequence diagrams for complex flows
   - Class/type diagrams for contracts
   - Timeline diagrams for migration plans
   - Error taxonomy hierarchies
4. **Creates a markdown file** with all diagrams and explanations

## Example

```bash
claude spec-to-diagrams _parallel/ingestion_spec.md ingestion_diagrams.md
```

## Output

Creates a comprehensive markdown file with:
- Multiple Mermaid diagrams covering different aspects
- Explanatory text for each diagram
- Key benefits and architectural principles
- Visual representations of complex concepts from the spec

The command automatically infers the most useful diagram types based on the spec content and creates visualizations that help understand the system architecture, data flow, and implementation strategy.