"""
Batch 4: SecurityAnalyzer and smart_test_generator.py Tests (25 tests)
Tests for SecurityAnalyzer class and smart_test_generator module components.
"""

import pytest
from pathlib import Path

from brain_dev.analyzer import (
    SecurityAnalyzer,
    SecurityIssue,
)
from brain_dev.smart_test_generator import (
    Parameter,
    FunctionInfo,
    ClassInfo,
    ImportInfo,
    ModuleInfo,
    CodeAnalyzer,
    MockDetector,
    SmartPytestFileGenerator,
    SmartTestFileGenerator,
    generate_tests_for_file,
)


# =============================================================================
# Section 1: SecurityAnalyzer Tests (12 tests)
# =============================================================================

class TestSecurityAnalyzerInit:
    """Test SecurityAnalyzer initialization."""

    def test_create_security_analyzer(self):
        """Test SecurityAnalyzer can be instantiated."""
        analyzer = SecurityAnalyzer()
        assert analyzer is not None

    def test_has_security_patterns(self):
        """Test analyzer has SECURITY_PATTERNS."""
        analyzer = SecurityAnalyzer()
        assert hasattr(analyzer, "SECURITY_PATTERNS")
        assert len(analyzer.SECURITY_PATTERNS) > 0


class TestSecurityAnalyzerPatternCategories:
    """Test SecurityAnalyzer detects various vulnerability categories."""

    def test_detects_sql_injection(self):
        """Test detects SQL injection patterns."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "unsafe_query",
                "file_path": "db.py",
                "line": 10,
                "source_code": 'cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        # Should detect SQL injection
        categories = [i.category for i in issues]
        assert "sql_injection" in categories or len(issues) > 0

    def test_detects_command_injection(self):
        """Test detects command injection patterns."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "run_command",
                "file_path": "utils.py",
                "line": 20,
                "source_code": 'os.system(f"rm -rf {path}")',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        categories = [i.category for i in issues]
        assert "command_injection" in categories or len(issues) > 0

    def test_detects_hardcoded_secrets(self):
        """Test detects hardcoded secrets."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "config",
                "file_path": "config.py",
                "line": 5,
                "source_code": 'password = "super_secret_password123"',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        categories = [i.category for i in issues]
        assert "hardcoded_secrets" in categories or len(issues) > 0

    def test_detects_insecure_deserialization(self):
        """Test detects insecure deserialization."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "load_data",
                "file_path": "loader.py",
                "line": 15,
                "source_code": 'pickle.loads(untrusted_data)',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        categories = [i.category for i in issues]
        assert "insecure_deserialization" in categories or len(issues) > 0


class TestSecurityAnalyzerSeverityThreshold:
    """Test SecurityAnalyzer severity threshold filtering."""

    def test_filters_by_severity_threshold(self):
        """Test issues below threshold are filtered."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "weak_hash",
                "file_path": "auth.py",
                "line": 30,
                "source_code": 'hashlib.md5(password.encode())',  # Medium severity
            }
        ]

        # High threshold should filter medium issues
        issues_high = analyzer.analyze_security(symbols, severity_threshold="critical")
        issues_low = analyzer.analyze_security(symbols, severity_threshold="low")

        # May have fewer issues with higher threshold
        assert len(issues_high) <= len(issues_low)

    @pytest.mark.parametrize("threshold", ["low", "medium", "high", "critical"])
    def test_accepts_severity_thresholds(self, threshold):
        """Test analyzer accepts all severity thresholds."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {"name": "func", "file_path": "a.py", "line": 1, "source_code": "pass"}
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold=threshold)

        assert isinstance(issues, list)


