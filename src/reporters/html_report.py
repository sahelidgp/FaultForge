import os
import webbrowser
from datetime import datetime


def generate_report(target_file, results):
    total_mutations = len(results)
    killed_count = sum(r['status'] == 'KILLED' for r in results)
    survived_count = total_mutations - killed_count

    mutation_score = int((killed_count / total_mutations) * 100) if total_mutations > 0 else 0

    # Score color & label
    if mutation_score > 80:
        status_color = "#2ea043"
        score_label = "Excellent"
    elif mutation_score > 50:
        status_color = "#d29922"
        score_label = "Moderate"
    else:
        status_color = "#f85149"
        score_label = "Weak"

    insight = ""
    if survived_count > 0:
        insight = f"""
        <div class="insight-box">
            ⚠️ <strong>Test Weakness Detected:</strong> {survived_count} mutant(s) survived.
            This indicates missing edge case or boundary test coverage.
        </div>
        """

    table_rows = ""
    for res in results:
        badge_class = "status-killed" if res['status'] == 'KILLED' else "status-survived"

        reason_html = ""
        if res['status'] == 'SURVIVED' and res.get("reason"):
            reason_html = f"""
            <div class="reason-text">⚠️ {res['reason']}</div>
            """

        table_rows += f"""
        <tr>
            <td>#{res['id']}</td>
            <td>
                <span class="code-block">{res['name']}</span>
                {reason_html}
            </td>
            <td>
                <span class="status-badge {badge_class}">
                    {res['status']}
                </span>
            </td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mutation Report | {target_file}</title>

<style>
:root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text-main: #c9d1d9;
    --text-muted: #8b949e;
    --green: #2ea043;
    --red: #f85149;
    --yellow: #d29922;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg);
    color: var(--text-main);
    padding: 40px;
    display: flex;
    justify-content: center;
}}

.dashboard {{
    width: 100%;
    max-width: 900px;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1px solid var(--border);
    padding-bottom: 15px;
    margin-bottom: 30px;
}}

.header h1 {{
    margin: 0;
    font-size: 24px;
}}

.meta {{
    color: var(--text-muted);
    font-size: 14px;
}}

.metrics-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}}

.metric-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}}

.metric-value {{
    font-size: 32px;
    font-weight: bold;
    margin: 10px 0 5px 0;
}}

.metric-label {{
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.score-card {{
    border-color: {status_color};
    box-shadow: 0 0 15px {status_color}20;
}}

.score-card .metric-value {{
    color: {status_color};
}}

.insight-box {{
    margin-bottom: 25px;
    padding: 15px;
    border: 1px solid var(--yellow);
    border-radius: 8px;
    background: #161b22;
    color: var(--text-main);
}}

.details-section {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}}

.details-header {{
    background: #010409;
    padding: 15px 20px;
    font-weight: bold;
    border-bottom: 1px solid var(--border);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
}}

th {{
    color: var(--text-muted);
    font-weight: 500;
}}

.code-block {{
    background: #0d1117;
    padding: 4px 8px;
    border-radius: 4px;
    font-family: monospace;
    color: #ff7b72;
    border: 1px solid var(--border);
}}

.reason-text {{
    color: var(--text-muted);
    font-size: 12px;
    margin-top: 5px;
}}

.status-badge {{
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}}

.status-killed {{
    background: var(--green);
    color: white;
}}

.status-survived {{
    background: var(--red);
    color: white;
}}
</style>
</head>

<body>
<div class="dashboard">

<div class="header">
    <h1>🧬 Mutation Test Execution Report</h1>
    <div class="meta">
        Target: <strong>{target_file}</strong> |
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
    </div>
</div>

<div class="metrics-grid">
    <div class="metric-card score-card">
        <div class="metric-label">Total Score ({score_label})</div>
        <div class="metric-value">{mutation_score}%</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Mutants Injected</div>
        <div class="metric-value">{total_mutations}</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Mutants Killed</div>
        <div class="metric-value" style="color: var(--green);">{killed_count}</div>
    </div>

    <div class="metric-card">
        <div class="metric-label">Mutants Survived</div>
        <div class="metric-value" style="color: var(--red);">{survived_count}</div>
    </div>
</div>

{insight}

<div class="details-section">
    <div class="details-header">Detailed Mutation Log (Isolated Execution)</div>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Mutation Applied</th>
                <th>Execution Status</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</div>

</div>
</body>
</html>
"""

    report_path = "mutation_report.html"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    webbrowser.open(f"file://{os.path.abspath(report_path)}")

    return report_path