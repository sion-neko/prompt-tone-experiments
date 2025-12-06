# LLM プロンプト口調実験ツール

異なるプロンプトの口調がGPT-5.1の応答にどのような影響を与えるかを分析する研究ツールです。複数のコミュニケーションスタイルを体系的にテストし、AI出力の品質と特性への影響を理解します。

## 概要

このツールは、同一のタスクを異なる口調のプロンプトでGPT-5.1に送信し、その応答を比較する実験を行います。プロンプトエンジニアリング技術がAIの振る舞いにどう影響するかを明らかにします。

### 実験タスク

本ツールには2つの事前定義タスクが含まれています：

1. **誤字脱字の検出**: 意図的なエラーを含むテキストを提示し、モデルのエラー識別能力を評価
2. **創造的推論**: オープンエンドな質問で創造的な応答生成をテスト

### 口調パターン

4つの異なるコミュニケーションスタイルをテストします：

- **普通**: 標準的で中立的な依頼形式
- **脅迫**: 断定的で命令的な口調
- **報酬型**: インセンティブを用いたプロンプト
- **丁寧**: 非常に礼儀正しく丁寧な表現

各パターンがすべてのタスクで実行され、比較データを生成します。

## 機能

- 自動化された実験実行（繰り返し回数の設定が可能）
- トークン使用量と実行時間を含む詳細なJSON出力
- 比較テーブル付きのHTMLレポート生成
- 拡張可能なタスクと口調パターンの設定
- APIの制約を尊重するレート制限

## 必要要件

- Python 3.8以上
- OpenAI APIキー
- pip（Pythonパッケージインストーラー）

## インストール

1. リポジトリをクローン：
```bash
git clone <repository-url>
cd prompt-tone-experiments
```

2. 仮想環境を作成：
```bash
# Linux/macOSの場合
python3 -m venv venv
source venv/bin/activate

# Windowsの場合
python -m venv venv
venv\Scripts\activate
```

3. 依存パッケージをインストール：
```bash
pip install -r requirements.txt
```

4. OpenAI APIキーを設定：
```bash
# Linux/macOSの場合
export OPENAI_API_KEY='your-api-key-here'

# Windowsの場合
set OPENAI_API_KEY=your-api-key-here
```

## 使用方法

### 実験の実行

メインスクリプトを実行します：

```bash
python prompt_experiment.py
```

スクリプトは以下の処理を行います：
1. `data/config.json` から設定を読み込み
2. `data/tone_patterns.json` から口調パターンを読み込み
3. すべてのタスク-口調の組み合わせを実行
4. 結果を `results.json` に保存
5. HTMLレポートを `report.html` に生成

### レポートの生成

既に `results.json` ファイルがある場合、HTMLレポートのみを再生成できます：

```bash
python generate_report.py
```

## 設定

### 実験設定

`data/config.json` を編集してカスタマイズ：

```json
{
  "model": "gpt-5.1",
  "output_file": "results.json",
  "html_report_file": "report.html",
  "tasks": [
    {
      "name": "誤字脱字の検出",
      "type": "typo_detection",
      "content_type": "file",
      "content": "typo_text.txt"
    }
  ]
}
```

### 口調パターン

`data/tone_patterns.json` を編集してコミュニケーションスタイルを追加・変更：

```json
{
  "普通": "以下のタスクを完了してください...",
  "丁寧": "大変恐縮ですが、以下のタスクをご対応いただけますと幸いです..."
}
```

## 出力形式

### JSON結果

`results.json` ファイルには以下の情報が含まれます：

```json
{
  "experiment_info": {
    "total_experiments": 8,
    "tasks": ["誤字脱字の検出", "創造的推論"],
    "tone_patterns": ["普通", "脅迫", "報酬", "丁寧"],
    "execution_date": "2025-12-06T...",
    "model": "gpt-4"
  },
  "results": [
    {
      "task_name": "誤字脱字の検出",
      "tone_pattern": "普通",
      "prompt": "...",
      "response": "...",
      "response_length": 1234,
      "timestamp": "2025-12-06T...",
      "execution_time_seconds": 2.5,
      "success": true,
      "usage": {
        "prompt_tokens": 500,
        "completion_tokens": 300,
        "total_tokens": 800
      },
      "model": "gpt-4"
    }
  ]
}
```

### HTMLレポート

生成される `report.html` には以下が含まれます：
- 実験のメタデータと実行サマリー
- 応答の長さ、実行時間、トークン使用量を示す比較テーブル
- 詳細分析用の完全なプロンプトと応答のペア
- 読みやすさを考慮した視覚的スタイリング

## 高度な使用方法

### カスタムタスクの追加

`data/config.json` に新しいタスクを追加：

```json
{
  "name": "カスタムタスク",
  "type": "question",
  "content_type": "inline",
  "content": "ここに質問内容"
}
```

サポートされるタスクタイプ：
- `typo_detection`: エラー識別タスク
- `question`: オープンエンドな質問

### モデルパラメータの調整

`prompt_experiment.py` の `generate()` 関数を編集：

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0,  # 創造性を調整 (0.0-2.0)
    max_tokens=500    # 応答の長さ制限を設定
)
```

## トラブルシューティング

**APIキーエラー**
```
ValueError: OPENAI_API_KEY 環境変数が設定されていません
```
解決方法: OpenAI APIキーが環境変数として設定されているか確認してください

**レート制限エラー**
```
openai.error.RateLimitError: Rate limit exceeded
```
解決方法: スクリプトには自動遅延が含まれていますが、リクエスト頻度を減らすかOpenAIプランをアップグレードする必要がある場合があります

**モジュールが見つからないエラー**
```
ModuleNotFoundError: No module named 'openai'
```
解決方法: 仮想環境が有効化されているか確認し、`pip install -r requirements.txt` を実行してください