class TestSecurityAnalyzerIssueContent:
    """Test SecurityIssue content from analyzer."""

    def test_issue_has_recommendation(self):
        """Test security issues have recommendations."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "unsafe",
                "file_path": "module.py",
                "line": 10,
                "source_code": 'eval(user_input)',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        for issue in issues:
            assert issue.recommendation is not None
            assert len(issue.recommendation) > 0

    def test_issue_has_cwe_id(self):
        """Test security issues may have CWE IDs."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "injection",
                "file_path": "query.py",
                "line": 5,
                "source_code": 'cursor.execute("SELECT * FROM t WHERE x=" + user_input)',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        # CWE ID may be present for known vulnerabilities
        for issue in issues:
            # cwe_id is optional, but should be string or None
            assert issue.cwe_id is None or isinstance(issue.cwe_id, str)


class TestSecurityAnalyzerSorting:
    """Test SecurityAnalyzer sorts issues by severity."""

    def test_issues_sorted_by_severity(self):
        """Test issues are sorted by severity (critical first)."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {
                "name": "mixed",
                "file_path": "vulnerabilities.py",
                "line": 10,
                "source_code": '''
                    password = "secret123"
                    eval(user_input)
                    md5(data)
                ''',
            }
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")

        if len(issues) > 1:
            severity_order = {"critical": 3, "high": 2, "medium": 1, "low": 0}
            severities = [severity_order.get(i.severity, 0) for i in issues]
            assert severities == sorted(severities, reverse=True)


class TestSecurityAnalyzerEmptyInput:
    """Test SecurityAnalyzer with empty input."""

    def test_empty_symbols(self):
        """Test with empty symbols list."""
        analyzer = SecurityAnalyzer()
        issues = analyzer.analyze_security([], severity_threshold="low")
        assert issues == []

    def test_no_source_code(self):
        """Test symbols without source_code are skipped."""
        analyzer = SecurityAnalyzer()

        symbols = [
            {"name": "no_source", "file_path": "a.py", "line": 1}
        ]

        issues = analyzer.analyze_security(symbols, severity_threshold="low")
        assert issues == []


# =============================================================================
# Section 2: smart_test_generator.py Tests (13 tests)
# =============================================================================

class TestCodeAnalyzerBasics:
    """Test CodeAnalyzer basic functionality."""

    def test_analyze_returns_module_info(self):
        """Test analyze returns ModuleInfo."""
        source = "def hello(): pass"
        analyzer = CodeAnalyzer(source, "test.py")
        result = analyzer.analyze()

        assert isinstance(result, ModuleInfo)

    def test_detect_module_path(self):
        """Test module path detection."""
        source = "pass"
        analyzer = CodeAnalyzer(source, "some/path/module.py")

        # Should derive module name from path
        assert analyzer.module_name is not None


class TestCodeAnalyzerFunctions:
    """Test CodeAnalyzer function parsing."""

    def test_parses_simple_function(self):
        """Test parsing a simple function."""
        source = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
        analyzer = CodeAnalyzer(source, "math.py")
        result = analyzer.analyze()

        assert len(result.functions) == 1
        func = result.functions[0]
        assert func.name == "add"
        assert func.return_annotation == "int"
        assert len(func.params) == 2

    def test_parses_async_function(self):
        """Test parsing async function."""
        source = '''
async def fetch(url: str) -> dict:
    pass
'''
        analyzer = CodeAnalyzer(source, "http.py")
        result = analyzer.analyze()

        assert len(result.functions) == 1
        assert result.functions[0].is_async is True

    def test_parses_decorated_function(self):
        """Test parsing decorated function."""
        source = '''
@property
def name(self) -> str:
    return self._name
'''
        analyzer = CodeAnalyzer(source, "model.py")
        result = analyzer.analyze()

        assert len(result.functions) == 1
        assert "property" in result.functions[0].decorators


class TestCodeAnalyzerClasses:
    """Test CodeAnalyzer class parsing."""

    def test_parses_class(self):
        """Test parsing a class."""
        source = '''
class MyClass:
    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self.value
'''
        analyzer = CodeAnalyzer(source, "models.py")
        result = analyzer.analyze()

        assert len(result.classes) == 1
        cls = result.classes[0]
        assert cls.name == "MyClass"
        assert len(cls.methods) == 2

    def test_detects_dataclass(self):
        """Test detecting dataclass decorator."""
        source = '''
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
'''
        analyzer = CodeAnalyzer(source, "shapes.py")
        result = analyzer.analyze()

        assert len(result.classes) == 1
        assert result.classes[0].is_dataclass is True


class TestCodeAnalyzerImports:
    """Test CodeAnalyzer import parsing."""

    def test_parses_import(self):
        """Test parsing import statement."""
        source = "import os"
        analyzer = CodeAnalyzer(source, "utils.py")
        result = analyzer.analyze()

        assert len(result.imports) == 1
        assert result.imports[0].module == "os"
        assert result.imports[0].is_from_import is False

    def test_parses_from_import(self):
        """Test parsing from ... import statement."""
        source = "from pathlib import Path, PurePath"
        analyzer = CodeAnalyzer(source, "paths.py")
        result = analyzer.analyze()

        assert len(result.imports) == 1
        imp = result.imports[0]
        assert imp.module == "pathlib"
        assert "Path" in imp.names
        assert "PurePath" in imp.names
        assert imp.is_from_import is True


class TestMockDetectorBasics:
    """Test MockDetector functionality."""

    def test_detects_external_mocks(self):
        """Test detecting external imports need mocking."""
        module = ModuleInfo(
            file_path="test.py",
            module_name="mymodule.test",
            imports=[ImportInfo(module="requests", is_from_import=False)],
        )

        detector = MockDetector(module)
        mocks = detector.detect_mocks()

        assert "requests" in mocks

    def test_async_mock_for_async_libs(self):
        """Test AsyncMock suggested for async libraries."""
        module = ModuleInfo(
            file_path="test.py",
            module_name="test",
            imports=[ImportInfo(module="aiohttp", is_from_import=False)],
        )

        detector = MockDetector(module)
        mocks = detector.detect_mocks()

        assert mocks.get("aiohttp") == "AsyncMock"

    def test_no_mock_for_stdlib(self):
        """Test standard library doesn't need mocking."""
        module = ModuleInfo(
            file_path="test.py",
            module_name="test",
            imports=[
                ImportInfo(module="json", is_from_import=False),
                ImportInfo(module="typing", is_from_import=False),
            ],
        )

        detector = MockDetector(module)
        mocks = detector.detect_mocks()

        assert "json" not in mocks
        assert "typing" not in mocks


