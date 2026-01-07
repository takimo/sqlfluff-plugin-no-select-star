---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
<!-- A clear and concise description of what the bug is -->

## To Reproduce
Steps to reproduce the behavior:

1. Configuration used: 
   ```ini
   [sqlfluff:rules:NoSelectStar_NS01]
   target_model_prefixes = ...
   ```

2. SQL file content:
   ```sql
   -- your SQL here
   ```

3. Command run: 
   ```bash
   sqlfluff lint ...
   ```

4. Error/unexpected behavior observed:
   ```
   -- error output or description
   ```

## Expected Behavior
<!-- What you expected to happen -->

## Environment
- SQLFluff version: [e.g., 3.0.0]
- Plugin version: [e.g., 0.1.0]
- Python version: [e.g., 3.11]
- OS: [e.g., macOS 14.0, Ubuntu 22.04]

## Additional Context
<!-- Any other context about the problem, screenshots, or examples -->
