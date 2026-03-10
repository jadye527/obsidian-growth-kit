# Obsidian Growth Kit — Quick Start Guide

## What You Get

6 CLI tools that automate X/Twitter growth for AI builders, solopreneurs, and anyone building in public:

| Tool | What It Does |
|------|-------------|
| `xpost` | Full X API CLI — tweet, reply, quote, search, follow, like, thread |
| `xqueue` | Tweet scheduler with 15-min cooldown between posts |
| `xanalytics` | Track followers, impressions, engagement, day-over-day growth |
| `xscout` | Content discovery — finds high-engagement tweets in your niche |
| `xgrowth` | Growth tracker — what's working, strategy log, performance by post type |
| `xrecord` | Record polished terminal demos of your tools for content |

## Prerequisites

1. **X Developer Account** — [developer.x.com](https://developer.x.com)
   - Create a project + app
   - Set permissions to "Read and Write"
   - Generate OAuth 1.0a keys (consumer key/secret + access token/secret)
   - Purchase API credits at [console.x.com](https://console.x.com)

2. **X Premium** ($8/mo recommended) — 4x visibility boost, analytics access

3. **Python 3.10+** with pip

4. **OpenClaw** (optional but recommended) — [openclaw.com](https://openclaw.com)
   - For autonomous agent operations, heartbeats, and cron scheduling
   - Without OpenClaw you can still use all tools manually

## Installation

```bash
git clone https://github.com/jadye527/obsidian-growth-kit.git
cd obsidian-growth-kit
bash install.sh
```

## Setup

### 1. Add your API keys

Edit `~/.config/x-api/keys.env`:

```env
X_API_KEY=your_consumer_key
X_API_SECRET=your_consumer_secret
TWITTER_BEARER_TOKEN=your_bearer_token
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_USER_HANDLE=YourHandle
```

### 2. Verify connection

```bash
xpost whoami
```

You should see your handle, bio, and follower count.

### 3. Your first post

```bash
xpost tweet "Testing my new growth toolkit. Let's go."
```

## Daily Workflow

### Morning (8-9 AM)
```bash
# Check overnight metrics
xanalytics snapshot
xanalytics compare

# Scout for content to engage with
xscout opportunities

# Queue today's posts
xqueue add "Your post here"
xqueue add "Another post"

# Start the drip (posts every 15 min)
bash -c 'while true; do xqueue next; sleep 900; done' &
```

### Throughout the day
```bash
# Check for mentions — reply to everything
xpost mentions

# Reply substantively
xpost reply <tweet_id> "Your thoughtful reply"

# Like relevant content
xpost like <tweet_id>
```

### Evening (9-10 PM)
```bash
# Full performance review
xgrowth report

# See what worked
xgrowth track

# Plan tomorrow
xqueue add "Tomorrow morning post"
```

## Content Strategy (Felix Playbook)

Based on studying accounts that grew from 0 to 15K+ followers:

### Post Rules
- **Zero hashtags** — algorithm penalizes 3+, Felix uses none
- **Links in replies only** — never in the main post (kills reach)
- **Emojis for structure** — 📊💰📈 for visual scanning, not spam
- **Real numbers** — actual P&L, metrics, data (builds trust)
- **End with questions** — drives replies (13-27x more valuable than likes)

### Content Mix
- 40% Build in Public — real updates, wins, losses, architecture
- 25% Educational — how things work, tutorials, frameworks
- 20% Data/Alpha — analysis, insights, contrarian takes
- 15% Personality — humor, hot takes, failures, lessons

### Growth Tactics
1. Reply to every comment within 30 min
2. Follow 10-20 accounts in your niche daily
3. Like 20-30 tweets daily in your space
4. Post 5-8x daily with the drip scheduler
5. Scout for viral content 3-4x daily
6. Implement one new tactic every morning
7. Review and adjust every night

## Cron Jobs (with OpenClaw)

Copy `examples/cron-jobs.json` entries into your OpenClaw `~/.openclaw/cron/jobs.json`:

- **Morning growth** (8 AM) — analytics, queue posts, implement new tactic
- **Content scout** (9am, 12pm, 3pm, 6pm) — find viral content, like, reference
- **Nightly review** (10 PM) — full analysis, strategy adjustment, plan tomorrow
- **Analytics snapshot** (every 4 hrs) — continuous metric tracking

## Customization

### Add your own topics to xscout

Edit `~/.local/bin/xscout` and modify the `TOPICS` dictionary:

```python
TOPICS = {
    "your-niche": [
        "search query 1",
        "search query 2",
    ],
}
```

### Track your own post categories in xgrowth

Edit the `categorize()` function in `~/.local/bin/xgrowth` to match your content types.

## Support

- Product page: https://jadye527.github.io/obsidian-trading/
- X: [@ObsidianLabsAI](https://x.com/ObsidianLabsAI)
- Email: support@obsidian.jasoncdye.com
