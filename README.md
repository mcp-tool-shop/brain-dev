# Dev Brain MCP Server

[![Tests](https://github.com/YOUR_USERNAME/dev-brain/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/dev-brain/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/YOUR_USERNAME/dev-brain)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligence layer for developer insights** - coverage analysis, test generation, refactoring suggestions, security audits, and UX insights via MCP.

## Features

- **9 Analysis Tools** - Coverage gaps, behavior analysis, test generation, refactoring, UX insights, security audits, and more
- **AST-Based Test Generation** - Automatically generate pytest tests with mocks that actually compile
- **Security Vulnerability Detection** - OWASP-style scanning for SQL injection, command injection, hardcoded secrets
- **Documentation Analysis** - Find missing docstrings and suggest templates
- **MCP Native** - Integrates seamlessly with Claude and other MCP clients

## Installation

```bash
pip install dev-brain
```

Or for development:

```bash
git clone https://github.com/YOUR_USERNAME/dev-brain.git
cd dev-brain
pip install -e ".[dev]"
```

## Quick Start

```bash
# Run the MCP server
dev-brain
```

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dev-brain": {
      "command": "dev-brain"
    }
  }
}
```

## Tools

### Analysis Tools

| Tool | Description |
|------|-------------|
| `coverage_analyze` | Compare observed patterns to test coverage, find gaps |
| `behavior_missing` | Find user behaviors not handled in code |
| `refactor_suggest` | Suggest refactoring based on complexity, duplication, naming |
| `ux_insights` | Extract UX insights from behavior patterns (dropoff, errors) |

### Generation Tools

| Tool | Description |
|------|-------------|
| `tests_generate` | Generate test suggestions for coverage gaps |
| `smart_tests_generate` | AST-based pytest generation with proper mocks and fixtures |
| `docs_generate` | Generate documentation templates for undocumented code |

### Security Tools

| Tool | Description |
|------|-------------|
| `security_audit` | Scan for vulnerabilities (SQL injection, command injection, secrets, etc.) |

### Utility Tools

| Tool | Description |
|------|-------------|
| `brain_stats` | Get server statistics and configuration |

## Example Usage

### Security Audit

```python
# Via MCP client
result = await client.call_tool("security_audit", {
    "symbols": [
        {
            "name": "execute_query",
            "file_path": "db.py",
            "line": 10,
            "source_code": "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")"
        }
    ],
    "severity_threshold": "medium"
})
# Returns: SQL injection vulnerability detected (CWE-89)
```

### Smart Test Generation

```python
result = await client.call_tool("smart_tests_generate", {
    "file_path": "/path/to/your/module.py"
})
# Returns complete pytest file with fixtures and mocks
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DEV BRAIN MCP SERVER                    │
├─────────────────────────────────────────────────────────────┤
│  Analyzers                                                   │
│  ├─ CoverageAnalyzer    (test gaps)                         │
│  ├─ BehaviorAnalyzer    (unhandled flows)                   │
│  ├─ RefactorAnalyzer    (complexity, naming)                │
│  ├─ UXAnalyzer          (dropoff, errors)                   │
│  ├─ DocsAnalyzer        (missing docs)                      │
│  └─ SecurityAnalyzer    (vulnerabilities)                   │
├─────────────────────────────────────────────────────────────┤
│  Generators                                                  │
│  ├─ TestGenerator       (skeleton tests)                    │
│  └─ SmartTestGenerator  (AST-based pytest)                  │
└─────────────────────────────────────────────────────────────┘
```

## Security Patterns Detected

| Category | Severity | CWE |
|----------|----------|-----|
| SQL Injection | Critical | CWE-89 |
| Command Injection | Critical | CWE-78 |
| Insecure Deserialization | Critical | CWE-502 |
| Hardcoded Secrets | High | CWE-798 |
| Path Traversal | High | CWE-22 |
| Insecure Crypto | Medium | CWE-327 |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=dev_brain --cov-report=html

# Type checking (optional)
mypy dev_brain
```

## Related Projects

- [Tool Compass](https://github.com/mikeyfrilot/tool-compass) - Semantic MCP tool discovery
- [Integradio](https://github.com/mikeyfrilot/integradio) - Semantic Gradio components

## License

MIT License - see [LICENSE](LICENSE) for details.
