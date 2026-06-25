"""
Live Kanban Dashboard for atlaspay-visual-regen board.

Pulls `hermes kanban list` output, parses tasks, detects worker subprocesses,
and writes a self-refreshing HTML page using the IfeSec brand palette.

Usage:
    python3 generate_kanban_dashboard.py
"""
import subprocess
import re
import os
from pathlib import Path
from datetime import datetime

OUT = Path("/Users/ifeanyi/Documents/IfeSec/Projects/atlaspay-grc-sandbox/dashboards/atlaspay-visual-regen.html")
OUT.parent.mkdir(parents=True, exist_ok=True)

BRAND_GOLD = "#d4af37"
BRAND_CRIMSON = "#8b0000"
BRAND_BLACK = "#0a0a0a"
BG_DARK = "#1a1a1a"
BG_CARD = "#262626"
TEXT_LIGHT = "#f0f0f0"
TEXT_DIM = "#999"

AGENT_INFO = {
    "default": {"llm": "minimax-m3:cloud", "role": "COO / Orchestration"},
    "adeola": {"llm": "ollama/glm-5.2:cloud", "role": "Screenshots / Code"},
    "amara": {"llm": "ollama/kimi-k2.7-code:cloud", "role": "Brand / PDFs"},
    "obinna": {"llm": "ollama/deepseek-v4-pro:cloud", "role": "Cybersecurity / Cert"},
    "ugo": {"llm": "ollama/glm-5.2:cloud", "role": "Status / Mission Control"},
    "zuri": {"llm": "ollama/nemotron-3-super:cloud", "role": "Finance"},
}

STATUS_COLORS = {
    "running": BRAND_GOLD,
    "ready": TEXT_DIM,
    "done": "#4CAF50",
    "blocked": BRAND_CRIMSON,
    "failed": BRAND_CRIMSON,
    "archived": TEXT_DIM,
}


def fetch_kanban():
    result = subprocess.run(["hermes", "kanban", "list"], capture_output=True, text=True, timeout=10)
    return result.stdout


def parse_tasks(text):
    tasks = []
    for line in text.split("\n"):
        m = re.match(r"\s*([●◻⊘▶✓])\s+(\S+)\s+(\w+)\s+(.+)", line)
        if m:
            marker, task_id, status, rest = m.groups()
            parts = rest.strip().split(None, 1)
            assignee = parts[0] if parts else "?"
            title = parts[1] if len(parts) > 1 else rest.strip()
            tasks.append({
                "id": task_id,
                "marker": marker,
                "status": status,
                "assignee": assignee,
                "title": title,
            })
    return tasks


def fetch_workers():
    workers = []
    ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
    for line in ps.stdout.split("\n"):
        if "kanban task" in line and "grep" not in line and "ps aux" not in line:
            parts = line.split()
            profile = "?"
            task_id = "?"
            for i, p in enumerate(parts):
                if p == "-p" and i + 1 < len(parts):
                    profile = parts[i + 1]
                if p.startswith("t_") and len(p) == 10:
                    task_id = p
            workers.append({"profile": profile, "task": task_id})
    return workers


