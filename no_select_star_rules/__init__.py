# no_select_star_rules/__init__.py

from sqlfluff.core.plugin import hookimpl

@hookimpl
def get_rules():
    """Register custom rules with SQLFluff."""
    # Import inside the function to avoid circular dependencies
    from no_select_star_rules.rule_no_select_star_ns01 import Rule_NoSelectStar_NS01
    return [Rule_NoSelectStar_NS01]
