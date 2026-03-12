# Obsidian Command Center — Dashboard Improvements

## Overview
Enhance the agent orchestration dashboard. The v1 HTML is at `/home/jasondye/openclaw-workspace/agent-dashboard/index.html`. Make it pull live data instead of hardcoded JSON.

## Requirements

### Data Collection Layer
- [x] Create `collect.py` in agent-dashboard/ — scans agent state, writes `dashboard-state.json`
- [x] Scan tmux sessions for agent health (`tmux -S ~/.tmux/sock list-sessions`)
- [x] Read PRD.md files from agent dirs for task progress (checked vs unchecked)
- [x] Parse `/tmp/metar_daemon.log` tail for daemon status
- [x] Check process health: `pgrep -f` for metar_daemon, five_min_monitor, xqueue
- [x] Read paper_trades.db for trading stats (win rate, P&L, last trade date)

### Dashboard Enhancements
- [x] Make `index.html` fetch `dashboard-state.json` instead of hardcoded DATA
- [x] Add auto-refresh (poll every 60 seconds)
- [x] Add "last refreshed" live timestamp
- [x] Add responsive mobile layout
- [x] Add expandable task details on click

### Cost Tracking
- [x] Create `cost-tracker.json` format for monthly cost entries
- [x] Render cost history chart (month-over-month)

### Agent Communication Log
- [x] Create `activity-log.jsonl` that agents append events to
- [x] Display in timeline with filtering by agent

## Tech Stack
- Pure HTML/CSS/JS (no build tools, no npm)
- Tailwind CSS via CDN
- Python for data collection
- JSON/JSONL for data

## Constraints
- No build step — must work as static files on GitHub Pages
- Data collection runs via cron, dashboard is read-only
- Do not expose credentials
