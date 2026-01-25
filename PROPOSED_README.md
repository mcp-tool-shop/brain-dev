# Dev Brain

Orchestration and reasoning infrastructure for agent-based systems.

Dev Brain coordinates **tools, context, memory, and decision flow** — acting as the control plane for complex agent behavior.

---

## What problem does this solve?

As agent systems grow, execution logic becomes fragile:

- tool selection becomes ad-hoc
- reasoning chains are implicit
- context assembly is unclear
- failures are hard to debug
- behavior becomes non-deterministic

Dev Brain introduces **explicit orchestration**.

---

## Core responsibilities

- Reasoning flow coordination
- Tool invocation routing
- Context assembly and delegation
- Memory and state handoff
- Deterministic execution planning
- Structured intermediate reasoning

Dev Brain does not replace models — it manages how they are used.

---

## Conceptual example

```python
from dev_brain import Brain

brain = Brain(
    tools=[search, summarize, analyze],
    policies={"approval_required": True}
)

result = brain.run("Investigate recent changes")
```

(Example illustrative — see repo for real APIs.)

---

## When to use Dev Brain

- Multi-step agent workflows
- Tool-heavy reasoning
- Deterministic planning
- Long-running agent sessions
- Systems requiring observability

## When not to use it

- Single-call inference
- Stateless chat bots
- Simple scripts

---

## Design principles

- **Explicit > implicit**
- **Deterministic > emergent**
- **Observable > opaque**
- **Composable > monolithic**

---

## Project status

**Stable core / evolving orchestration strategies**

The orchestration engine is stable.
Routing heuristics may evolve.

---

## Ecosystem

Part of the [MCP Tool Shop](https://github.com/mcp-tool-shop) ecosystem.

Works especially well with:

- **Tool Compass** (tool selection)
- **Tool Scan** (capability inspection)
- **Context Window Manager** (context shaping)
- **Aspire AI** (goal evaluation)

---

## License

MIT
