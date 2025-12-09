#!/usr/bin/env python3
"""
GPTプロンプト口調実験スクリプト
異なる口調でGPT-4に質問し、応答の違いを記録する
"""

import os
import re
import json
import statistics
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from openai import OpenAI
from report_generator import generate_html_report

# データディレクトリのパス
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


def load_file(filename: str) -> Any:
    """
    JSONファイルを読み込む

    Args:
        filename: ファイル名

    Returns:
        JSONファイルの内容を含む辞書
    """

    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        if filename.endswith(".json"):
            return json.load(f)
        elif filename.endswith(".txt"):
            return f.read().strip()
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    


def extract_number(text: str) -> Optional[int]:
    """
    テキストから数値を抽出する

    Args:
        text: レスポンステキスト

    Returns:
        抽出された数値、または抽出できない場合はNone
    """
    if not text:
        return None
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None


def generate(client: OpenAI, prompt: str, model: str = "gpt-4") -> Dict[str, Any]:
    """
    GPT APIを呼び出す

    Args:
        prompt: 送信するプロンプト
        model: 使用するモデル名

    Returns:
        APIレスポンスと応答内容を含む辞書
    """
    try:
        response = client.responses.create(
            model=model,
            input=prompt
        )

        # responses API uses output_text instead of choices
        answer = response.output_text

        return {
            "success": True,
            "answer": answer,
            "answer_length": len(answer) if answer else 0,
            "model": model,
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "answer": None,
            "answer_length": 0
        }


def build_prompt(task: Dict[str, Any], tone_instruction: str) -> str:
    """
    タスクと口調からプロンプトを構築

    Args:
        task: タスク情報の辞書
        tone_instruction: 口調パターンの指示文

    Returns:
        完全なプロンプト文字列
    """
    task_type = task["type"]
    content = task["content"]

    if task_type == "typo_detection":
        return f"{tone_instruction}\n\n次の文章に含まれる誤字・脱字・文法ミスの総数を数えてください。回答は数字のみで出力してください（例: 5）。\n{content}"
    elif task_type == "question":
        return f"{tone_instruction}\n\n大喜利です。以下のお題から、面白い回答を1つだけ答えてください。\n{content}"
    else:
        raise ValueError(f"Unsupported task type: {task_type}")


def run_experiment(client: OpenAI, config: Dict[str, Any], tone_patterns: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    実験を実行する

    Args:
        client: OpenAI クライアント
        config: 実験設定
        tone_patterns: 口調パターン

    Returns:
        実験結果のリスト
    """
    results = []
    tasks = config["tasks"]
    model = config["model"]
    runs_per_task = config["runs_per_task"]

    for task in tasks:
        task_name = task["name"]
        task_type = task["type"]

        # タスクのコンテンツを読み込み
        if task["content_type"] == "file":
            task["content"] = load_file(task["content"])

        for tone_key, tone_instruction in tone_patterns.items():
            # プロンプト構築
            prompt = build_prompt(task, tone_instruction)

            # 複数回実行用のデータ
            run_results = []
            extracted_values = []

            # typo_detectionは複数回、それ以外は1回
            actual_runs = runs_per_task if task_type == "typo_detection" else 1

            for run_num in range(actual_runs):
                print(f"  実行 {run_num + 1}/{actual_runs}...", end=" ")

                # API呼び出し
                start_time = datetime.now()
                api_result = generate(client, prompt, model)
                end_time = datetime.now()

                if api_result["success"]:
                    print(f"✓ ({api_result['answer']})")
                    # 数値を抽出（typo_detectionの場合）
                    if task_type == "typo_detection":
                        extracted = extract_number(api_result["answer"])
                        if extracted is not None:
                            extracted_values.append(extracted)
                else:
                    print(f"✗ エラー: {api_result['error']}")

                run_results.append({
                    "run_number": run_num + 1,
                    "response": api_result["answer"],
                    "response_length": api_result["answer_length"],
                    "execution_time_seconds": (end_time - start_time).total_seconds(),
                    "success": api_result["success"],
                    "extracted_value": extract_number(api_result["answer"]) if api_result["success"] else None,
                    "usage": api_result.get("usage"),
                    "error": api_result.get("error")
                })

            # 統計情報を計算
            stats = {}
            if extracted_values:
                stats["mean"] = statistics.mean(extracted_values)
                stats["values"] = extracted_values
                if len(extracted_values) >= 2:
                    stats["stdev"] = statistics.stdev(extracted_values)
                    stats["min"] = min(extracted_values)
                    stats["max"] = max(extracted_values)

            # 結果を記録
            result = {
                "task_name": task_name,
                "task_type": task_type,
                "tone_pattern": tone_key,
                "prompt": prompt,
                "runs": run_results,
                "runs_count": actual_runs,
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "statistics": stats
            }

            results.append(result)

    print("\n" + "=" * 60)
    print("実験が完了しました")

    return results


def save_results(results: List[Dict[str, Any]], config: Dict[str, Any], tone_patterns: Dict[str, str], filename: str = "output/results.json"):
    """
    結果をJSONファイルに保存

    Args:
        results: 実験結果のリスト
        config: 実験設定
        tone_patterns: 口調パターン
        filename: 保存先ファイル名
    """
    output = {
        "experiment_info": {
            "total_experiments": len(results),
            "tasks": [task["name"] for task in config["tasks"]],
            "tone_patterns": list(tone_patterns.keys()),
            "execution_date": datetime.now().isoformat(),
            "model": config["model"],
        },
        "results": results
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n結果を {filename} に保存しました")


def main():
    """メイン関数"""
    try:
        # 出力ディレクトリの作成
        OUTPUT_DIR.mkdir(exist_ok=True)

        # OpenAI クライアントの初期化
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 環境変数が設定されていません")
        client = OpenAI(api_key=api_key)

        # 設定の読み込み
        config = load_file("config.json")
        tone_patterns = load_file("tone_patterns.json")

        # 実験実行
        results = run_experiment(client, config, tone_patterns)

        # 結果保存
        output_file = config.get("output_file", "output/results.json")
        save_results(results, config, tone_patterns, output_file)

        # HTMLレポート生成
        html_file = config.get("html_report_file", "output/index.html")
        generate_html_report(results, config, tone_patterns, html_file)

    except FileNotFoundError as e:
        print(f"\nエラー: 必要なファイルが見つかりません: {e}")
        print("data/ ディレクトリに必要なファイルが存在するか確認してください")
    except ValueError as e:
        print(f"\nエラー: {e}")
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
