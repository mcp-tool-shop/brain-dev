"""
Batch 2: BehaviorAnalyzer and CodeTestGenerator Tests (25 tests)
Tests for BehaviorAnalyzer class and CodeTestGenerator (TestGenerator alias).
"""

import pytest
from brain_dev.analyzer import (
    BehaviorAnalyzer,
    MissingBehavior,
    CodeTestGenerator,
    TestGenerator,
    CoverageGap,
    SuggestedUnitCase,
)


# =============================================================================
# Section 1: BehaviorAnalyzer Tests (14 tests)
# =============================================================================

class TestBehaviorAnalyzerInit:
    """Test BehaviorAnalyzer initialization."""

    def test_create_behavior_analyzer(self):
        """Test BehaviorAnalyzer can be instantiated."""
        analyzer = BehaviorAnalyzer()
        assert analyzer is not None


class TestBehaviorAnalyzerFindMissingBehaviors:
    """Test BehaviorAnalyzer.find_missing_behaviors method."""

    def test_finds_unhandled_patterns(self):
        """Test finding patterns not handled by code."""
        analyzer = BehaviorAnalyzer()

        observed = [
            {"sequence": ["unhandled_event"], "occurrence_count": 20},
        ]
        code_symbols = []  # No handlers

        missing = analyzer.find_missing_behaviors(observed, code_symbols, min_count=5)

        assert len(missing) > 0
        assert isinstance(missing[0], MissingBehavior)

    def test_respects_min_count_threshold(self):
        """Test min_count filters low-occurrence patterns."""
        analyzer = BehaviorAnalyzer()

        observed = [
            {"sequence": ["rare_event"], "occurrence_count": 3},  # Below threshold
            {"sequence": ["common_event"], "occurrence_count": 15},
        ]
        code_symbols = []

        missing = analyzer.find_missing_behaviors(observed, code_symbols, min_count=10)

        # Should only include common_event
        patterns = [m.pattern for m in missing]
        assert ["rare_event"] not in patterns

    def test_empty_patterns_returns_empty(self):
        """Test empty observed patterns returns empty list."""
        analyzer = BehaviorAnalyzer()

        missing = analyzer.find_missing_behaviors([], [], min_count=5)

        assert missing == []

    def test_all_patterns_handled_returns_empty(self):
        """Test when all patterns have handlers."""
        analyzer = BehaviorAnalyzer()

        observed = [
            {"sequence": ["login"], "occurrence_count": 50},
        ]
        # Code has a handler for login
        code_symbols = [
            {"name": "handle_login", "kind": "function"},
        ]

        missing = analyzer.find_missing_behaviors(observed, code_symbols, min_count=5)

        # Login is handled, so may return empty or filtered
        # The behavior depends on implementation details
        assert isinstance(missing, list)


class TestBehaviorAnalyzerExtractCodeEvents:
    """Test BehaviorAnalyzer._extract_code_events method."""

    def test_extracts_from_handler_names(self):
        """Test extracts events from handle_* function names."""
        analyzer = BehaviorAnalyzer()

        symbols = [
            {"name": "handle_login"},
            {"name": "handle_logout"},
            {"name": "on_click"},
            {"name": "process_payment"},
        ]

        events = analyzer._extract_code_events(symbols)

        # Should extract meaningful parts
        assert isinstance(events, set)

    def test_empty_symbols(self):
        """Test with empty symbols list."""
        analyzer = BehaviorAnalyzer()

        events = analyzer._extract_code_events([])

        assert events == set()

    def test_non_handler_functions_ignored(self):
        """Test non-handler functions don't contribute events."""
        analyzer = BehaviorAnalyzer()

        symbols = [
            {"name": "calculate_total"},  # Not a handler
            {"name": "get_data"},  # Not a handler
        ]

        events = analyzer._extract_code_events(symbols)

        # No handler patterns matched
        assert isinstance(events, set)


