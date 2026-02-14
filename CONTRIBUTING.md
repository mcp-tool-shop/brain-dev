# Contributing to Dev Brain

Dev Brain is an MCP server that provides AI-powered code analysis tools. Contributions are welcome!

## Local Development

```bash
git clone https://github.com/mcp-tool-shop-org/brain-dev.git
cd brain-dev
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
brain-dev            # run the MCP server
```

Requires **Python 3.11+** (CI tests 3.11, 3.12, 3.13, 3.14).

## How to Contribute

### Reporting Issues

1. Check existing [issues](https://github.com/mcp-tool-shop-org/brain-dev/issues)
2. If not found, create a new issue using the provided bug report or feature request template

### Contributing Code

1. **Fork the repository** and create a branch from `main`
2. **Make your changes** — follow existing code style, use type hints, add tests
3. **Test your changes**
   ```bash
   pytest                                                       # run all tests
   pytest tests/ -v --cov=brain_dev --cov-report=term-missing   # with coverage
   ```
4. **Commit** with clear, descriptive messages; reference issue numbers when applicable
5. **Submit a pull request** using the PR template

## Project Structure

```
brain-dev/
├── brain_dev/
│   ├── __init__.py
│   ├── server.py               # MCP server, TOOL_DEFINITIONS registry, handlers
│   ├── analyzer.py             # All analyzer classes + dataclasses
│   ├── smart_test_generator.py # AST-based pytest file generator
│   └── config.py               # DevBrainConfig dataclass
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── test_server.py          # Server + handler tests
│   ├── test_analyzer.py        # Core analyzer tests
│   ├── test_new_analyzers.py   # Docs + Security analyzer tests
│   ├── test_smart_generator.py # Smart test generator tests
│   ├── test_integration.py     # End-to-end workflow tests
│   └── test_coverage_gaps.py   # Edge-case coverage tests
├── pyproject.toml              # Build config, deps, entry point
└── CHANGELOG.md
```

## Adding New Analysis Tools

The tool registry lives in `brain_dev/server.py`:

1. Add a `Tool(...)` entry to the `TOOL_DEFINITIONS` list
2. Write a `def handle_<tool_name>(args: dict) -> list[TextContent]` handler inside `create_server()`
3. Map the name to the handler in the `_HANDLERS` dict
4. Add tests in `tests/`
5. Update `CHANGELOG.md`

## MCP Tools (source of truth: `TOOL_DEFINITIONS` in server.py)

| Tool | Description |
|------|-------------|
| `coverage_analyze` | Test coverage gap detection |
| `behavior_missing` | Find unhandled user behaviours |
| `tests_generate` | Test suggestions from coverage gaps |
| `smart_tests_generate` | AST-powered pytest file generation |
| `refactor_suggest` | Complexity, duplication, naming analysis |
| `ux_insights` | Dropoff and error-pattern detection |
| `docs_generate` | Documentation gap finder |
| `security_audit` | OWASP vulnerability scanning with CWE mapping |
| `brain_stats` | Server statistics and health |

## Code Quality

- **Type hints** on all functions
- **AST analysis**: use `ast.parse()` / `ast.walk()`; handle `SyntaxError` gracefully (return empty / fallback)
- **MCP convention**: handlers return `list[TextContent]` with JSON; never crash on bad input

## Release Process

(For maintainers)

1. Bump `version` in `pyproject.toml`
2. Add a new section to `CHANGELOG.md` under `## [x.y.z] - YYYY-MM-DD`
3. Commit: `git commit -m "release: vX.Y.Z"`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push origin main --tags`
6. Create a GitHub Release from the tag — the publish workflow uploads to PyPI automatically

## Questions?

Open an issue or start a discussion in the [mcp-tool-shop-org](https://github.com/mcp-tool-shop-org) organization.
