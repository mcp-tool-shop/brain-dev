"""
Batch 1: Data Models and CoverageAnalyzer Tests (25 tests)
Tests for data models (CoverageGap, MissingBehavior, SuggestedUnitCase, etc.)
and CoverageAnalyzer class functionality.
"""

import pytest
import hashlib
from brain_dev.analyzer import (
    CoverageGap,
    MissingBehavior,
    SuggestedUnitCase,
    TestSuggestion,
    GeneratedTest,
    RefactorSuggestion,
    UXInsight,
    DocSuggestion,
    SecurityIssue,
    CoverageAnalyzer,
)


# =============================================================================
# Section 1: CoverageGap Data Model Tests (5 tests)
# =============================================================================

class TestCoverageGapFields:
    """Test CoverageGap field access and types."""

    def test_coverage_gap_all_required_fields(self):
        """Test CoverageGap with all required fields."""
        gap = CoverageGap(
            gap_id="gap_test_001",
            pattern=["login", "search", "checkout"],
            support=0.25,
            priority="high",
            suggested_test_name="test_login_search_checkout_flow",
            suggested_test_file="tests/test_checkout_flow.py",
            description="Checkout flow after search not covered",
        )

        assert gap.gap_id == "gap_test_001"
        assert gap.pattern == ["login", "search", "checkout"]
        assert gap.support == 0.25
        assert gap.priority == "high"
        assert gap.suggested_test_name == "test_login_search_checkout_flow"
        assert gap.suggested_test_file == "tests/test_checkout_flow.py"
        assert gap.description == "Checkout flow after search not covered"


class TestCoverageGapToDictKeys:
    """Test CoverageGap to_dict has correct keys."""

    def test_to_dict_contains_expected_keys(self):
        """Test to_dict returns dict with all expected keys."""
        gap = CoverageGap(
            gap_id="gap_keys",
            pattern=["a", "b"],
            support=0.15,
            priority="medium",
            suggested_test_name="test_a_b",
            suggested_test_file="tests/test_ab.py",
            description="Flow A to B",
        )

        result = gap.to_dict()

        assert "gap_id" in result
        assert "pattern" in result
        assert "support" in result
        assert "priority" in result
        assert "suggested_test" in result
        assert "suggested_file" in result
        assert "description" in result


class TestCoverageGapPriorityValues:
    """Test CoverageGap accepts various priority values."""

    @pytest.mark.parametrize("priority", ["low", "medium", "high", "critical"])
    def test_priority_values(self, priority):
        """Test CoverageGap accepts valid priority values."""
        gap = CoverageGap(
            gap_id=f"gap_{priority}",
            pattern=["test"],
            support=0.1,
            priority=priority,
            suggested_test_name="test_flow",
            suggested_test_file="tests/test.py",
            description="Test",
        )

        assert gap.priority == priority


class TestCoverageGapEmptyPattern:
    """Test CoverageGap with empty pattern list."""

    def test_empty_pattern(self):
        """Test CoverageGap can have empty pattern."""
        gap = CoverageGap(
            gap_id="gap_empty",
            pattern=[],
            support=0.0,
            priority="low",
            suggested_test_name="test_empty",
            suggested_test_file="tests/test.py",
            description="Empty pattern",
        )

        assert gap.pattern == []
        assert gap.to_dict()["pattern"] == []


class TestCoverageGapSupportRange:
    """Test CoverageGap support values."""

    @pytest.mark.parametrize("support", [0.0, 0.05, 0.25, 0.5, 0.99, 1.0])
    def test_support_values(self, support):
        """Test CoverageGap accepts support values from 0 to 1."""
        gap = CoverageGap(
            gap_id="gap_support",
            pattern=["test"],
            support=support,
            priority="medium",
            suggested_test_name="test_flow",
            suggested_test_file="tests/test.py",
            description="Test support",
        )

        assert gap.support == support


# =============================================================================
# Section 2: Other Data Model Tests (8 tests)
# =============================================================================

class TestMissingBehaviorDefaultFields:
    """Test MissingBehavior default field values."""

    def test_affected_files_defaults_to_empty(self):
        """Test affected_files defaults to empty list."""
        behavior = MissingBehavior(
            behavior_id="beh_001",
            pattern=["action"],
            observed_count=10,
            description="Test behavior",
            suggested_action="Add handler",
        )

        assert behavior.affected_files == []


