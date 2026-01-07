"""
Unit tests for Rule_NoSelectStar_NS01

Test cases:
1. Prefix match returns error
2. Prefix mismatch skips
3. No prefix configuration checks all files
4. Empty prefix configuration handling
5. COUNT(*) is allowed
6. Table-qualified wildcards (t.*) return errors
7. Explicit columns pass
8. Multiple prefixes configuration
"""

from typing import Optional

import pytest
from sqlfluff.core import Linter
from sqlfluff.core.config import FluffConfig


def create_config_file(target_model_prefixes: Optional[str] = None) -> str:
    """Create a temporary configuration file for testing"""
    config_content = """[sqlfluff]
dialect = bigquery
templater = raw
rules = NoSelectStar_NS01
"""
    if target_model_prefixes is not None:
        config_content += f"""
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = {target_model_prefixes}
"""
    return config_content


class TestRuleNoSelectStarNS01:
    """Test class for Rule_NoSelectStar_NS01"""

    @pytest.fixture
    def linter_with_prefix(self, tmp_path):
        """Create a Linter with prefix configuration"""
        config_file = tmp_path / ".sqlfluff"
        config_file.write_text(create_config_file("stg_"))
        config = FluffConfig.from_root(overrides={"dialect": "bigquery"}, require_dialect=False)
        config = FluffConfig.from_path(str(tmp_path))
        return Linter(config=config)

    @pytest.fixture
    def linter_without_prefix(self, tmp_path):
        """Create a Linter without prefix configuration"""
        config_file = tmp_path / ".sqlfluff"
        config_file.write_text(create_config_file(None))
        config = FluffConfig.from_path(str(tmp_path))
        return Linter(config=config)

    @pytest.fixture
    def linter_with_empty_prefix(self, tmp_path):
        """Create a Linter with empty prefix configuration"""
        config_file = tmp_path / ".sqlfluff"
        config_file.write_text(create_config_file(""))
        config = FluffConfig.from_path(str(tmp_path))
        return Linter(config=config)

    def test_prefix_match_returns_error(self, linter_with_prefix):
        """
        Test case 1: Prefix match returns error
        
        When a filename starts with stg_ and contains SELECT *,
        verify that NoSelectStar_NS01 error occurs
        """
        sql = "SELECT * FROM users"
        result = linter_with_prefix.lint_string(sql, fname="stg_users.sql")
        
        # Verify error exists
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) > 0, "Files with stg_ prefix should error on SELECT *"
        
        # Verify error message contains filename and wildcard
        error_desc = violations[0].desc()
        assert "stg_users.sql" in error_desc
        assert "*" in error_desc

    def test_prefix_mismatch_skips(self, linter_with_prefix):
        """
        Test case 2: Prefix mismatch skips
        
        When a filename does not start with stg_,
        verify that SELECT * does not cause an error
        """
        sql = "SELECT * FROM users"
        result = linter_with_prefix.lint_string(sql, fname="mart_users.sql")
        
        # Verify NoSelectStar_NS01 error does not exist
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) == 0, "Files without stg_ prefix should not error"

    def test_no_prefix_config_checks_all_files(self, linter_without_prefix):
        """
        Test case 3: No prefix configuration checks all files
        
        When target_model_prefixes is not configured,
        verify that SELECT * causes an error in all files
        """
        sql = "SELECT * FROM users"
        result = linter_without_prefix.lint_string(sql, fname="any_model.sql")
        
        # Verify error exists
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) > 0, "Without prefix config, all files should be checked"

    def test_empty_prefix_config_checks_all_files(self, linter_with_empty_prefix):
        """
        Test case 4: Empty prefix configuration handling
        
        When target_model_prefixes is an empty string,
        verify that SELECT * causes an error in all files
        """
        sql = "SELECT * FROM users"
        result = linter_with_empty_prefix.lint_string(sql, fname="any_model.sql")
        
        # Verify error exists
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) > 0, "With empty prefix config, all files should be checked"

    def test_count_star_is_allowed(self, linter_with_prefix):
        """
        Test case 5: COUNT(*) is allowed
        
        COUNT(*) is parsed as a 'star' segment, not 'wildcard_expression',
        so verify it does not cause an error
        """
        sql = "SELECT COUNT(*) FROM users"
        result = linter_with_prefix.lint_string(sql, fname="stg_users.sql")
        
        # Verify NoSelectStar_NS01 error does not exist
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) == 0, "COUNT(*) should not error"

    def test_table_wildcard_returns_error(self, linter_with_prefix):
        """
        Test case 6: Table-qualified wildcards (t.*) return errors
        
        Table-qualified wildcards like SELECT t.* should also
        cause an error
        """
        sql = "SELECT t.* FROM users AS t"
        result = linter_with_prefix.lint_string(sql, fname="stg_users.sql")
        
        # Verify error exists
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) > 0, "t.* should also error"

    def test_explicit_columns_pass(self, linter_with_prefix):
        """
        Test case 7: Explicit columns pass
        
        Explicit column specification like SELECT id, name FROM users
        should not cause an error
        """
        sql = "SELECT id, name FROM users"
        result = linter_with_prefix.lint_string(sql, fname="stg_users.sql")
        
        # Verify NoSelectStar_NS01 error does not exist
        violations = [v for v in result.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations) == 0, "Explicit column specification should not error"

    def test_multiple_prefixes(self, tmp_path):
        """
        Test case 8: Multiple prefixes configuration
        
        When multiple prefixes are configured with comma separation,
        verify that errors occur for any matching prefix
        """
        config_file = tmp_path / ".sqlfluff"
        config_file.write_text(create_config_file("stg_, int_"))
        config = FluffConfig.from_path(str(tmp_path))
        linter = Linter(config=config)
        sql = "SELECT * FROM users"
        
        # Files starting with stg_
        result_stg = linter.lint_string(sql, fname="stg_users.sql")
        violations_stg = [v for v in result_stg.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations_stg) > 0, "stg_ prefix should error"
        
        # Files starting with int_
        result_int = linter.lint_string(sql, fname="int_orders.sql")
        violations_int = [v for v in result_int.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations_int) > 0, "int_ prefix should error"
        
        # Files that don't match any prefix
        result_mart = linter.lint_string(sql, fname="mart_data.sql")
        violations_mart = [v for v in result_mart.violations if v.rule_code() == "NoSelectStar_NS01"]
        assert len(violations_mart) == 0, "Prefixes other than stg_, int_ should not error"
