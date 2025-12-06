#!/usr/bin/env python3
"""
既存のresults.jsonからHTMLレポートを生成するスクリプト
"""

import json
from report_generator import generate_html_report

# results.jsonを読み込む
with open("results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 設定情報を復元
config = {
    "model": data["experiment_info"]["model"],
    "tasks": [{"name": task_name} for task_name in data["experiment_info"]["tasks"]]
}

# 口調パターンを復元
tone_patterns = {pattern: pattern for pattern in data["experiment_info"]["tone_patterns"]}

# HTMLレポート生成
generate_html_report(data["results"], config, tone_patterns, "report.html")
print("HTMLレポートが生成されました。report.html をブラウザで開いてください。")
