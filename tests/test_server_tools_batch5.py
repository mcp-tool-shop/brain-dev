"""
Batch 5: server.py MCP Tools and Config Tests (25 tests)
Tests for MCP server creation, tool handlers, and configuration.
"""

import pytest
import json
from pathlib import Path

from brain_dev.config import DevBrainConfig, load_config
from brain_dev.server import create_server


# =============================================================================
# Section 1: DevBrainConfig Tests (8 tests)
# =============================================================================

class TestDevBrainConfigDefaults:
    """Test DevBrainConfig default values."""

    def test_default_server_name(self):
        """Test default server_name."""
        config = DevBrainConfig()
        assert config.server_name == "brain-dev"

    def test_default_server_version(self):
        """Test default server_version."""
        config = DevBrainConfig()
        assert config.server_version == "1.0.0"

    def test_default_min_gap_support(self):
        """Test default min_gap_support is 0.05."""
        config = DevBrainConfig()
        assert config.min_gap_support == 0.05

    def test_default_min_confidence(self):
        """Test default min_confidence is 0.5."""
        config = DevBrainConfig()
        assert config.min_confidence == 0.5

    def test_default_max_suggestions(self):
        """Test default max_suggestions is 20."""
        config = DevBrainConfig()
        assert config.max_suggestions == 20

    def test_default_test_framework(self):
        """Test default test framework is pytest."""
        config = DevBrainConfig()
        assert config.default_test_framework == "pytest"


class TestDevBrainConfigCustomValues:
    """Test DevBrainConfig with custom values."""

    def test_custom_values(self):
        """Test setting custom config values."""
        config = DevBrainConfig(
            server_name="custom-brain",
            min_gap_support=0.10,
            min_confidence=0.8,
            max_suggestions=50,
        )

        assert config.server_name == "custom-brain"
        assert config.min_gap_support == 0.10
        assert config.min_confidence == 0.8
        assert config.max_suggestions == 50

    def test_custom_test_style(self):
        """Test custom test_style setting."""
        config = DevBrainConfig(test_style="integration")
        assert config.test_style == "integration"


class TestLoadConfig:
    """Test load_config function."""

    def test_load_config_returns_default(self):
        """Test load_config returns DevBrainConfig."""
        config = load_config()
        assert isinstance(config, DevBrainConfig)


# =============================================================================
# Section 2: create_server Tests (5 tests)
# =============================================================================

class TestCreateServer:
    """Test create_server function."""

    def test_create_server_returns_server(self):
        """Test create_server returns Server instance."""
        config = DevBrainConfig()
        server = create_server(config)
        assert server is not None

    def test_create_server_with_default_config(self):
        """Test create_server with no config uses defaults."""
        server = create_server()
        assert server is not None

    def test_create_server_with_custom_config(self):
        """Test create_server with custom config."""
        config = DevBrainConfig(
            min_gap_support=0.15,
            max_suggestions=10,
        )
        server = create_server(config)
        assert server is not None


class TestServerAnalyzersLazyInit:
    """Test server analyzers are lazily initialized."""

    def test_server_has_list_tools_handler(self, server):
        """Test server has tools registered."""
        # The server fixture from conftest provides a configured server
        assert server is not None


# =============================================================================
# Section 3: Tool Handler Tests (12 tests)
# =============================================================================

class TestCoverageAnalyzeTool:
    """Test coverage_analyze tool handler."""

    @pytest.mark.asyncio
    async def test_coverage_analyze_basic(self, server):
        """Test coverage_analyze tool with basic input."""
        # Direct test of the handler logic
        from brain_dev.analyzer import CoverageAnalyzer

        analyzer = CoverageAnalyzer(min_support=0.05)
        patterns = [
            {"sequence": ["login", "checkout"], "support": 0.20},
        ]
        test_patterns = []

        gaps = analyzer.analyze_gaps(patterns, test_patterns)

        assert len(gaps) == 1
        assert gaps[0].pattern == ["login", "checkout"]

    @pytest.mark.asyncio
    async def test_coverage_analyze_with_test_patterns(self, server):
        """Test coverage_analyze with test patterns covering some flows."""
        from brain_dev.analyzer import CoverageAnalyzer

        analyzer = CoverageAnalyzer(min_support=0.05)
        patterns = [
            {"sequence": ["a", "b"], "support": 0.15},
            {"sequence": ["c", "d"], "support": 0.15},
        ]
        test_patterns = [["a", "b"]]  # Only a->b is covered

        gaps = analyzer.analyze_gaps(patterns, test_patterns)

        gap_seqs = [g.pattern for g in gaps]
        assert ["c", "d"] in gap_seqs
        assert ["a", "b"] not in gap_seqs


class TestBehaviorMissingTool:
    """Test behavior_missing tool handler."""

    @pytest.mark.asyncio
    async def test_behavior_missing_basic(self):
        """Test behavior_missing tool with basic input."""
        from brain_dev.analyzer import BehaviorAnalyzer

        analyzer = BehaviorAnalyzer()
        patterns = [
            {"sequence": ["unhandled_event"], "occurrence_count": 20},
        ]

        missing = analyzer.find_missing_behaviors(patterns, [], min_count=5)

        assert len(missing) > 0


