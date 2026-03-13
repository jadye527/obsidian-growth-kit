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

## CRITICAL — X Media Posting (Due: 2026-03-13 09:18 AM ET)

The launch tweet with the Charlie meme MUST go out tomorrow morning. `xpost` CLI exists at `~/.local/bin/xpost` and keys are at `~/.config/x-api/keys.env`.

- [x] Verify `xpost` can post with media: test `xpost --media /home/jasondye/.openclaw/workspace-obsidian/out/charlie_fire_v1d.png --text "test"` (delete test tweet after)
- [x] If xpost media upload fails, debug and fix it — check tweepy v2 media upload flow
- [x] Set up a cron or scheduled task to post at 2026-03-13 09:18 AM ET with: image `out/charlie_fire_v1d.png` and copy from `x-post-release-package-2026-03-12.md`
- [x] Confirm the post went out successfully

Post copy is at: `/home/jasondye/.openclaw/workspace-obsidian/x-post-release-package-2026-03-12.md`
Image asset: `/home/jasondye/.openclaw/workspace-obsidian/out/charlie_fire_v1d.png`

## CRITICAL — Mission Control Login via Cloudflare Tunnel

Login at https://opportunity-grove-bags-grounds.trycloudflare.com redirects back to login with no error after submitting valid credentials. The API returns 200 and sets a session cookie, but the browser silently rejects it.

**Root cause:** cloudflared terminates TLS and forwards to Next.js over plain HTTP on localhost. It does NOT inject `X-Forwarded-Proto: https`. The server sees HTTP, so it doesn't set `Secure` on the cookie. But `SameSite=none` REQUIRES `Secure` — browsers silently drop the cookie.

**What was already tried:**
- Set `MC_COOKIE_SAMESITE=none` in `.env` (done)
- Set `MC_COOKIE_SECURE=true` in `.env` (done)
- Recreated Docker container with `docker compose up -d --force-recreate` (done)
- Verified cookie now shows `Secure; SameSite=none` via curl (confirmed)
- BUT login still fails in browser — needs deeper investigation

Tasks:
- [x] Investigate why browser login still fails despite correct cookie flags — check CSP headers, CORS, redirect logic, or Next.js middleware host validation
- [x] Test the full browser flow: POST /api/auth/login → set cookie → redirect to / → GET /api/auth/me with cookie
- [x] Check if Next.js middleware is stripping/rejecting the cookie or blocking the tunneled host
- [x] Fix the issue and confirm login works end-to-end through the Cloudflare tunnel
- [x] Clean up: remove meme images from `mission-control/public/` after testing

Config location: `/home/jasondye/.openclaw/workspace-obsidian/mission-control/.env`
Docker: `cd /home/jasondye/.openclaw/workspace-obsidian/mission-control && docker compose up -d --force-recreate`

## CRITICAL — Persistent Daily X Posting Schedule (2x/day with memes + engagement)

Obsidian currently uses session-only cron jobs for daily X posting, which die when the session exits. This needs to be a permanent system-level solution.

**Requirements:**
The @ObsidianLabsAI account posts 2x daily with original memes + engagement replies. Every critical recurring task must be persistent (survives reboots, session exits).

### Posting Pipeline (runs at 9 AM ET and 6 PM ET daily)
1. Scan X for trending topics in AI/startup/build-in-public space
2. Write copy in our voice: self-deprecating startup humor, real build-in-public stories
3. Generate a fresh meme using `memegen.py` at `/home/jasondye/.openclaw/workspace-obsidian/out/` (venv at `out/.venv/bin/python`, templates in `out/templates/`)
4. End every post with a question or hot take to drive replies
5. Include #buildinpublic tag
6. Post with: `xpost tweet "copy" --media /path/to/meme.png`
7. Within 10 min of posting, add a self-reply thread with more context + a question
8. Check mentions and reply to 2-3 engaged followers with substance + questions (not spam)

### Tasks
- [x] Set up persistent system-level cron (crontab or systemd timer) for 9 AM ET and 6 PM ET daily posting
- [x] Each cron job should invoke a script that handles the full pipeline above autonomously
- [x] The script must generate a NEW meme each time (not reuse old ones)
- [x] Add variety to meme templates — download 5-10 more popular templates to `out/templates/`
- [x] Test the full pipeline end-to-end: cron fires → meme generated → post goes out → self-reply added → mentions replied to
- [x] Ensure the cron survives reboots (not session-only)

**DO NOT mark tasks as done unless you have ACTUALLY completed them. Verify your work before checking off.**

### Important context
- `xpost` CLI at `~/.local/bin/xpost` (tweepy + OAuth, keys at `~/.config/x-api/keys.env`)
- `memegen.py` at `/home/jasondye/.openclaw/workspace-obsidian/out/memegen.py` — uses Pillow, venv at `out/.venv/`
- X blocks cold replies to accounts that haven't engaged with us — only reply to people in our mentions or who've interacted
- Copy style reference: see today's posts on @ObsidianLabsAI for tone

### Rule for ALL critical scheduled items
Any recurring task that is critical to operations MUST use persistent scheduling (system crontab or systemd timers). Session-only cron is for temporary/one-off use only. If it matters, it must survive a reboot.

## REQUIRED — Adopt Shared Memory System

All agents must use the shared memory system at `/home/jasondye/.openclaw/workspace-obsidian/memory/`.

Read `inbox/from-obsidian-002.md` for full instructions.

- [x] PROOF REQUIRED: Add a new section "## Ralph's Session Log" to `/home/jasondye/.openclaw/workspace-obsidian/memory/ralph.md` with today's date and what you actually worked on. The supervisor will check this file's modification time.
- [x] PROOF REQUIRED: Run `curl -s "http://127.0.0.1:3000/api/memory?action=search&query=ralph" -H "x-api-key: f8496446d5cfc7beca41f40e21edcb1f"` and save the output to `/tmp/ralph-memory-test.json`. Supervisor will verify this file exists.
- [x] PROOF REQUIRED: Move `inbox/from-obsidian-002.md` to `inbox/processed/from-obsidian-002.md`. Supervisor will check.

**STOP FAKING COMPLETIONS. The supervisor validates artifacts. If you check these off without doing them, they get unchecked and you restart.**

## Constraints
- No build step — must work as static files on GitHub Pages
- Data collection runs via cron, dashboard is read-only
- Do not expose credentials
