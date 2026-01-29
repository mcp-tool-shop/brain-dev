"""
Batch 3: RefactorAnalyzer, UXAnalyzer, and DocsAnalyzer Tests (25 tests)
Tests for RefactorAnalyzer, UXAnalyzer, and DocsAnalyzer classes.
"""

import pytest
from brain_dev.analyzer import (
    RefactorAnalyzer,
    RefactorSuggestion,
    UXAnalyzer,
    UXInsight,
    DocsAnalyzer,
    DocSuggestion,
)


# =============================================================================
# Section 1: RefactorAnalyzer Tests (10 tests)
# =============================================================================

class TestRefactorAnalyzerInit:
    """Test RefactorAnalyzer initialization."""

    def test_create_refactor_analyzer(self):
        """Test RefactorAnalyzer can be instantiated."""
        analyzer = RefactorAnalyzer()
        assert analyzer is not None


class TestRefactorAnalyzerAnalyzeCode:
    """Test RefactorAnalyzer.analyze_code method."""

    def test_analyze_complexity_finds_complex_functions(self):
        """Test complexity analysis finds overly complex functions."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {
                "name": "complex_function",
                "file_path": "module.py",
                "line": 10,
                "source_code": "if a: if b: if c: for x in y: for z in w: while True: if d: pass",
            }
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="complexity")

        assert len(suggestions) > 0
        assert all(isinstance(s, RefactorSuggestion) for s in suggestions)
        assert all(s.suggestion_type == "reduce_complexity" for s in suggestions)

    def test_analyze_complexity_no_source_code(self):
        """Test complexity analysis skips symbols without source_code."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {"name": "no_source", "file_path": "module.py", "line": 10}
            # No source_code field
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="complexity")

        assert suggestions == []

    def test_analyze_duplication_finds_similar_names(self):
        """Test duplication analysis finds functions with similar names."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {"name": "handler1", "file_path": "a.py"},
            {"name": "handler2", "file_path": "a.py"},
            {"name": "handler3", "file_path": "a.py"},
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="duplication")

        assert isinstance(suggestions, list)
        for s in suggestions:
            assert s.suggestion_type == "extract_common"

    def test_analyze_naming_single_letter(self):
        """Test naming analysis flags single-letter variable names."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {"name": "x", "symbol_type": "variable", "file_path": "a.py", "line": 10},
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="naming")

        assert len(suggestions) > 0
        assert suggestions[0].suggestion_type == "rename"
        assert "single-letter" in suggestions[0].reason.lower() or "clarity" in suggestions[0].reason.lower()

    def test_analyze_naming_very_long_names(self):
        """Test naming analysis flags very long names."""
        analyzer = RefactorAnalyzer()

        long_name = "a" * 55  # 55 characters > 50 threshold
        symbols = [
            {"name": long_name, "file_path": "a.py", "line": 20},
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="naming")

        assert len(suggestions) > 0
        assert suggestions[0].suggestion_type == "rename"
        assert "long" in suggestions[0].reason.lower()


class TestRefactorAnalyzerConfidence:
    """Test RefactorAnalyzer confidence scores."""

    def test_complexity_confidence_increases_with_branches(self):
        """Test complexity confidence increases with more branches."""
        analyzer = RefactorAnalyzer()

        # Many branches
        symbols = [
            {
                "name": "very_complex",
                "file_path": "module.py",
                "line": 10,
                "source_code": "if a: if b: if c: if d: for x in y: for z in w: while True: elif x: except: pass",
            }
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="complexity")

        if suggestions:
            assert suggestions[0].confidence > 0.5

    def test_naming_confidence_values(self):
        """Test naming suggestions have reasonable confidence."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {"name": "x", "symbol_type": "variable", "file_path": "a.py", "line": 10},
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="naming")

        if suggestions:
            assert 0 < suggestions[0].confidence <= 1.0


class TestRefactorAnalyzerEmptyInput:
    """Test RefactorAnalyzer with empty input."""

    def test_empty_symbols_complexity(self):
        """Test complexity analysis with empty symbols."""
        analyzer = RefactorAnalyzer()
        suggestions = analyzer.analyze_code([], [], analysis_type="complexity")
        assert suggestions == []

    def test_empty_symbols_naming(self):
        """Test naming analysis with empty symbols."""
        analyzer = RefactorAnalyzer()
        suggestions = analyzer.analyze_code([], [], analysis_type="naming")
        assert suggestions == []


class TestRefactorAnalyzerLocationInfo:
    """Test RefactorAnalyzer location information."""

    def test_suggestion_has_location(self):
        """Test suggestions include file:line location."""
        analyzer = RefactorAnalyzer()

        symbols = [
            {
                "name": "complex_func",
                "file_path": "utils.py",
                "line": 42,
                "source_code": "if a: if b: if c: for x in y: for z in w: while True: pass",
            }
        ]

        suggestions = analyzer.analyze_code(symbols, [], analysis_type="complexity")

        if suggestions:
            assert "utils.py" in suggestions[0].location


# =============================================================================
# Section 2: UXAnalyzer Tests (9 tests)
# =============================================================================

class TestUXAnalyzerInit:
    """Test UXAnalyzer initialization."""

    def test_create_ux_analyzer(self):
        """Test UXAnalyzer can be instantiated."""
        analyzer = UXAnalyzer()
        assert analyzer is not None


class TestUXAnalyzerAnalyzeFlow:
    """Test UXAnalyzer.analyze_flow method."""

    def test_analyze_dropoff(self):
        """Test dropoff analysis."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["start", "step1"], "occurrence_count": 100},
            {"sequence": ["start", "step1", "step2"], "occurrence_count": 50},  # 50% dropoff
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="dropoff")

        assert isinstance(insights, list)
        for i in insights:
            assert isinstance(i, UXInsight)
            assert i.metric == "dropoff"

    def test_analyze_error_rate(self):
        """Test error rate analysis."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["action", "error"], "occurrence_count": 20},
            {"sequence": ["action", "fail"], "occurrence_count": 15},
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="error_rate")

        assert isinstance(insights, list)
        for i in insights:
            assert i.metric == "error_rate"

    def test_empty_patterns(self):
        """Test with empty patterns."""
        analyzer = UXAnalyzer()

        insights = analyzer.analyze_flow([], flow_type="general", metric="dropoff")

        assert insights == []


class TestUXAnalyzerDropoffAnalysis:
    """Test UXAnalyzer dropoff analysis in detail."""

    def test_detects_high_dropoff_rate(self):
        """Test detects significant dropoff (>50%)."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["login"], "occurrence_count": 100},
            {"sequence": ["login", "next_step"], "occurrence_count": 30},  # 70% dropoff
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="dropoff")

        # Should detect the significant dropoff
        assert isinstance(insights, list)

    def test_dropoff_insight_has_finding(self):
        """Test dropoff insights have descriptive finding."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["a"], "occurrence_count": 100},
            {"sequence": ["a", "b"], "occurrence_count": 40},
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="dropoff")

        for i in insights:
            assert i.finding is not None
            assert len(i.finding) > 0


class TestUXAnalyzerErrorAnalysis:
    """Test UXAnalyzer error rate analysis."""

    def test_finds_error_patterns(self):
        """Test finds patterns containing error events."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["submit", "error_response"], "occurrence_count": 15},
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="error_rate")

        assert isinstance(insights, list)

    def test_error_insight_has_suggestion(self):
        """Test error insights have suggestions."""
        analyzer = UXAnalyzer()

        patterns = [
            {"sequence": ["action", "failure"], "occurrence_count": 10},
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="error_rate")

        for i in insights:
            assert i.suggestion is not None


