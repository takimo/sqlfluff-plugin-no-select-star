import os
import logging
from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

# Logger configuration
logger = logging.getLogger(__name__)

class Rule_NoSelectStar_NS01(BaseRule):
    """
    Forbid wildcard projections (SELECT *).

    This rule detects and forbids the use of wildcard projections such as
    `SELECT *` or `SELECT t.*` in SQL files.

    The rule is designed to enforce explicit column enumeration, which improves:
    - Schema evolution control
    - Query performance
    - Code maintainability
    - Documentation clarity

    Configuration:
        target_model_prefixes (str): Comma-separated list of filename prefixes.
            Only files starting with these prefixes will be checked.
            If empty or not set, all files are checked.

    Example configuration in .sqlfluff:
        [sqlfluff:rules:NoSelectStar_NS01]
        target_model_prefixes = stg_, int_

    Note:
        COUNT(*) is automatically allowed because it's parsed as a 'star' segment,
        not a 'wildcard_expression'.
    """
    
    # Rule group definition
    groups = ("all",)
    
    # Rule ID (4-character code recommended)
    code = "NS01"
    
    description = "Explicit column enumeration is required."
    
    # Performance optimization: Use SegmentSeekerCrawler to only check
    # locations where wildcard_expression exists
    crawl_behaviour = SegmentSeekerCrawler({"wildcard_expression"})

    # Configuration variables that can be set in .sqlfluff
    # Example: [sqlfluff:rules:NoSelectStar_NS01] target_model_prefixes = stg_
    config_vals = ["target_model_prefixes"]

    def _eval(self, context: RuleContext):
        """
        Evaluate whether a wildcard projection should be flagged as an error.
        
        This function is called for each wildcard_expression found in the SQL.
        
        Args:
            context: RuleContext object containing segment information
            
        Returns:
            LintResult: Empty if valid, contains error details if invalid
        """

        # ---------------------------------------------------------
        # 0. Get filename once at the beginning (performance optimization)
        # ---------------------------------------------------------
        fname = ""
        if context.templated_file and context.templated_file.fname:
            fname = context.templated_file.fname
        file_name = os.path.basename(fname) if fname else ""

        # ---------------------------------------------------------
        # 1. Get target prefixes from configuration file (.sqlfluff)
        # ---------------------------------------------------------
        # Returns None if not configured
        prefixes_str = getattr(self, "target_model_prefixes", None)
        
        # Debug logging: output configuration value
        logger.debug(
            f"NS01 config - target_model_prefixes: '{prefixes_str}', "
            f"checking file: '{file_name}'"
        )

        # ---------------------------------------------------------
        # 2. Filter target models based on configuration
        # ---------------------------------------------------------
        # Only perform filename check if configuration exists
        if prefixes_str and prefixes_str.strip():
            # Parse comma-separated string: "stg_, int_" -> ['stg_', 'int_']
            prefixes = [p.strip() for p in prefixes_str.split(",") if p.strip()]
            
            if prefixes:
                # Skip safely if filename cannot be determined
                if not file_name:
                    return LintResult()

                # Check if filename starts with any of the specified prefixes
                is_target = any(file_name.startswith(p) for p in prefixes)
                
                # If not a target file, skip error (pass)
                if not is_target:
                    return LintResult()

        # ---------------------------------------------------------
        # 3. Return error
        # ---------------------------------------------------------
        # At this point, the following conditions are confirmed:
        # A. A wildcard exists in the SQL (guaranteed by crawl_behaviour)
        # B. This is a target file (passed filtering)
        
        file_name_display = file_name if file_name else "unknown_file"

        # Return error information
        return LintResult(
            anchor=context.segment,  # Error location (where to underline)
            description=f"Forbidden wildcard projection found in '{file_name_display}': {context.segment.raw}"
        )