def render_html(tasks, workers):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S EDT")
    counts = {s: 0 for s in STATUS_COLORS}
    for t in tasks:
        counts[t["status"]] = counts.get(t["status"], 0) + 1

    worker_count_by_profile = {}
    for w in workers:
        worker_count_by_profile[w["profile"]] = worker_count_by_profile.get(w["profile"], 0) + 1

    # Render task rows
    task_rows = ""
    for t in tasks:
        agent = AGENT_INFO.get(t["assignee"], {"llm": "?", "role": "?"})
        color = STATUS_COLORS.get(t["status"], TEXT_DIM)
        is_pulsing = 'class="pulsing"' if t["status"] == "running" else ""
        task_rows += f"""
        <tr>
            <td><span class="status-dot" style="background:{color}" {is_pulsing}></span></td>
            <td class="task-id">{t['id']}</td>
            <td class="status" style="color:{color}">{t['status'].upper()}</td>
            <td><strong>{t['assignee']}</strong><br/><span class="llm">{agent['llm']}</span></td>
            <td>{t['title']}</td>
        </tr>
        """

    # Worker rows
    worker_rows = ""
    for w in workers:
        agent = AGENT_INFO.get(w["profile"], {"llm": "?", "role": "?"})
        worker_rows += f"""
        <tr>
            <td><span class="status-dot pulsing" style="background:{BRAND_GOLD}"></span></td>
            <td><strong>{w['profile']}</strong> <span class="llm">({agent['llm']})</span></td>
            <td>{w['task']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AtlasPay Visual Regen — Live Kanban</title>
<meta http-equiv="refresh" content="30">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: {BG_DARK}; color: {TEXT_LIGHT}; font-family: 'Helvetica Neue', Arial, sans-serif; padding: 24px; }}
h1 {{ color: {BRAND_GOLD}; font-size: 28px; margin-bottom: 8px; }}
h2 {{ color: {BRAND_GOLD}; font-size: 18px; margin: 32px 0 12px 0; border-bottom: 1px solid {BRAND_GOLD}; padding-bottom: 6px; }}
.meta {{ color: {TEXT_DIM}; font-size: 12px; margin-bottom: 24px; }}
.kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
.kpi {{ background: {BG_CARD}; padding: 16px; border-radius: 6px; border-left: 3px solid {BRAND_GOLD}; }}
.kpi .num {{ font-size: 32px; font-weight: bold; color: {BRAND_GOLD}; }}
.kpi .label {{ font-size: 11px; color: {TEXT_DIM}; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }}
.kpi.blocked {{ border-left-color: {BRAND_CRIMSON}; }}
.kpi.blocked .num {{ color: {BRAND_CRIMSON}; }}
table {{ width: 100%; border-collapse: collapse; background: {BG_CARD}; border-radius: 6px; overflow: hidden; }}
th {{ background: {BRAND_BLACK}; color: {BRAND_GOLD}; padding: 12px 8px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }}
td {{ padding: 12px 8px; border-top: 1px solid #333; font-size: 13px; }}
.task-id {{ font-family: 'Courier New', monospace; color: {TEXT_DIM}; }}
.status {{ font-weight: bold; font-size: 11px; }}
.llm {{ color: {TEXT_DIM}; font-size: 10px; font-family: 'Courier New', monospace; }}
.status-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }}
.pulsing {{ animation: pulse 1.2s ease-in-out infinite; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.4; transform: scale(0.85); }} }}
.legend {{ color: {TEXT_DIM}; font-size: 11px; margin-top: 24px; padding-top: 12px; border-top: 1px solid #333; }}
</style>
</head>
<body>
<h1>AtlasPay Visual Regen — Live Kanban</h1>
<p class="meta">Board: atlaspay-visual-regen · Last refresh: {now} · Auto-refresh every 30s</p>

<div class="kpi-row">
    <div class="kpi"><div class="num">{counts.get('ready', 0)}</div><div class="label">Ready</div></div>
    <div class="kpi"><div class="num">{counts.get('running', 0)}</div><div class="label">Running</div></div>
    <div class="kpi"><div class="num">{counts.get('done', 0)}</div><div class="label">Done</div></div>
    <div class="kpi {'blocked' if counts.get('blocked', 0) > 0 else ''}"><div class="num">{counts.get('blocked', 0)}</div><div class="label">Blocked</div></div>
</div>

<h2>Active Workers ({len(workers)})</h2>
<table>
    <thead><tr><th>Status</th><th>Profile / LLM</th><th>Task</th></tr></thead>
    <tbody>
    {worker_rows if worker_rows else '<tr><td colspan="3" style="color:{TEXT_DIM}; text-align: center; padding: 24px;">No active workers</td></tr>'}
    </tbody>
</table>

<h2>All Tasks ({len(tasks)})</h2>
<table>
    <thead><tr><th>●</th><th>Task ID</th><th>Status</th><th>Agent / LLM</th><th>Title</th></tr></thead>
    <tbody>
    {task_rows}
    </tbody>
</table>

<p class="legend">
AtlasPay SOC 2 Type 1 readiness package — visual regeneration + PDF v2 quality upgrade.
Phase: filter-aware screenshot capture → PDF v2 regen (briefing + risk register) → README integration → visual QA → commit + push to GitHub.
</p>

</body>
</html>"""


def main():
    kanban_text = fetch_kanban()
    tasks = parse_tasks(kanban_text)
    workers = fetch_workers()
    html = render_html(tasks, workers)
    OUT.write_text(html)
    print(f"Wrote {OUT} ({len(tasks)} tasks, {len(workers)} active workers)")


if __name__ == "__main__":
    main()