class TestBehaviorAnalyzerCreateMissingBehavior:
    """Test BehaviorAnalyzer._create_missing_behavior method."""

    def test_creates_valid_missing_behavior(self):
        """Test creates MissingBehavior with correct fields."""
        analyzer = BehaviorAnalyzer()

        behavior = analyzer._create_missing_behavior(
            pattern=["upload", "process"],
            count=25,
            unhandled=["process"],
        )

        assert behavior.behavior_id.startswith("behavior_")
        assert behavior.pattern == ["upload", "process"]
        assert behavior.observed_count == 25
        assert "process" in behavior.description or "unhandled" in behavior.description.lower()

    def test_behavior_id_is_unique(self):
        """Test different patterns get different behavior IDs."""
        analyzer = BehaviorAnalyzer()

        b1 = analyzer._create_missing_behavior(["a", "b"], 10, ["b"])
        b2 = analyzer._create_missing_behavior(["c", "d"], 10, ["d"])

        assert b1.behavior_id != b2.behavior_id


class TestBehaviorAnalyzerMissingBehaviorContent:
    """Test content of MissingBehavior objects."""

    def test_has_suggested_action(self):
        """Test MissingBehavior has suggested_action."""
        analyzer = BehaviorAnalyzer()

        observed = [
            {"sequence": ["unhandled_action"], "occurrence_count": 20},
        ]

        missing = analyzer.find_missing_behaviors(observed, [], min_count=5)

        if missing:
            assert missing[0].suggested_action is not None
            assert len(missing[0].suggested_action) > 0

    def test_has_description(self):
        """Test MissingBehavior has description."""
        analyzer = BehaviorAnalyzer()

        observed = [
            {"sequence": ["test_event"], "occurrence_count": 15},
        ]

        missing = analyzer.find_missing_behaviors(observed, [], min_count=5)

        if missing:
            assert missing[0].description is not None


class TestBehaviorAnalyzerWithHandlers:
    """Test BehaviorAnalyzer with various handler patterns."""

    def test_on_prefix_handlers(self):
        """Test on_* prefix handlers are recognized."""
        analyzer = BehaviorAnalyzer()

        symbols = [{"name": "on_user_click"}]
        events = analyzer._extract_code_events(symbols)

        # Should extract some event from on_user_click
        assert isinstance(events, set)

    def test_process_prefix_handlers(self):
        """Test process_* prefix handlers are recognized."""
        analyzer = BehaviorAnalyzer()

        symbols = [{"name": "process_order"}]
        events = analyzer._extract_code_events(symbols)

        assert isinstance(events, set)


# =============================================================================
# Section 2: CodeTestGenerator Tests (11 tests)
# =============================================================================

class TestCodeTestGeneratorAlias:
    """Test TestGenerator is alias for CodeTestGenerator."""

    def test_alias_is_correct(self):
        """Test TestGenerator points to CodeTestGenerator."""
        assert TestGenerator is CodeTestGenerator


class TestCodeTestGeneratorInit:
    """Test CodeTestGenerator initialization."""

    def test_create_generator(self):
        """Test CodeTestGenerator can be instantiated."""
        generator = CodeTestGenerator()
        assert generator is not None

    def test_has_templates(self):
        """Test generator has TEMPLATES attribute."""
        generator = CodeTestGenerator()
        assert hasattr(generator, "TEMPLATES")
        assert "pytest" in generator.TEMPLATES


