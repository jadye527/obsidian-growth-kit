# ⚫ Obsidian Growth Kit

**AI-powered X/Twitter growth toolkit — autonomous content, analytics, and engagement.**

Built on [OpenClaw](https://openclaw.com). Used by [@ObsidianLabsAI](https://x.com/ObsidianLabsAI) to grow from 0 followers with fully autonomous AI agents.

## What's Inside

| Tool | Description |
|------|------------|
| `xpost` | Full X API CLI — tweet, reply, quote, search, follow, like, thread |
| `xqueue` | Tweet scheduler with 15-min cooldown between posts |
| `xanalytics` | Track followers, impressions, engagement day-over-day |
| `xscout` | Content discovery engine — finds high-engagement tweets in your niche |
| `xgrowth` | Growth tracker — what's working, strategy log, post-type performance |
| `xrecord` | Terminal demo recorder for polished content creation |

Plus: content playbook, dashboard template, cron job configs, and setup automation.

## Quick Start

```bash
git clone https://github.com/jadye527/obsidian-growth-kit.git
cd obsidian-growth-kit
bash install.sh
```

Then edit `~/.config/x-api/keys.env` with your X API credentials and run:

```bash
xpost whoami          # Verify connection
xqueue add "Hello"    # Queue your first post
xscout scan           # Find content in your niche
xgrowth report        # See what's working
```

Full guide: [docs/QUICKSTART.md](docs/QUICKSTART.md)

## How It Works

```
┌─────────────────────────────────────────────────┐
│  Morning (8 AM)                                 │
│  xanalytics snapshot → xscout scan → xqueue add │
│  Queue 4-5 posts, implement 1 new tactic        │
├─────────────────────────────────────────────────┤
│  Throughout Day                                  │
│  xqueue drip (every 15 min) → xpost mentions    │
│  Reply to everything, like relevant content      │
├─────────────────────────────────────────────────┤
│  Content Scout (4x daily)                        │
│  xscout opportunities → like viral tweets        │
│  Queue reactive posts referencing trending topics │
├─────────────────────────────────────────────────┤
│  Nightly (10 PM)                                 │
│  xgrowth report → analyze what worked            │
│  Log strategy, queue tomorrow's posts             │
└─────────────────────────────────────────────────┘
```

## Requirements

- Python 3.10+
- X Developer Account with API credits ([developer.x.com](https://developer.x.com))
- X Premium recommended ($8/mo) for 4x visibility boost
- [OpenClaw](https://openclaw.com) (optional) for autonomous agent operations

## Live Example

See our dashboard: [jadye527.github.io/obsidian-trading/dashboard.html](https://jadye527.github.io/obsidian-trading/dashboard.html)

Watch the agent in action: [Terminal Demo](https://asciinema.org/a/MtIOcUhJ0xBtNIEB)

## License

MIT

## Support

- Product page: [jadye527.github.io/obsidian-trading](https://jadye527.github.io/obsidian-trading/)
- X: [@ObsidianLabsAI](https://x.com/ObsidianLabsAI)
- Email: support@obsidian.jasoncdye.com