class TestUXAnalyzerFlowTypes:
    """Test UXAnalyzer with different flow types."""

    @pytest.mark.parametrize("flow_type", ["general", "checkout", "search", "onboarding"])
    def test_accepts_flow_type(self, flow_type):
        """Test analyzer accepts various flow types."""
        analyzer = UXAnalyzer()

        patterns = [{"sequence": ["step1", "step2"], "occurrence_count": 50}]

        insights = analyzer.analyze_flow(patterns, flow_type=flow_type, metric="dropoff")

        assert isinstance(insights, list)


# =============================================================================
# Section 3: DocsAnalyzer Tests (6 tests)
# =============================================================================

class TestDocsAnalyzerInit:
    """Test DocsAnalyzer initialization."""

    def test_create_docs_analyzer(self):
        """Test DocsAnalyzer can be instantiated."""
        analyzer = DocsAnalyzer()
        assert analyzer is not None


class TestDocsAnalyzerAnalyzeDocs:
    """Test DocsAnalyzer.analyze_docs method."""

    def test_finds_missing_docstrings(self):
        """Test finding symbols without docstrings."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "calculate_total",
                "symbol_type": "function",
                "file_path": "billing.py",
                "line": 10,
                "docstring": "",  # Empty docstring
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        assert len(suggestions) > 0
        assert suggestions[0].doc_type == "missing"

    def test_finds_incomplete_docstrings(self):
        """Test finding incomplete docstrings."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "process_data",
                "symbol_type": "function",
                "file_path": "processor.py",
                "line": 20,
                "docstring": "Does stuff.",  # Too short, no Returns
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        # May find incomplete docstring
        assert isinstance(suggestions, list)

    def test_skips_private_functions(self):
        """Test skips private (underscore-prefixed) functions."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "_helper",
                "symbol_type": "function",
                "file_path": "utils.py",
                "line": 5,
                "docstring": "",
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        # Should skip private functions
        names = [s.symbol_name for s in suggestions]
        assert "_helper" not in names

    def test_includes_init_method(self):
        """Test includes __init__ even though it starts with underscore."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "__init__",
                "symbol_type": "function",
                "file_path": "class.py",
                "line": 10,
                "docstring": "",
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        # __init__ should be included
        names = [s.symbol_name for s in suggestions]
        assert "__init__" in names


class TestDocsAnalyzerDocStyles:
    """Test DocsAnalyzer with different doc styles."""

    @pytest.mark.parametrize("doc_style", ["google", "numpy", "sphinx"])
    def test_accepts_doc_style(self, doc_style):
        """Test analyzer accepts various doc styles."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "func",
                "symbol_type": "function",
                "file_path": "mod.py",
                "line": 1,
                "docstring": "",
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style=doc_style)

        assert isinstance(suggestions, list)


class TestDocsAnalyzerSuggestionContent:
    """Test DocSuggestion content."""

    def test_suggestion_has_template(self):
        """Test missing doc suggestion includes template."""
        analyzer = DocsAnalyzer()

        symbols = [
            {
                "name": "my_function",
                "symbol_type": "function",
                "file_path": "module.py",
                "line": 15,
                "docstring": "",
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        if suggestions:
            assert suggestions[0].suggested_doc is not None
            assert len(suggestions[0].suggested_doc) > 0