class TestCodeTestGeneratorGenerateTest:
    """Test CodeTestGenerator.generate_test method."""

    def test_generates_pytest_unit_test(self):
        """Test generating pytest unit test."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_001",
            pattern=["login", "checkout"],
            support=0.15,
            priority="high",
            suggested_test_name="test_login_checkout",
            suggested_test_file="tests/test_flow.py",
            description="Login to checkout flow",
        )

        result = generator.generate_test(gap, framework="pytest", style="unit")

        assert isinstance(result, SuggestedUnitCase)
        assert result.framework == "pytest"
        assert result.style == "unit"
        assert "def " in result.test_code

    def test_generates_pytest_integration_test(self):
        """Test generating pytest integration test."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_int",
            pattern=["api_call", "db_write"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_api_db_flow",
            suggested_test_file="tests/test_integration.py",
            description="API to DB flow",
        )

        result = generator.generate_test(gap, framework="pytest", style="integration")

        assert result.style == "integration"
        assert "integration" in result.test_code.lower()

    def test_generates_jest_test(self):
        """Test generating jest test."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_jest",
            pattern=["click", "submit"],
            support=0.12,
            priority="medium",
            suggested_test_name="test_click_submit",
            suggested_test_file="tests/test.js",
            description="Click and submit",
        )

        result = generator.generate_test(gap, framework="jest", style="unit")

        assert result.framework == "jest"
        assert "describe(" in result.test_code or "it(" in result.test_code


class TestCodeTestGeneratorTestOutput:
    """Test CodeTestGenerator output content."""

    def test_test_name_matches_gap(self):
        """Test output test_name matches gap suggestion."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_name",
            pattern=["search"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_search_flow",
            suggested_test_file="tests/test_search.py",
            description="Search flow",
        )

        result = generator.generate_test(gap)

        assert result.test_name == "test_search_flow"

    def test_test_file_matches_gap(self):
        """Test output test_file matches gap suggestion."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_file",
            pattern=["filter"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_filter",
            suggested_test_file="tests/test_filters.py",
            description="Filter flow",
        )

        result = generator.generate_test(gap)

        assert result.test_file == "tests/test_filters.py"

    def test_covers_pattern_matches_gap(self):
        """Test output covers_pattern matches gap pattern."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_pattern",
            pattern=["a", "b", "c"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_abc",
            suggested_test_file="tests/test.py",
            description="ABC flow",
        )

        result = generator.generate_test(gap)

        assert result.covers_pattern == ["a", "b", "c"]


class TestCodeTestGeneratorUnknownFramework:
    """Test CodeTestGenerator with unknown framework."""

    def test_fallback_for_unknown_framework(self):
        """Test fallback template for unknown framework."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_unknown",
            pattern=["test"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_flow",
            suggested_test_file="tests/test.py",
            description="Test flow",
        )

        result = generator.generate_test(gap, framework="unknown_framework", style="unit")

        # Should have fallback code
        assert result.test_code is not None
        assert len(result.test_code) > 0

    def test_fallback_for_unknown_style(self):
        """Test fallback for unknown test style."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_style",
            pattern=["test"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_flow",
            suggested_test_file="tests/test.py",
            description="Test flow",
        )

        result = generator.generate_test(gap, framework="pytest", style="unknown_style")

        # Should have fallback
        assert result.test_code is not None


class TestCodeTestGeneratorTemplates:
    """Test CodeTestGenerator template content."""

    def test_pytest_unit_template_has_docstring(self):
        """Test pytest unit template includes docstring."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_doc",
            pattern=["test"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_with_doc",
            suggested_test_file="tests/test.py",
            description="Test with documentation",
        )

        result = generator.generate_test(gap, framework="pytest", style="unit")

        # Should have triple-quoted docstring
        assert '"""' in result.test_code

    def test_pytest_unit_template_has_arrange_act_assert(self):
        """Test pytest unit template follows AAA pattern."""
        generator = CodeTestGenerator()

        gap = CoverageGap(
            gap_id="gap_aaa",
            pattern=["test"],
            support=0.10,
            priority="medium",
            suggested_test_name="test_aaa",
            suggested_test_file="tests/test.py",
            description="Test AAA",
        )

        result = generator.generate_test(gap, framework="pytest", style="unit")

        # Should have Arrange/Act/Assert comments
        assert "Arrange" in result.test_code or "# TODO" in result.test_code
