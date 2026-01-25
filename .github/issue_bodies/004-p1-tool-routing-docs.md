# P1 — Document tool routing and decision logic

**Labels:** `docs`, `P1`

## Summary

Tool routing is core to Dev Brain's value. This needs clear documentation.

## Problem

Without routing documentation:
- Developers can't predict behavior
- Custom routing is blocked
- Debugging tool selection is guesswork

## Acceptance Criteria

- [ ] Routing rules explained (how tools are selected)
- [ ] Deterministic vs heuristic decisions distinguished
- [ ] Error and fallback behavior documented
- [ ] Custom routing hooks explained (if available)

## Suggested Content Structure

### How Tool Routing Works
1. Request analysis
2. Capability matching
3. Policy evaluation
4. Selection and execution

### Routing Modes
- **Deterministic** — rule-based, predictable
- **Heuristic** — model-assisted, flexible

### Configuration
How to customize routing behavior.

### Error Handling
- What happens when no tool matches
- Fallback strategies
- Retry logic

### Examples
```python
# Force specific tool
brain.run("task", force_tool="search")

# Exclude tools
brain.run("task", exclude=["dangerous_tool"])
```

## Location

`docs/tool-routing.md`
