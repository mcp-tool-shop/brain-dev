# P2 — Add observability and debugging guidance

**Labels:** `docs`, `P2`

## Summary

Orchestration systems need visibility. Dev Brain should document how to observe and debug agent behavior.

## Problem

Without observability docs:
- Production debugging is painful
- Performance optimization is blind
- Trust in the system is lower

## Acceptance Criteria

- [ ] Logging strategy documented
- [ ] Trace examples provided
- [ ] Failure diagnosis workflow explained
- [ ] Metrics/telemetry approach described (if applicable)

## Suggested Content

### Logging

```python
import logging
logging.getLogger("dev_brain").setLevel(logging.DEBUG)
```

Explain log levels and what each reveals.

### Tracing

Show how to trace a request through the system:
- Request ID
- Tool invocations
- Decision points
- Timing information

### Debugging Workflow

1. **Symptom**: Wrong tool selected
   - Check: routing rules, context, tool capabilities

2. **Symptom**: Infinite loop
   - Check: termination conditions, state transitions

3. **Symptom**: Slow execution
   - Check: tool latency, context size, routing overhead

### Production Considerations

- Log retention
- Sensitive data handling
- Performance impact of logging levels

## Location

`docs/observability.md`
