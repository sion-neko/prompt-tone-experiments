#!/usr/bin/env python3
"""
HTMLレポート生成モジュール
"""


import json
from datetime import datetime
from typing import List, Dict, Any


def generate_html_report(results: List[Dict[str, Any]], config: Dict[str, Any], tone_patterns: Dict[str, str], filename: str = "report.html"):
    """
    HTMLレポートを生成
    """
    # タスクごとに結果をグループ化
    tasks_data = {}
    for result in results:
        task_name = result["task_name"]
        if task_name not in tasks_data:
            tasks_data[task_name] = []
        tasks_data[task_name].append(result)

    # JSONデータをHTMLに埋め込むためにシリアライズ
    tasks_data_json = json.dumps(tasks_data, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT プロンプト口調実験レポート</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #3b82f6;
            --primary-dark: #2563eb;
            --secondary-color: #64748b;
            --success-color: #22c55e;
            --error-color: #ef4444;
            --background-color: #f8fafc;
            --surface-color: #ffffff;
            --text-color: #1e293b;
            --border-color: #e2e8f0;
            --sidebar-width: 280px;
        }}

        body {{
            font-family: 'Inter', 'Noto Sans JP', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            margin: 0;
            display: flex;
            min-height: 100vh;
        }}

        /* Sidebar */
        .sidebar {{
            width: var(--sidebar-width);
            background-color: var(--surface-color);
            border-right: 1px solid var(--border-color);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            padding: 2rem 1rem;
            box-sizing: border-box;
            z-index: 10;
        }}

        .sidebar-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .nav-link {{
            display: block;
            padding: 0.75rem 1rem;
            color: var(--secondary-color);
            text-decoration: none;
            border-radius: 0.5rem;
            transition: all 0.2s;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}

        .nav-link:hover, .nav-link.active {{
            background-color: #eff6ff;
            color: var(--primary-color);
        }}
        
        .nav-link.active {{
            font-weight: 700;
        }}

        /* Main Content */
        .main-content {{
            margin-left: var(--sidebar-width);
            flex: 1;
            padding: 2rem 4rem;
            max-width: 1600px;
        }}

        .header-section {{
            margin-bottom: 3rem;
            background: var(--surface-color);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            font-size: 2rem;
            margin: 0 0 1rem 0;
            color: var(--text-color);
        }}
        
        .meta-info {{
            display: flex;
            gap: 2rem;
            color: var(--secondary-color);
            font-size: 0.9rem;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        /* Task Section */
        .task-section {{
            background: var(--surface-color);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 3rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            scroll-margin-top: 2rem;
        }}

        h2 {{
            font-size: 1.5rem;
            margin-top: 0;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}

        /* Comparison View */
        .comparison-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }}

        .comparison-column {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .comparison-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 0.75rem;
        }}
        
        select {{
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            font-size: 0.9rem;
            min-width: 200px;
        }}

        .result-card {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1.5rem;
            height: 100%;
        }}
        
        .prompt-text {{
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.25rem;
            font-size: 0.9rem;
            color: #78350f;
            white-space: pre-wrap;
            height: 120px;
            overflow-y: auto;
        }}

        .response-text {{
            white-space: pre-wrap;
            line-height: 1.7;
            color: #334155;
        }}
        
        .stats-tag {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: #f1f5f9;
            color: #475569;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        /* Tabs */
        .tabs {{
            display: flex;
            gap: 1rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }}

        .tab-btn {{
            padding: 0.75rem 1.5rem;
            background: none;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            font-weight: 500;
            color: var(--secondary-color);
        }}

        .tab-btn.active {{
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
        }}
        
        .hidden {{
            display: none;
        }}

    </style>
</head>
<body>

    <!-- Sidebar -->
    <nav class="sidebar">
        <div class="sidebar-title">実験レポート</div>
        <a href="#header" class="nav-link">概要</a>
        {''.join([f'<a href="#task-{i}" class="nav-link">{name}</a>' for i, name in enumerate(tasks_data.keys())])}
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        <div id="header" class="header-section">
            <h1>GPT プロンプト口調実験レポート</h1>
            <div class="meta-info">
                <div class="meta-item"><span>📅</span> {datetime.now().strftime('%Y年%m月%d日 %H:%M')}</div>
                <div class="meta-item"><span>🤖</span> {config["model"]}</div>
                <div class="meta-item"><span>📊</span> Total Tasks: {len(tasks_data)}</div>
            </div>
        </div>

        {generate_task_sections(tasks_data)}

    </main>

    <script>
        const tasksData = {tasks_data_json};

        function initComparison(taskName, taskIndex) {{
            const leftSelect = document.getElementById(`select-left-${{taskIndex}}`);
            const rightSelect = document.getElementById(`select-right-${{taskIndex}}`);
            
            const render = (side) => {{
                const select = side === 'left' ? leftSelect : rightSelect;
                const pattern = select.value;
                const result = tasksData[taskName].find(r => r.tone_pattern === pattern);
                const container = document.getElementById(`result-${{side}}-${{taskIndex}}`);
                
                if (!result) return;
                
                container.innerHTML = `
                    <div class="prompt-text"><strong>プロンプト:</strong><br>${{escapeHtml(result.prompt)}}</div>
                    <div class="stats-bar">
                        <span class="stats-tag">文字数: ${{result.response_length}}</span>
                        <span class="stats-tag">時間: ${{result.execution_time_seconds.toFixed(2)}}s</span>
                        <span class="stats-tag">トークン: ${{result.usage ? result.usage.total_tokens : 'N/A'}}</span>
                    </div>
                    <div class="response-text">${{escapeHtml(result.response)}}</div>
                `;
            }};

            leftSelect.addEventListener('change', () => render('left'));
            rightSelect.addEventListener('change', () => render('right'));

            // Initial render
            if (leftSelect.options.length > 0) render('left');
            if (rightSelect.options.length > 1) {{
                rightSelect.selectedIndex = 1;
                render('right');
            }} else if (rightSelect.options.length > 0) {{
                render('right');
            }}
        }}

        function escapeHtml(text) {{
            if (!text) return '';
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        // Initialize all comparisons
        document.addEventListener('DOMContentLoaded', () => {{
            Object.keys(tasksData).forEach((taskName, index) => {{
                initComparison(taskName, index);
            }});
        }});
    </script>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTMLレポートを {filename} に保存しました")

def generate_task_sections(tasks_data):
    html = ""
    for i, (task_name, results) in enumerate(tasks_data.items()):
        options = "".join([f'<option value="{r["tone_pattern"]}">{r["tone_pattern"]}</option>' for r in results])
        
        html += f"""
        <section id="task-{i}" class="task-section">
            <h2>{task_name}</h2>
            
            <div class="comparison-container">
                <!-- Left Column -->
                <div class="comparison-column">
                    <div class="comparison-controls">
                        <label>比較 A</label>
                        <select id="select-left-{i}">
                            {options}
                        </select>
                    </div>
                    <div id="result-left-{i}" class="result-card">
                        <!-- Content injected by JS -->
                    </div>
                </div>

                <!-- Right Column -->
                <div class="comparison-column">
                    <div class="comparison-controls">
                        <label>比較 B</label>
                        <select id="select-right-{i}">
                            {options}
                        </select>
                    </div>
                    <div id="result-right-{i}" class="result-card">
                        <!-- Content injected by JS -->
                    </div>
                </div>
            </div>
        </section>
        """
    return html

