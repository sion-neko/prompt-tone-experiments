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
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        select {{
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            font-size: 0.9rem;
            min-width: 200px;
        }}
        
        .run-selector {{
            font-size: 0.9rem;
            color: var(--secondary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .run-btn {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 0.25rem;
            padding: 0.25rem 0.5rem;
            cursor: pointer;
            font-size: 0.8rem;
        }}
        
        .run-btn:hover {{
            background-color: #e2e8f0;
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
        
        .stats-bar {{
            margin-bottom: 1rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
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
        }}
        
        .statistics-panel {{
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }}
        
        .stat-item {{
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--secondary-color);
        }}

        /* Table View */
        .stats-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            font-size: 0.95rem;
        }}
        
        .text-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            font-size: 0.95rem;
        }}

        .stats-table th, .stats-table td, .text-table th, .text-table td {{
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            text-align: left;
        }}

        .stats-table th, .text-table th {{
            font-weight: 600;
            color: var(--secondary-color);
            background-color: #f8fafc;
        }}

        .stats-table th.sortable {{
            cursor: pointer;
            user-select: none;
            position: relative;
            padding-right: 1.5rem;
        }}

        .stats-table th.sortable:hover {{
            background-color: #e2e8f0;
        }}

        .stats-table th.sortable::after {{
            content: '⇅';
            position: absolute;
            right: 0.5rem;
            opacity: 0.3;
            font-size: 0.8rem;
        }}

        .stats-table th.sortable.asc::after {{
            content: '↑';
            opacity: 1;
        }}

        .stats-table th.sortable.desc::after {{
            content: '↓';
            opacity: 1;
        }}

        .stats-table tr:hover, .text-table tr:hover {{
            background-color: #f1f5f9;
        }}
        
        .cell-number {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}
        
        .cell-text {{
            white-space: pre-wrap;
            line-height: 1.6;
            color: #334155;
        }}

        /* Prompt Details */
        .prompt-details {{
            margin-top: 2rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1rem;
        }}

        .prompt-details summary {{
            cursor: pointer;
            color: var(--primary-color);
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        .prompt-item {{
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }}
        
        .prompt-item strong {{
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }}
        
        .prompt-item pre {{
            background-color: #f8fafc;
            border: 1px solid var(--border-color);
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            white-space: pre-wrap;
            color: var(--secondary-color);
            margin: 0;
            font-family: inherit;
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
        const currentRunIndex = {{}}; // Tracks current run index for each comparison panel: key="left-0", val=0

        function initComparison(taskName, taskIndex) {{
            // Only initialize if comparison elements exist (might be table view)
            if (!document.getElementById(`select-left-${{taskIndex}}`)) return;

            const setupSide = (side) => {{
                const selectId = `select-${{side}}-${{taskIndex}}`;
                const select = document.getElementById(selectId);
                const runKey = `${{side}}-${{taskIndex}}`;
                
                // Initialize run index
                currentRunIndex[runKey] = 0;

                const render = () => {{
                    const pattern = select.value;
                    const result = tasksData[taskName].find(r => r.tone_pattern === pattern);
                    const container = document.getElementById(`result-${{side}}-${{taskIndex}}`);
                    
                    if (!result) return;
                    
                    const runIdx = currentRunIndex[runKey] || 0;
                    const runData = result.runs ? result.runs[runIdx] : null;
                    const totalRuns = result.runs ? result.runs.length : 0;
                    
                    // Run Navigator Logic
                    let runNavHtml = '';
                    if (totalRuns > 1) {{
                        runNavHtml = `
                            <div class="run-selector" style="margin-top:0.5rem; width:100%; justify-content:flex-end;">
                                <button class="run-btn" onclick="changeRun('${{runKey}}', -1, ${{totalRuns}})">◀</button>
                                <span>Run ${{runIdx + 1}} / ${{totalRuns}}</span>
                                <button class="run-btn" onclick="changeRun('${{runKey}}', 1, ${{totalRuns}})">▶</button>
                            </div>
                        `;
                    }}
                    
                    // Statistics HTML
                    let statsHtml = '';
                    if (result.statistics && result.statistics.mean !== undefined) {{
                        statsHtml = `
                            <div class="statistics-panel">
                                <div class="stat-item"><strong>統計 (全${{result.runs_count}}回)</strong></div>
                                <div class="stat-item"><span>平均値:</span> <span>${{result.statistics.mean.toFixed(2)}}</span></div>
                                ${{result.statistics.stdev !== undefined ? `<div class="stat-item"><span>標準偏差:</span> <span>${{result.statistics.stdev.toFixed(2)}}</span></div>` : ''}}
                                ${{result.statistics.min !== undefined ? `<div class="stat-item"><span>最小/最大:</span> <span>${{result.statistics.min}} / ${{result.statistics.max}}</span></div>` : ''}}
                            </div>
                        `;
                    }}

                    // Response Data
                    const responseContent = runData ? runData.response : (result.response || "No data");
                    const tokens = runData && runData.usage ? runData.usage.total_tokens : 'N/A';
                    const time = runData ? runData.execution_time_seconds.toFixed(2) : 'N/A';
                    const length = runData ? runData.response_length : 'N/A';

                    container.innerHTML = `
                        <div class="prompt-text"><strong>プロンプト:</strong><br>${{escapeHtml(result.prompt)}}</div>
                        
                        <div class="stats-bar">
                            <span class="stats-tag">文字数: ${{length}}</span>
                            <span class="stats-tag">時間: ${{time}}s</span>
                            <span class="stats-tag">トークン: ${{tokens}}</span>
                        </div>
                        
                        <div class="response-text">${{escapeHtml(responseContent)}}</div>
                        
                        ${{statsHtml}}
                        ${{runNavHtml}}
                    `;
                }};
                
                select.addEventListener('change', () => {{
                    currentRunIndex[runKey] = 0; // Reset run index on pattern change
                    render();
                }});
                
                // Expose render function for global access (for run buttons)
                window[`render_${{runKey}}`] = render;
                
                return render;
            }};

            const renderLeft = setupSide('left');
            const renderRight = setupSide('right');

            // Initial render
            if (document.getElementById(`select-left-${{taskIndex}}`).options.length > 0) renderLeft();
            const rightSelect = document.getElementById(`select-right-${{taskIndex}}`);
            if (rightSelect.options.length > 1) {{
                rightSelect.selectedIndex = 1;
            }}
            if (rightSelect.options.length > 0) renderRight();
        }}
        
        function changeRun(runKey, delta, maxRuns) {{
            const current = currentRunIndex[runKey] || 0;
            let next = current + delta;
            if (next < 0) next = maxRuns - 1;
            if (next >= maxRuns) next = 0;
            
            currentRunIndex[runKey] = next;
            if (window[`render_${{runKey}}`]) {{
                window[`render_${{runKey}}`]();
            }}
        }}

        function escapeHtml(text) {{
            if (!text) return '';
            return String(text)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        // Table sort function
        function sortTable(tableId, colIndex, type) {{
            const table = document.getElementById(tableId);
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const th = table.querySelectorAll('thead th')[colIndex];

            // Determine sort direction
            const isAsc = th.classList.contains('asc');
            const newDir = isAsc ? 'desc' : 'asc';

            // Remove sort classes from all headers
            table.querySelectorAll('thead th').forEach(h => {{
                h.classList.remove('asc', 'desc');
            }});

            // Add sort class to current header
            th.classList.add(newDir);

            // Sort rows
            rows.sort((a, b) => {{
                let aVal = a.cells[colIndex].textContent.trim();
                let bVal = b.cells[colIndex].textContent.trim();

                if (type === 'number') {{
                    // Handle '-' as a very small number for sorting
                    aVal = aVal === '-' ? -Infinity : parseFloat(aVal);
                    bVal = bVal === '-' ? -Infinity : parseFloat(bVal);
                    return newDir === 'asc' ? aVal - bVal : bVal - aVal;
                }} else {{
                    return newDir === 'asc'
                        ? aVal.localeCompare(bVal, 'ja')
                        : bVal.localeCompare(aVal, 'ja');
                }}
            }});

            // Re-append rows in sorted order
            rows.forEach(row => tbody.appendChild(row));
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
        # Determine task type from the first result
        task_type = results[0].get("task_type", "default")
        
        html += f'<section id="task-{i}" class="task-section">'
        html += f'<h2>{task_name}</h2>'
        
        if task_type == "typo_detection":
            html += generate_stats_table(results)
            html += generate_prompt_list(results)
        elif task_type == "question":
            html += generate_text_table(results)
            html += generate_prompt_list(results)
        else:
            html += generate_comparison_view(i, results)
            
        html += '</section>'
            
    return html

def generate_stats_table(results):
    # ユニークなテーブルIDを生成
    import random
    table_id = f"stats-table-{random.randint(1000, 9999)}"

    html = f"""
    <table class="stats-table" id="{table_id}">
        <thead>
            <tr>
                <th class="sortable" data-col="0" data-type="string" style="width: 20%;" onclick="sortTable('{table_id}', 0, 'string')">口調パターン</th>
                <th class="sortable cell-number" data-col="1" data-type="number" onclick="sortTable('{table_id}', 1, 'number')">平均値</th>
                <th class="sortable cell-number" data-col="2" data-type="number" onclick="sortTable('{table_id}', 2, 'number')">標準偏差</th>
                <th class="sortable cell-number" data-col="3" data-type="number" onclick="sortTable('{table_id}', 3, 'number')">最小</th>
                <th class="sortable cell-number" data-col="4" data-type="number" onclick="sortTable('{table_id}', 4, 'number')">最大</th>
                <th class="sortable cell-number" data-col="5" data-type="number" onclick="sortTable('{table_id}', 5, 'number')">サンプル数</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in results:
        stats = r.get("statistics", {})
        mean = f"{stats.get('mean', 0):.2f}" if "mean" in stats else "-"
        stdev = f"{stats.get('stdev', 0):.2f}" if "stdev" in stats else "-"
        min_val = stats.get("min", "-")
        max_val = stats.get("max", "-")
        count = len(r.get("runs", []))

        html += f"""
        <tr>
            <td><strong>{r['tone_pattern']}</strong></td>
            <td class="cell-number">{mean}</td>
            <td class="cell-number">{stdev}</td>
            <td class="cell-number">{min_val}</td>
            <td class="cell-number">{max_val}</td>
            <td class="cell-number">{count}</td>
        </tr>
        """

    html += """
        </tbody>
    </table>
    <div style="margin-top: 1rem; color: #64748b; font-size: 0.9rem;">
        ※ 数値は実験で抽出された誤字脱字の指摘数を示しています。ヘッダーをクリックでソートできます。
    </div>
    """
    return html

def generate_text_table(results):
    html = """
    <table class="text-table">
        <thead>
            <tr>
                <th style="width: 15%;">口調パターン</th>
                <th>回答テキスト</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for r in results:
        # Assuming single run for text table as per user request
        runs = r.get("runs", [])
        response = runs[0].get("response", "") if runs else r.get("response", "")
        
        html += f"""
        <tr>
            <td style="vertical-align: top;"><strong>{r['tone_pattern']}</strong></td>
            <td class="cell-text">{escape_html_py(response)}</td>
        </tr>
        """
        
    html += """
        </tbody>
    </table>
    """
    return html

def generate_prompt_list(results):
    html = """
    <details class="prompt-details">
        <summary>プロンプト詳細を表示</summary>
    """
    
    for r in results:
        html += f"""
        <div class="prompt-item">
            <strong>{r['tone_pattern']}</strong>
            <pre>{escape_html_py(r['prompt'])}</pre>
        </div>
        """
    
    html += "</details>"
    return html

def generate_comparison_view(index, results):
    options = "".join([f'<option value="{r["tone_pattern"]}">{r["tone_pattern"]}</option>' for r in results])
    
    return f"""
    <div class="comparison-container">
        <!-- Left Column -->
        <div class="comparison-column">
            <div class="comparison-controls">
                <label>比較 A</label>
                <select id="select-left-{index}">
                    {options}
                </select>
            </div>
            <div id="result-left-{index}" class="result-card">
                <!-- Content injected by JS -->
            </div>
        </div>

        <!-- Right Column -->
        <div class="comparison-column">
            <div class="comparison-controls">
                <label>比較 B</label>
                <select id="select-right-{index}">
                    {options}
                </select>
            </div>
            <div id="result-right-{index}" class="result-card">
                <!-- Content injected by JS -->
            </div>
        </div>
    </div>
    """

def escape_html_py(text):
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#039;")
