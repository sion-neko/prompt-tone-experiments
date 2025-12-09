# LLM プロンプト口調実験ツール

異なるプロンプトの口調がLLMの応答にどのような影響を与えるかを分析する研究ツールです。

## デモ

実験結果のHTMLレポートは以下で確認できます：

**[実験結果レポート](https://sion-neko.github.io/prompt-tone-experiments/)**

## 概要

このツールは、同一のタスクを異なる口調のプロンプトでLLMに送信し、その応答を比較する実験を行います。プロンプトの書き方がAIの振る舞いにどう影響するかを定量的に分析します。

### 実験タスク

1. **誤字脱字の検出**: 意図的なエラーを含むテキストを提示し、モデルのエラー識別能力を評価（複数回実行で統計分析）
2. **大喜利**: オープンエンドな質問で創造的な応答生成をテスト

### 口調パターン

6つの異なるコミュニケーションスタイルをテストします：

| パターン | 説明 |
|---------|------|
| 普通 | 標準的で中立的な依頼形式 |
| 普通2 | カジュアルな依頼形式 |
| 丁寧 | 非常に礼儀正しく丁寧な表現 |
| 脅迫 | 断定的で命令的な口調 |
| 脅迫2 | 感情的な圧力を用いた口調 |
| 報酬 | インセンティブを用いたプロンプト |

## 機能

- 自動化された実験実行（タスクごとに繰り返し回数を設定可能）
- 統計分析（平均値、標準偏差、最小/最大値）
- トークン使用量と実行時間の記録
- ソート可能なテーブル付きHTMLレポート生成
- 拡張可能なタスクと口調パターンの設定

## プロジェクト構成

```
prompt-tone-experiments/
├── prompt_experiment.py  # メイン実験スクリプト
├── report_generator.py   # HTMLレポート生成モジュール
├── merge_results.py      # 複数結果ファイルのマージ
├── requirements.txt      # Python依存パッケージ
├── data/
│   ├── config.json       # 実験設定
│   ├── tone_patterns.json # 口調パターン定義
│   └── typo_text.txt     # 誤字脱字検出用テキスト
├── output/
│   ├── results.json      # 実験結果（JSON）
│   └── results2.json     # 追加実験結果
└── docs/
    └── index.html        # HTMLレポート（GitHub Pages用）
```

## 必要要件

- Python 3.8以上
- OpenAI APIキー

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/sion-neko/prompt-tone-experiments.git
cd prompt-tone-experiments
```

2. 仮想環境を作成：
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. 依存パッケージをインストール：
```bash
pip install -r requirements.txt
```

4. OpenAI APIキーを設定：
```bash
# Linux/macOS
export OPENAI_API_KEY='your-api-key-here'

# Windows
set OPENAI_API_KEY=your-api-key-here
```

## 使用方法

### 実験の実行

```bash
python prompt_experiment.py
```

実行すると：
1. `data/config.json` から設定を読み込み
2. `data/tone_patterns.json` から口調パターンを読み込み
3. すべてのタスク×口調の組み合わせを実行
4. 結果を `output/results.json` に保存
5. HTMLレポートを `docs/index.html` に生成

### HTMLレポートの再生成

既存の `output/results.json` からHTMLレポートのみを再生成：

```bash
python report_generator.py
```

### 複数結果ファイルのマージ

複数の実験結果を1つのHTMLレポートにマージ：

```bash
python merge_results.py
```

## 設定

### 実験設定 (`data/config.json`)

```json
{
  "model": "gpt-4o",
  "runs_per_task": 10,
  "tasks": [
    {
      "name": "誤字脱字の指摘",
      "type": "typo_detection",
      "content_type": "file",
      "content": "typo_text.txt",
      "instruction": "誤字・脱字の総数を数字のみで出力"
    },
    {
      "name": "大喜利",
      "type": "question",
      "content_type": "inline",
      "content": "お題の内容"
    }
  ]
}
```

**設定項目:**
- `model`: 使用するOpenAIモデル
- `runs_per_task`: typo_detectionタスクの実行回数（統計分析用）
- `tasks`: 実験タスクのリスト

### 口調パターン (`data/tone_patterns.json`)

```json
{
  "普通": "以下の指示に従ってください。",
  "丁寧": "大変恐縮ですが..."
}
```

## 出力形式

### JSON結果 (`output/results.json`)

```json
{
  "experiment_info": {
    "total_experiments": 12,
    "tasks": ["誤字脱字の指摘", "大喜利"],
    "tone_patterns": ["普通", "普通2", "丁寧", "脅迫", "脅迫2", "報酬"],
    "execution_date": "2025-12-08T...",
    "model": "gpt-4o"
  },
  "results": [
    {
      "task_name": "誤字脱字の指摘",
      "task_type": "typo_detection",
      "tone_pattern": "普通",
      "prompt": "...",
      "runs": [...],
      "runs_count": 10,
      "statistics": {
        "mean": 13.4,
        "stdev": 1.35,
        "min": 11,
        "max": 15,
        "values": [12, 14, 14, ...]
      }
    }
  ]
}
```

### HTMLレポート (`docs/index.html`)

- 実験のメタデータと実行サマリー
- ソート可能な統計テーブル（平均値、標準偏差、最小/最大）
- 各口調パターンのプロンプト詳細
- レスポンシブデザイン

## ライセンス

MIT License