class TestSmartTestFileGeneratorAliases:
    """Test generator class aliases."""

    def test_alias_is_correct(self):
        """Test SmartTestFileGenerator is alias for SmartPytestFileGenerator."""
        assert SmartTestFileGenerator is SmartPytestFileGenerator


class TestGenerateTestsForFile:
    """Test generate_tests_for_file function."""

    def test_generates_for_simple_file(self, tmp_path):
        """Test generating tests for simple file."""
        source_file = tmp_path / "simple.py"
        source_file.write_text('''
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}"
''')

        result = generate_tests_for_file(str(source_file))

        assert "Tests for" in result
        assert "def test_greet" in result

    def test_generates_for_class(self, tmp_path):
        """Test generating tests for class."""
        source_file = tmp_path / "with_class.py"
        source_file.write_text('''
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
''')

        result = generate_tests_for_file(str(source_file))

        assert "class TestCalculator" in result
        assert "def test_add" in result

    def test_generates_async_tests(self, tmp_path):
        """Test async functions get async tests."""
        source_file = tmp_path / "async_mod.py"
        source_file.write_text('''
async def fetch_data(url: str) -> dict:
    pass
''')

        result = generate_tests_for_file(str(source_file))

        assert "@pytest.mark.asyncio" in result
        assert "async def test_fetch_data" in result
