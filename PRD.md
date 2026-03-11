# Obsidian Command Center — Dashboard Improvements

## Overview
Enhance the agent orchestration dashboard. The v1 HTML is at `/home/jasondye/openclaw-workspace/agent-dashboard/index.html`. Make it pull live data instead of hardcoded JSON.

## Requirements

### Data Collection Layer
- [ ] Create `collect.py` in agent-dashboard/ — scans agent state, writes `dashboard-state.json`
- [ ] Scan tmux sessions for agent health (`tmux -S ~/.tmux/sock list-sessions`)
- [ ] Read PRD.md files from agent dirs for task progress (checked vs unchecked)
- [ ] Parse `/tmp/metar_daemon.log` tail for daemon status
- [ ] Check process health: `pgrep -f` for metar_daemon, five_min_monitor, xqueue
- [ ] Read paper_trades.db for trading stats (win rate, P&L, last trade date)

### Dashboard Enhancements
- [ ] Make `index.html` fetch `dashboard-state.json` instead of hardcoded DATA
- [ ] Add auto-refresh (poll every 60 seconds)
- [ ] Add "last refreshed" live timestamp
- [ ] Add responsive mobile layout
- [ ] Add expandable task details on click

### Cost Tracking
- [ ] Create `cost-tracker.json` format for monthly cost entries
- [ ] Render cost history chart (month-over-month)

### Agent Communication Log
- [ ] Create `activity-log.jsonl` that agents append events to
- [ ] Display in timeline with filtering by agent

## Tech Stack
- Pure HTML/CSS/JS (no build tools, no npm)
- Tailwind CSS via CDN
- Python for data collection
- JSON/JSONL for data

## Constraints
- No build step — must work as static files on GitHub Pages
- Data collection runs via cron, dashboard is read-only
- Do not expose credentials