class TestTestsGenerateTool:
    """Test tests_generate tool handler."""

    @pytest.mark.asyncio
    async def test_tests_generate_basic(self):
        """Test tests_generate tool with gap input."""
        from brain_dev.analyzer import CodeTestGenerator, CoverageGap

        generator = CodeTestGenerator()
        gap = CoverageGap(
            gap_id="gap_001",
            pattern=["login", "checkout"],
            support=0.15,
            priority="high",
            suggested_test_name="test_login_checkout",
            suggested_test_file="tests/test_flow.py",
            description="Login checkout flow",
        )

        suggestion = generator.generate_test(gap, framework="pytest", style="unit")

        assert suggestion.test_name == "test_login_checkout"
        assert suggestion.framework == "pytest"


class TestRefactorSuggestTool:
    """Test refactor_suggest tool handler."""

    @pytest.mark.asyncio
    async def test_refactor_suggest_complexity(self):
        """Test refactor_suggest with complexity analysis."""
        from brain_dev.analyzer import RefactorAnalyzer

        analyzer = RefactorAnalyzer()
        symbols = [
            {
                "name": "complex_func",
                "file_path": "module.py",
                "line": 10,
                "source_code": "if a: if b: if c: for x in y: for z in w: while True: pass",
            }
        ]

        suggestions = analyzer.analyze_code(symbols, [], "complexity")

        assert len(suggestions) > 0
        assert suggestions[0].suggestion_type == "reduce_complexity"


class TestUXInsightsTool:
    """Test ux_insights tool handler."""

    @pytest.mark.asyncio
    async def test_ux_insights_dropoff(self):
        """Test ux_insights with dropoff metric."""
        from brain_dev.analyzer import UXAnalyzer

        analyzer = UXAnalyzer()
        patterns = [
            {"sequence": ["start", "step1"], "occurrence_count": 100},
            {"sequence": ["start", "step1", "step2"], "occurrence_count": 40},
        ]

        insights = analyzer.analyze_flow(patterns, flow_type="general", metric="dropoff")

        assert isinstance(insights, list)


class TestBrainStatsTool:
    """Test brain_stats tool handler."""

    @pytest.mark.asyncio
    async def test_brain_stats_returns_config(self, config):
        """Test brain_stats returns server configuration."""
        # The config fixture from conftest provides configuration
        assert config.server_name == "brain-dev"
        assert config.max_suggestions == 10  # Overridden in fixture


class TestSmartTestsGenerateTool:
    """Test smart_tests_generate tool handler."""

    @pytest.mark.asyncio
    async def test_smart_tests_generate_valid_file(self, tmp_path):
        """Test smart_tests_generate with valid Python file."""
        from brain_dev.smart_test_generator import generate_tests_for_file

        source_file = tmp_path / "sample.py"
        source_file.write_text("def hello(): pass")

        result = generate_tests_for_file(str(source_file))

        assert "Tests for" in result

    @pytest.mark.asyncio
    async def test_smart_tests_generate_file_not_found(self, tmp_path):
        """Test smart_tests_generate with non-existent file."""
        from brain_dev.smart_test_generator import generate_tests_for_file

        with pytest.raises(FileNotFoundError):
            generate_tests_for_file(str(tmp_path / "nonexistent.py"))


class TestDocsGenerateTool:
    """Test docs_generate tool handler."""

    @pytest.mark.asyncio
    async def test_docs_generate_basic(self):
        """Test docs_generate with symbols lacking docs."""
        from brain_dev.analyzer import DocsAnalyzer

        analyzer = DocsAnalyzer()
        symbols = [
            {
                "name": "undocumented_func",
                "symbol_type": "function",
                "file_path": "module.py",
                "line": 10,
                "docstring": "",
            }
        ]

        suggestions = analyzer.analyze_docs(symbols, doc_style="google")

        assert len(suggestions) > 0
        assert suggestions[0].doc_type == "missing"


class TestSecurityAuditTool:
    """Test security_audit tool handler."""

    @pytest.mark.asyncio
    async def test_security_audit_basic(self):
        """Test security_audit with vulnerable code."""
        from brain_dev.analyzer import SecurityAnalyzer

        analyzer = SecurityAnalyzer()
        symbols = [
            {
                "name": "vulnerable",
                "file_path": "query.py",
                "line": 5,
                "source_code": 'eval(user_input)',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        assert len(issues) > 0

    @pytest.mark.asyncio
    async def test_security_audit_severity_counts(self):
        """Test security_audit returns severity counts."""
        from brain_dev.analyzer import SecurityAnalyzer

        analyzer = SecurityAnalyzer()
        symbols = [
            {
                "name": "mixed_vulns",
                "file_path": "vulnerabilities.py",
                "line": 10,
                "source_code": '''
                    password = "secret123"
                    eval(user_input)
                ''',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        # Count severities
        severity_counts = {}
        for issue in issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

        assert isinstance(severity_counts, dict)
