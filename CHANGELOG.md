# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.0.1](https://github.com/takimo/sqlfluff-plugin-no-select-star/commits/v0.0.1) - 2026-01-07
- ドキュメント改善とCI/CD環境の構築 by @takimo in https://github.com/takimo/sqlfluff-plugin-no-select-star/pull/1
- CI修正: Python 3.9互換性対応とtagpr設定の修正 by @takimo in https://github.com/takimo/sqlfluff-plugin-no-select-star/pull/2

## [Unreleased]

### Added
- Initial release of sqlfluff-plugin-no-select-star
- NS01 rule to forbid wildcard projections (SELECT *)
- Configurable file targeting with `target_model_prefixes`
- Comprehensive test coverage with 8 test cases
- Support for dbt project conventions (staging, intermediate models)

### Features
- Detects `SELECT *` and `table.*` patterns
- Allows `COUNT(*)` (correctly recognized as aggregate function)
- Fast performance using SQLFluff's SegmentSeekerCrawler
- Configurable prefix-based file filtering
- Detailed error messages with filename and wildcard location

### Documentation
- Comprehensive README in Japanese and English
- Installation instructions for development and production
- Configuration examples and use cases
- Troubleshooting guide
- Testing documentation
