"""Golden-file (snapshot) tests for analyzer behavior.

Each test case:
1. Reads a small Python sample from tests/golden/inputs/<case>/sample.py
2. Runs the appropriate analyzer
3. Normalizes output (deterministic IDs, sorted, no machine-specific paths)
4. Compares against tests/golden/expected/<case>.json

To update snapshots after an intentional change:
    pytest tests/test_golden.py --update-golden
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from brain_dev.analyzer import (
    DocsAnalyzer,
    RefactorAnalyzer,
    SecurityAnalyzer,
)

GOLDEN_DIR = Path(__file__).parent / "golden"
INPUTS_DIR = GOLDEN_DIR / "inputs"
EXPECTED_DIR = GOLDEN_DIR / "expected"


# ── Normalization helpers ─────────────────────────────────────────────

_ID_PATTERN = re.compile(r"^(sec_|doc_|complex_|ux_|dup_|name_).*$")


def _normalize_id(value: str) -> str:
    """Replace nondeterministic hash suffixes in IDs with a placeholder."""
    # e.g. "sec_a1b2c3d4" → "sec_<hash>"
    for prefix in ("sec_", "doc_", "complex_", "dup_", "name_", "ux_"):
        if value.startswith(prefix):
            return f"{prefix}<hash>"
    return value


def _normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize a single output dict for stable comparison."""
    out = {}
    for key, value in sorted(item.items()):
        if key.endswith("_id") and isinstance(value, str):
            out[key] = _normalize_id(value)
        elif isinstance(value, float):
            out[key] = round(value, 4)
        else:
            out[key] = value
    return out


def _sort_key(item: dict[str, Any]) -> tuple:
    """Deterministic sort: by location, then category/type, then description."""
    return (
        item.get("location", ""),
        item.get("category", item.get("suggestion_type", item.get("doc_type", ""))),
        item.get("description", item.get("reason", item.get("suggested_doc", ""))),
    )


def _normalize_output(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize and sort a list of analyzer output dicts."""
    normalized = [_normalize_item(d) for d in items]
    return sorted(normalized, key=_sort_key)


# ── Helpers for reading inputs ────────────────────────────────────────


def _read_sample(case_name: str) -> str:
    """Read the sample.py input for a golden test case."""
    path = INPUTS_DIR / case_name / "sample.py"
    return path.read_text(encoding="utf-8")


def _build_symbols_from_source(source: str, file_path: str) -> list[dict]:
    """Parse source into per-function symbol dicts for analyzers that need them."""
    import ast

    tree = ast.parse(source)
    symbols = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Extract the source lines for this function
            start = node.lineno - 1
            end = node.end_lineno if node.end_lineno else start + 1
            lines = source.splitlines()[start:end]
            func_source = "\n".join(lines)
            symbols.append({
                "name": node.name,
                "file_path": file_path,
                "line": node.lineno,
                "source_code": func_source,
            })
        elif isinstance(node, ast.ClassDef):
            symbols.append({
                "name": node.name,
                "symbol_type": "class",
                "file_path": file_path,
                "line": node.lineno,
                "source_code": "",
                "docstring": ast.get_docstring(node) or "",
            })
    return symbols


def _build_doc_symbols(source: str, file_path: str) -> list[dict]:
    """Build symbol dicts specifically for DocsAnalyzer."""
    import ast

    tree = ast.parse(source)
    symbols = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append({
                "name": node.name,
                "symbol_type": "function",
                "docstring": ast.get_docstring(node) or "",
                "file_path": file_path,
                "line": node.lineno,
            })
        elif isinstance(node, ast.ClassDef):
            symbols.append({
                "name": node.name,
                "symbol_type": "class",
                "docstring": ast.get_docstring(node) or "",
                "file_path": file_path,
                "line": node.lineno,
            })
    return symbols


# ── Snapshot comparison ───────────────────────────────────────────────


def _load_expected(case_name: str) -> list[dict[str, Any]] | None:
    """Load expected JSON, or None if it doesn't exist yet."""
    path = EXPECTED_DIR / f"{case_name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _save_expected(case_name: str, data: list[dict[str, Any]]) -> None:
    """Write expected JSON."""
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
    path = EXPECTED_DIR / f"{case_name}.json"
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _assert_golden(
    case_name: str,
    actual: list[dict[str, Any]],
    request: pytest.FixtureRequest,
) -> None:
    """Compare actual output against expected golden file."""
    normalized = _normalize_output(actual)

    if request.config.getoption("--update-golden"):
        _save_expected(case_name, normalized)
        pytest.skip(f"Updated golden file: {case_name}.json")
        return

    expected = _load_expected(case_name)
    if expected is None:
        _save_expected(case_name, normalized)
        pytest.skip(f"Created initial golden file: {case_name}.json (re-run to verify)")
        return

    assert normalized == expected, (
        f"Golden file mismatch for {case_name}.\n"
        f"If the change is intentional, run:\n"
        f"  pytest tests/test_golden.py --update-golden\n\n"
        f"Actual ({len(normalized)} items):\n{json.dumps(normalized, indent=2)}\n\n"
        f"Expected ({len(expected)} items):\n{json.dumps(expected, indent=2)}"
    )


# ── Test cases ────────────────────────────────────────────────────────


def test_golden_security_injection_patterns(request):
    """Snapshot: SecurityAnalyzer on known injection patterns."""
    source = _read_sample("security_injection_patterns")
    symbols = _build_symbols_from_source(source, "sample.py")

    analyzer = SecurityAnalyzer()
    issues = analyzer.analyze_security(symbols, severity_threshold="low")

    raw = [issue.to_dict() for issue in issues]
    _assert_golden("security_injection_patterns", raw, request)


def test_golden_doc_completeness(request):
    """Snapshot: DocsAnalyzer on mixed documentation quality."""
    source = _read_sample("doc_completeness")
    symbols = _build_doc_symbols(source, "sample.py")

    analyzer = DocsAnalyzer()
    suggestions = analyzer.analyze_docs(symbols, doc_style="google")

    raw = [s.to_dict() for s in suggestions]
    _assert_golden("doc_completeness", raw, request)


def test_golden_complexity_scoring(request):
    """Snapshot: RefactorAnalyzer complexity on various nesting depths."""
    source = _read_sample("complexity_scoring")
    symbols = _build_symbols_from_source(source, "sample.py")

    analyzer = RefactorAnalyzer()
    suggestions = analyzer.analyze_code(
        symbols=symbols,
        patterns=[],
        analysis_type="complexity",
    )

    raw = [s.to_dict() for s in suggestions]
    _assert_golden("complexity_scoring", raw, request)