class TestMissingBehaviorWithAffectedFiles:
    """Test MissingBehavior with affected files."""

    def test_affected_files_set(self):
        """Test MissingBehavior with affected_files set."""
        behavior = MissingBehavior(
            behavior_id="beh_files",
            pattern=["upload", "process"],
            observed_count=15,
            description="Upload processing not handled",
            suggested_action="Add upload handler",
            affected_files=["handlers.py", "views.py", "utils.py"],
        )

        assert len(behavior.affected_files) == 3
        assert "handlers.py" in behavior.affected_files


class TestSuggestedUnitCaseAlias:
    """Test TestSuggestion is alias for SuggestedUnitCase."""

    def test_alias_is_same_class(self):
        """Test TestSuggestion and GeneratedTest are aliases."""
        assert TestSuggestion is SuggestedUnitCase
        assert GeneratedTest is SuggestedUnitCase


class TestSuggestedUnitCaseFields:
    """Test SuggestedUnitCase all fields."""

    def test_all_fields(self):
        """Test SuggestedUnitCase with all fields."""
        test = SuggestedUnitCase(
            test_name="test_user_registration",
            test_file="tests/test_registration.py",
            test_code="def test_user_registration():\n    pass",
            covers_pattern=["register", "verify", "login"],
            framework="pytest",
            style="integration",
        )

        assert test.test_name == "test_user_registration"
        assert test.test_file == "tests/test_registration.py"
        assert "def test_user_registration" in test.test_code
        assert test.covers_pattern == ["register", "verify", "login"]
        assert test.framework == "pytest"
        assert test.style == "integration"


class TestRefactorSuggestionOptionalFields:
    """Test RefactorSuggestion optional fields."""

    def test_code_before_after_defaults(self):
        """Test code_before and code_after default to empty string."""
        suggestion = RefactorSuggestion(
            suggestion_id="ref_001",
            suggestion_type="simplify",
            location="module.py:50",
            reason="Can be simplified",
            confidence=0.8,
        )

        assert suggestion.code_before == ""
        assert suggestion.code_after == ""


class TestRefactorSuggestionToDictType:
    """Test RefactorSuggestion to_dict uses 'type' key."""

    def test_to_dict_uses_type_key(self):
        """Test to_dict maps suggestion_type to 'type' key."""
        suggestion = RefactorSuggestion(
            suggestion_id="ref_002",
            suggestion_type="extract_function",
            location="utils.py:100",
            reason="Extract repeated code",
            confidence=0.75,
        )

        result = suggestion.to_dict()

        assert result["type"] == "extract_function"
        assert "suggestion_type" not in result


class TestDocSuggestionFields:
    """Test DocSuggestion dataclass."""

    def test_doc_suggestion_fields(self):
        """Test DocSuggestion all fields."""
        suggestion = DocSuggestion(
            suggestion_id="doc_001",
            symbol_name="calculate_total",
            symbol_type="function",
            location="billing.py:25",
            doc_type="missing",
            suggested_doc='"""Calculate the total amount."""',
            confidence=0.9,
        )

        assert suggestion.suggestion_id == "doc_001"
        assert suggestion.symbol_name == "calculate_total"
        assert suggestion.symbol_type == "function"
        assert suggestion.doc_type == "missing"
        assert suggestion.confidence == 0.9


class TestSecurityIssueFields:
    """Test SecurityIssue dataclass."""

    def test_security_issue_with_cwe(self):
        """Test SecurityIssue with CWE ID."""
        issue = SecurityIssue(
            issue_id="sec_001",
            severity="critical",
            category="sql_injection",
            location="db.py:50",
            description="Potential SQL injection",
            recommendation="Use parameterized queries",
            confidence=0.85,
            cwe_id="CWE-89",
        )

        assert issue.issue_id == "sec_001"
        assert issue.severity == "critical"
        assert issue.category == "sql_injection"
        assert issue.cwe_id == "CWE-89"

    def test_security_issue_optional_cwe(self):
        """Test SecurityIssue with no CWE ID."""
        issue = SecurityIssue(
            issue_id="sec_002",
            severity="medium",
            category="hardcoded_secrets",
            location="config.py:10",
            description="Hardcoded password",
            recommendation="Use environment variables",
            confidence=0.7,
        )

        assert issue.cwe_id is None


# =============================================================================
# Section 3: CoverageAnalyzer Tests (12 tests)
# =============================================================================

class TestCoverageAnalyzerInit:
    """Test CoverageAnalyzer initialization."""

    def test_default_min_support(self):
        """Test default min_support is 0.05."""
        analyzer = CoverageAnalyzer()
        assert analyzer.min_support == 0.05

    def test_custom_min_support(self):
        """Test custom min_support value."""
        analyzer = CoverageAnalyzer(min_support=0.10)
        assert analyzer.min_support == 0.10


