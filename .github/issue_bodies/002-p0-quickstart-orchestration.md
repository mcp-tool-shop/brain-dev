# P0 — Add minimal orchestration quickstart

**Labels:** `docs`, `P0`

## Summary

Developers need a copy-paste runnable example to understand Dev Brain in under 2 minutes.

## Problem

Without a quickstart:
- Developers can't evaluate the project quickly
- Time-to-value is too high
- Concepts remain abstract

## Acceptance Criteria

- [ ] Copy-paste runnable example (works out of the box)
- [ ] One simple multi-tool workflow demonstrated
- [ ] Links to examples directory for more complex use cases
- [ ] Prerequisites clearly stated (Python version, dependencies)

## Suggested Structure

```markdown
## Quickstart

### Install
pip install dev-brain

### Basic Example
[runnable code here]

### What just happened?
[brief explanation]

### Next steps
- See examples/ for more
- Read the architecture guide
```

## Notes

The example should:
- Use 2-3 simple tools maximum
- Complete in <5 seconds
- Produce visible output
- Not require API keys for the basic demo
