# Media Assets Guidance

## Recommended Visuals

Dev Brain's value is best communicated through diagrams, not screenshots.

### Priority diagrams to create:

1. **Reasoning Flow Diagram**
   - Show the orchestration loop
   - Decision points clearly marked
   - Input/output boundaries

2. **Tool Routing Sequence Diagram**
   - Request comes in
   - Brain evaluates context
   - Tool selection happens
   - Execution and result flow

3. **State Transitions Chart**
   - Agent states (planning, executing, waiting, complete)
   - Transition triggers
   - Error states and recovery

4. **Context Assembly Pipeline**
   - How context is gathered
   - Memory retrieval
   - Tool capability injection
   - Final prompt assembly

## Format Recommendations

| Format | Use Case |
|--------|----------|
| SVG | Primary choice — scales perfectly, editable |
| PNG | Fallback for complex diagrams |
| Mermaid | In-repo diagrams that can be edited as code |

## Style Guidelines

- Use consistent colors across all diagrams
- Prefer dark-mode friendly palettes
- Keep text readable at small sizes
- Include a legend for non-obvious symbols

## Tools

Recommended diagram tools:
- [Excalidraw](https://excalidraw.com) — hand-drawn style, exports SVG
- [Mermaid](https://mermaid.js.org) — code-based, GitHub-rendered
- [draw.io](https://draw.io) — full-featured, exports SVG

## Why Diagrams Matter

Orchestration is about **flow and coordination**.

Screenshots show static UI.
Diagrams show **how things connect and move**.

For Dev Brain, the architecture IS the product.
