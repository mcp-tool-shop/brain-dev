# P1 — Document orchestration architecture and flow

**Labels:** `docs`, `P1`

## Summary

Developers need to understand how Dev Brain orchestrates agent behavior at an architectural level.

## Problem

Without architecture documentation:
- Integration decisions are harder
- Debugging is opaque
- Contributions are blocked

## Acceptance Criteria

- [ ] Diagram showing the reasoning loop
- [ ] Tool routing sequence explained
- [ ] Context handoff mechanism documented
- [ ] State management approach described

## Suggested Diagrams

### 1. Reasoning Loop
```
[Request] → [Context Assembly] → [Decision] → [Tool Selection] → [Execution] → [Result]
     ↑                                                                              |
     └──────────────────────────────────────────────────────────────────────────────┘
```

### 2. Component Overview
- Brain (coordinator)
- Tool Registry
- Context Manager
- State Store
- Policy Engine

### 3. Data Flow
Show how information moves through the system at each step.

## Format

Prefer Mermaid diagrams for maintainability, with SVG exports for README.

## Location

`docs/architecture.md` with diagrams in `docs/media/`
