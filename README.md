# SQLFluff Plugin: No Select Star

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A SQLFluff plugin to forbid wildcard projections (`SELECT *`) in SQL files.

**[日本語版はこちら](#japanese-version) | [Japanese version](#japanese-version)**

---

## Table of Contents

- [Why This Plugin?](#why-this-plugin)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Use Cases](#use-cases)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Why This Plugin?

Using wildcard projections like `SELECT *` or `table.*` in SQL queries can cause several problems:

### 1. **Unpredictable Schema Changes**
When a source table's schema changes (columns added/removed), wildcard projections cause your query output to change automatically and silently. This can break downstream models or applications without warning.

### 2. **Performance Degradation**
Wildcards select all columns, including ones you don't need. This wastes:
- Network bandwidth
- Memory
- Storage space
- Compute resources (especially in columnar databases like BigQuery)

### 3. **Reduced Maintainability**
It's impossible to understand which columns are actually used just by reading the SQL. This makes:
- Code reviews difficult
- Debugging time-consuming
- Impact analysis nearly impossible

### 4. **Poor Documentation**
Explicit column selection serves as implicit documentation of your data contracts and dependencies.

**This plugin enforces explicit column enumeration to prevent these issues.**

---

## Features

- ✅ Detects `SELECT *` and `table.*` patterns
- ✅ Allows `COUNT(*)` (correctly recognized as aggregate function)
- ✅ Configurable file targeting with prefix filters
- ✅ Perfect for dbt projects (staging, intermediate layers)
- ✅ Fast performance using SQLFluff's SegmentSeekerCrawler
- ✅ Comprehensive test coverage

---

## Installation

### From Source (Editable Install)

```bash
cd sqlfluff-plugin-no-select-star
pip install -e .
```

### For Development (with test dependencies)

```bash
pip install -e ".[test]"
```

---

## Quick Start

### 1. Create a `.sqlfluff` configuration file

```ini
[sqlfluff]
dialect = bigquery
rules = NoSelectStar_NS01
```

### 2. Run SQLFluff

```bash
sqlfluff lint models/
```

### 3. See errors for wildcard projections

```
== [models/staging/stg_users.sql] FAIL
L:1 | P:1 | NS01 | Forbidden wildcard projection found in 'stg_users.sql': *
```

---

## Configuration

### Basic Configuration

Add the rule to your `.sqlfluff` file:

```ini
[sqlfluff]
dialect = bigquery
rules = NoSelectStar_NS01
```

### Target Specific File Prefixes

Use `target_model_prefixes` to only check files with specific prefixes:

```ini
[sqlfluff]
rules = NoSelectStar_NS01

[sqlfluff:rules:NoSelectStar_NS01]
# Only check staging models
target_model_prefixes = stg_
```

### Multiple Prefixes

Use comma-separated values:

```ini
[sqlfluff:rules:NoSelectStar_NS01]
# Check staging and intermediate models
target_model_prefixes = stg_, int_
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `target_model_prefixes` | string | (empty) | Comma-separated filename prefixes. Only files starting with these prefixes will be checked. If empty, all files are checked. |

---

## Use Cases

### Use Case 1: dbt Staging Models (Recommended)

In dbt projects, **staging models** (`stg_*`) are the first transformation layer from raw data sources. Explicit column selection here is crucial for:

- **Schema evolution control**: Raw data schemas change frequently
- **Early detection**: Catch schema changes at the earliest pipeline stage
- **Data contracts**: Clear column selection acts as a contract
- **Performance**: Only select columns actually needed downstream

**Configuration:**

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = stg_
```

**Example:**

❌ **Bad (Error):**
```sql
-- models/staging/stg_users.sql
SELECT * FROM {{ source('raw', 'users') }}
```

✅ **Good (Pass):**
```sql
-- models/staging/stg_users.sql
SELECT
    user_id,
    email,
    created_at,
    updated_at
FROM {{ source('raw', 'users') }}
```

### Use Case 2: Staging + Intermediate Layers

For stricter enforcement, check both staging and intermediate models:

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = stg_, int_
```

### Use Case 3: All Models (Strictest)

For maximum SQL quality, check all models:

```ini
[sqlfluff]
rules = NoSelectStar_NS01

# No target_model_prefixes = all files are checked
```

### Use Case 4: Data Marts Only

If you only want to enforce in business logic layers:

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = mart_, dim_, fact_
```

### Use Case 5: Custom Gate/Review Layer

For models that require approval before deployment:

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = gate_, review_
```

---

## Testing

### Run Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_rule_no_select_star_ns01.py::TestRuleNoSelectStarNS01::test_prefix_match_returns_error -v
```

### Test Coverage

The test suite covers:
- ✅ Prefix matching and filtering
- ✅ Multiple prefix configurations
- ✅ Empty/null configuration handling
- ✅ COUNT(*) allowance
- ✅ Table-qualified wildcards (`t.*`)
- ✅ Explicit column selection validation

---

## Contributing

Contributions are welcome! Please feel free to:

1. Report bugs via [GitHub Issues](https://github.com/takimo/sqlfluff-plugin-no-select-star/issues)
2. Submit pull requests
3. Suggest new features or improvements

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="japanese-version"></a>

# SQLFluff プラグイン: No Select Star

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

SQL ファイル内のワイルドカード投影（`SELECT *`）を禁止する SQLFluff プラグインです。

---

## 目次

- [なぜこのプラグインが必要なのか？](#なぜこのプラグインが必要なのか)
- [機能](#機能)
- [インストール](#インストール)
- [クイックスタート](#クイックスタート)
- [設定方法](#設定方法)
- [使用例](#使用例)
- [テスト](#テスト)
- [コントリビューション](#コントリビューション)
- [ライセンス](#ライセンス)

---

## なぜこのプラグインが必要なのか？

SQL クエリで `SELECT *` や `table.*` のようなワイルドカード投影を使用すると、以下のような問題が発生します：

### 1. **予測不可能なスキーマ変更**
ソーステーブルのスキーマが変更（カラムの追加・削除）されると、ワイルドカード投影はクエリ出力を自動的かつ暗黙的に変更します。これにより、下流のモデルやアプリケーションが予告なく壊れる可能性があります。

### 2. **パフォーマンスの低下**
ワイルドカードは必要のないカラムも含めてすべてのカラムを選択します。これにより以下が無駄になります：
- ネットワーク帯域幅
- メモリ
- ストレージ容量
- 計算リソース（特に BigQuery のような列指向データベースで顕著）

### 3. **保守性の低下**
SQL を読むだけでは、実際にどのカラムが使用されているかを理解することができません。これにより：
- コードレビューが困難になる
- デバッグに時間がかかる
- 影響分析がほぼ不可能になる

### 4. **ドキュメント性の欠如**
明示的なカラム選択は、データコントラクトと依存関係の暗黙的なドキュメントとして機能します。

**このプラグインは、明示的なカラム列挙を強制することで、これらの問題を防ぎます。**

---

## 機能

- ✅ `SELECT *` と `table.*` パターンを検出
- ✅ `COUNT(*)` は許可（集約関数として正しく認識）
- ✅ プレフィックスフィルターによる対象ファイルの設定が可能
- ✅ dbt プロジェクト（ステージング層、中間層）に最適
- ✅ SQLFluff の SegmentSeekerCrawler による高速パフォーマンス
- ✅ 包括的なテストカバレッジ

---

## インストール

### ソースからインストール（編集可能モード）

```bash
cd sqlfluff-plugin-no-select-star
pip install -e .
```

### 開発用（テスト依存関係込み）

```bash
pip install -e ".[test]"
```

---

## クイックスタート

### 1. `.sqlfluff` 設定ファイルを作成

```ini
[sqlfluff]
dialect = bigquery
rules = NoSelectStar_NS01
```

### 2. SQLFluff を実行

```bash
sqlfluff lint models/
```

### 3. ワイルドカード投影のエラーを確認

```
== [models/staging/stg_users.sql] FAIL
L:1 | P:1 | NS01 | Forbidden wildcard projection found in 'stg_users.sql': *
```

---

## 設定方法

### 基本設定

`.sqlfluff` ファイルにルールを追加します：

```ini
[sqlfluff]
dialect = bigquery
rules = NoSelectStar_NS01
```

### 特定のファイルプレフィックスのみを対象にする

`target_model_prefixes` を使用して、特定のプレフィックスで始まるファイルのみをチェックします：

```ini
[sqlfluff]
rules = NoSelectStar_NS01

[sqlfluff:rules:NoSelectStar_NS01]
# ステージングモデルのみをチェック
target_model_prefixes = stg_
```

### 複数のプレフィックス

カンマ区切りで複数指定できます：

```ini
[sqlfluff:rules:NoSelectStar_NS01]
# ステージングと中間モデルをチェック
target_model_prefixes = stg_, int_
```

### 設定オプション

| オプション | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `target_model_prefixes` | string | (空) | カンマ区切りのファイル名プレフィックス。指定されたプレフィックスで始まるファイルのみがチェック対象となります。空の場合は全ファイルが対象です。 |

---

## 使用例

### 使用例 1: dbt ステージングモデル（推奨）

dbt プロジェクトにおいて、**ステージングモデル**（`stg_*`）は生データソースからの最初の変換層です。ここでの明示的なカラム選択が重要な理由：

- **スキーマ変更の制御**: 生データのスキーマは頻繁に変わります
- **早期発見**: パイプラインの最も早い段階でスキーマ変更をキャッチできます
- **データコントラクト**: カラムの明示的な選択が契約として機能します
- **パフォーマンス**: 下流で実際に必要なカラムのみを選択します

**設定例：**

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = stg_
```

**例：**

❌ **悪い例（エラーになる）:**
```sql
-- models/staging/stg_users.sql
SELECT * FROM {{ source('raw', 'users') }}
```

✅ **良い例（成功）:**
```sql
-- models/staging/stg_users.sql
SELECT
    user_id,
    email,
    created_at,
    updated_at
FROM {{ source('raw', 'users') }}
```

### 使用例 2: ステージング + 中間層

より厳格な適用として、ステージングと中間モデルの両方をチェック：

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = stg_, int_
```

### 使用例 3: 全モデル（最も厳格）

最大限の SQL 品質を求める場合、全モデルをチェック：

```ini
[sqlfluff]
rules = NoSelectStar_NS01

# target_model_prefixes を指定しない = 全ファイルが対象
```

### 使用例 4: データマート層のみ

ビジネスロジック層でのみ適用したい場合：

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = mart_, dim_, fact_
```

### 使用例 5: カスタムゲート/レビュー層

デプロイ前に承認が必要なモデルに対して：

```ini
[sqlfluff:rules:NoSelectStar_NS01]
target_model_prefixes = gate_, review_
```

---

## テスト

### テストの実行

```bash
# テスト依存関係をインストール
pip install -e ".[test]"

# 全テストを実行
pytest tests/ -v

# 特定のテストのみ実行
pytest tests/test_rule_no_select_star_ns01.py::TestRuleNoSelectStarNS01::test_prefix_match_returns_error -v
```

### テストカバレッジ

テストスイートは以下をカバーします：
- ✅ プレフィックスマッチングとフィルタリング
- ✅ 複数プレフィックス設定
- ✅ 空/null 設定の処理
- ✅ COUNT(*) の許可
- ✅ テーブル修飾子付きワイルドカード（`t.*`）
- ✅ 明示的なカラム選択の検証

---

## コントリビューション

コントリビューションを歓迎します！以下の方法でご参加ください：

1. [GitHub Issues](https://github.com/takimo/sqlfluff-plugin-no-select-star/issues) でバグ報告
2. プルリクエストの送信
3. 新機能や改善の提案

---

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

---

## Author

**Shinya Takimoto**

- GitHub: [@takimo](https://github.com/takimo)