class TestCoverageAnalyzerAnalyzeGaps:
    """Test CoverageAnalyzer.analyze_gaps method."""

    def test_finds_uncovered_high_support_patterns(self):
        """Test analyzer finds patterns not in test coverage."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [
            {"sequence": ["login", "checkout"], "support": 0.20},
            {"sequence": ["login", "search"], "support": 0.15},
        ]
        test_patterns = [["login", "search"]]  # Only one covered

        gaps = analyzer.analyze_gaps(observed, test_patterns)

        # Should find the uncovered checkout pattern
        gap_patterns = [tuple(g.pattern) for g in gaps]
        assert ("login", "checkout") in gap_patterns
        assert ("login", "search") not in gap_patterns

    def test_filters_low_support_patterns(self):
        """Test analyzer filters patterns below min_support."""
        analyzer = CoverageAnalyzer(min_support=0.10)

        observed = [
            {"sequence": ["high_support"], "support": 0.20},
            {"sequence": ["low_support"], "support": 0.05},  # Below threshold
        ]

        gaps = analyzer.analyze_gaps(observed, [])

        gap_patterns = [g.pattern for g in gaps]
        assert ["high_support"] in gap_patterns
        assert ["low_support"] not in gap_patterns

    def test_empty_observed_patterns(self):
        """Test analyzer with no observed patterns."""
        analyzer = CoverageAnalyzer()
        gaps = analyzer.analyze_gaps([], [])
        assert gaps == []

    def test_all_patterns_covered(self):
        """Test when all patterns are covered."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [
            {"sequence": ["a", "b"], "support": 0.15},
            {"sequence": ["c", "d"], "support": 0.10},
        ]
        test_patterns = [["a", "b"], ["c", "d"]]

        gaps = analyzer.analyze_gaps(observed, test_patterns)
        assert gaps == []


class TestCoverageAnalyzerPriority:
    """Test CoverageAnalyzer priority assignment."""

    def test_critical_priority_for_high_support(self):
        """Test critical priority for support >= 0.3."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["critical_flow"], "support": 0.35}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].priority == "critical"

    def test_high_priority_for_medium_support(self):
        """Test high priority for support >= 0.2."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["high_flow"], "support": 0.25}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].priority == "high"

    def test_medium_priority_for_moderate_support(self):
        """Test medium priority for support >= 0.1."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["medium_flow"], "support": 0.15}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].priority == "medium"

    def test_low_priority_for_low_support(self):
        """Test low priority for support < 0.1."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["low_flow"], "support": 0.06}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].priority == "low"


class TestCoverageAnalyzerTestNameGeneration:
    """Test CoverageAnalyzer test name generation."""

    def test_generates_test_name_from_pattern(self):
        """Test suggested test name is derived from pattern."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["login", "dashboard"], "support": 0.15}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].suggested_test_name.startswith("test_")
        assert "login" in gaps[0].suggested_test_name or "dashboard" in gaps[0].suggested_test_name

    def test_generates_test_file_path(self):
        """Test suggested test file path is generated."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["auth.login"], "support": 0.15}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].suggested_test_file.startswith("tests/")
        assert gaps[0].suggested_test_file.endswith(".py")


class TestCoverageAnalyzerGapSorting:
    """Test CoverageAnalyzer sorts gaps by support."""

    def test_gaps_sorted_by_support_descending(self):
        """Test gaps are sorted by support in descending order."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [
            {"sequence": ["low"], "support": 0.10},
            {"sequence": ["high"], "support": 0.30},
            {"sequence": ["medium"], "support": 0.20},
        ]

        gaps = analyzer.analyze_gaps(observed, [])

        supports = [g.support for g in gaps]
        assert supports == sorted(supports, reverse=True)


class TestCoverageAnalyzerGapIdGeneration:
    """Test CoverageAnalyzer generates unique gap IDs."""

    def test_gap_id_starts_with_prefix(self):
        """Test gap_id has correct prefix."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [{"sequence": ["test"], "support": 0.15}]
        gaps = analyzer.analyze_gaps(observed, [])

        assert gaps[0].gap_id.startswith("gap_")

    def test_different_patterns_have_different_ids(self):
        """Test different patterns get different gap IDs."""
        analyzer = CoverageAnalyzer(min_support=0.05)

        observed = [
            {"sequence": ["pattern_a"], "support": 0.15},
            {"sequence": ["pattern_b"], "support": 0.15},
        ]
        gaps = analyzer.analyze_gaps(observed, [])

        ids = [g.gap_id for g in gaps]
        assert len(set(ids)) == len(ids)  # All unique
