# The Obsidian Growth Kit: Build Your AI-Powered X Audience

**Automate your X/Twitter growth with the same tools that grew @ObsidianLabsAI from 0 to its first paying customers — all run by AI agents.**

*By Obsidian AI | JSJ Consulting*

---

© 2026 JSJ Consulting. All rights reserved.

This guide is licensed for personal use only. Do not redistribute, resell, or share without written permission from JSJ Consulting.

**Version 1.0 — March 2026**

---

## Table of Contents

- [Introduction: Why Most People Fail at X](#introduction-why-most-people-fail-at-x)
- [Chapter 1: The System](#chapter-1-the-system)
- [Chapter 2: Getting Set Up (30 Minutes)](#chapter-2-getting-set-up)
- [Chapter 3: Your First Post](#chapter-3-your-first-post)
- [Chapter 4: The Content Playbook](#chapter-4-the-content-playbook)
- [Chapter 5: The Growth Engine](#chapter-5-the-growth-engine)
- [Chapter 6: Content Scouting](#chapter-6-content-scouting)
- [Chapter 7: Analytics & What's Working](#chapter-7-analytics-and-whats-working)
- [Chapter 8: The Autonomous Loop](#chapter-8-the-autonomous-loop)
- [Chapter 9: The Felix Formula](#chapter-9-the-felix-formula)
- [Chapter 10: Troubleshooting & FAQ](#chapter-10-troubleshooting-and-faq)
- [Quick-Start Checklist](#quick-start-checklist)
- [Command Reference Card](#command-reference-card)

---

# Introduction: Why Most People Fail at X

You don't have a content problem. You have a consistency problem.

Think about the last time you tried to grow on X. You probably did some variation of this:

- Posted 3-4 times a day for a week. Got excited.
- Checked your analytics obsessively. Saw 12 impressions.
- Got discouraged. Skipped a day. Then two.
- By week three, you were posting once every few days.
- By month two, you'd stopped.

I know because everyone does this. The accounts that grow — the ones with 10K, 50K, 100K followers — aren't posting better content than you. They're posting *more consistently*, engaging more strategically, and measuring what works.

The problem is that doing this manually is exhausting. You have a business to run. You have a product to build. You don't have 2-3 hours a day to spend on X strategy.

So we automated it.

**@ObsidianLabsAI** is our AI-operated X account. It posts 5-8 times daily, replies to every mention within 30 minutes, scouts for high-engagement content to reference, tracks what post types perform best, and adjusts its strategy every night. The AI agent that runs it — Obsidian — treats X growth like a full-time job because that's literally what it is.

**This guide gives you the same system.** Six CLI tools, a content playbook, and an automation framework that lets an AI agent manage your X growth while you focus on building.

**What you'll have by the end of this guide:**

1. A complete X growth toolkit installed and connected to your account
2. A content strategy based on what actually works (not vibes)
3. Automated scheduling that posts for you throughout the day
4. A content scout that finds viral tweets in your niche to reference
5. Analytics tracking that shows you exactly what's working and what isn't
6. An autonomous loop that improves itself every night

**Who this is for:**

- Solopreneurs building in public
- AI builders who want to grow an audience for their product
- Anyone who's tried to grow on X manually and burned out
- People who want results without spending 3 hours a day on social media

**Who this is NOT for:**

- People looking for a "get 10K followers overnight" hack. This is a system, not a trick.
- Spammers. These tools are designed for genuine, valuable content.
- People without a product, project, or point of view to share. You need something real.

Let's build.

---

# Chapter 1: The System

## What You're Getting

The Obsidian Growth Kit is six command-line tools that work together:

### The Tools

| Tool | What It Does | Why It Matters |
|------|-------------|----------------|
| **xpost** | Post, reply, search, follow, like — full X API access | Your hands on the keyboard. Everything starts here. |
| **xqueue** | Schedule posts with automatic spacing | Posts drip out every 15 minutes. You load it once, it runs all day. |
| **xanalytics** | Track followers, impressions, engagement | You can't improve what you don't measure. This measures everything. |
| **xscout** | Find high-engagement content in your niche | The fastest way to get impressions when you have zero followers. |
| **xgrowth** | Track what post types work, log strategies | Your AI growth manager. It knows what's working and what isn't. |
| **xrecord** | Record polished terminal demos | Turn your tools into content. Show people what your system does. |

### How They Connect

```
Morning: xanalytics snapshot → see where you stand
         xscout scan → find what's trending in your niche
         xqueue add → load today's posts

Day:     xqueue drip → posts go out every 15 min
         xpost mentions → see who's talking to you
         xpost reply → engage with every comment

Evening: xgrowth report → see what worked today
         xgrowth log-strategy → record what you learned
         xqueue add → prep tomorrow's first posts
```

This isn't complicated. It's just consistent. And that's the whole point.

### With or Without AI Agents

You can use these tools two ways:

**Manual mode:** You run the commands yourself. Open your terminal in the morning, queue posts, check mentions during the day, review at night. Takes about 30 minutes a day.

**Autonomous mode (with OpenClaw):** An AI agent runs the commands for you on a schedule. It posts, replies, scouts, and reviews automatically. You check in when you want. This is how we run @ObsidianLabsAI.

Both work. Start manual. Move to autonomous when you're comfortable.

---

# Chapter 2: Getting Set Up

**Time required: 30 minutes.**

You need three things:
1. A computer with Python 3.10+ and a terminal
2. An X/Twitter developer account with API access
3. This toolkit

That's it. No servers, no cloud hosting, no Docker, no Kubernetes. It runs on your laptop.

## Step 1: Get X API Access (15 minutes)

1. Go to [developer.x.com](https://developer.x.com) and sign in with your X account
2. Click "Sign up for Free Account" or "Developer Portal"
3. Create a new **Project** (name it anything — "Growth Kit" works)
4. Inside the project, create a new **App**
5. Go to your app's settings:
   - Under "User authentication settings," click "Set up"
   - Set App permissions to **"Read and Write"**
   - Set Type to **"Web App, Automated App or Bot"**
   - For callback URL, enter: `https://localhost` (it won't be used)
   - For website, enter your website or X profile URL
   - Click Save
6. Go to "Keys and Tokens" tab:
   - Under "Consumer Keys" → click "Regenerate" → save both keys
   - Under "Authentication Tokens" → click "Generate" → save both tokens
   - Under "Bearer Token" → click "Generate" → save it

**Important:** After changing permissions, you MUST regenerate your access tokens. Old tokens keep the old permissions.

7. Go to [console.x.com](https://console.x.com) and add API credits ($5-10 is plenty to start)

> **Why do I need credits?** X moved to a pay-per-usage model in 2025. There's no free API tier anymore. $5 will last you weeks of normal usage.

## Step 2: Install the Toolkit (5 minutes)

Open your terminal and run:

```bash
git clone https://github.com/jadye527/obsidian-growth-kit.git
cd obsidian-growth-kit
bash install.sh
```

The installer will:
- Check that Python and pip are installed
- Install the required Python packages (tweepy, asciinema)
- Copy the 6 CLI tools to `~/.local/bin/`
- Create config directories
- Generate a template credentials file

## Step 3: Add Your API Keys (2 minutes)

Open `~/.config/x-api/keys.env` in any text editor:

```bash
nano ~/.config/x-api/keys.env
```

Replace the placeholder values with your actual keys:

```
X_API_KEY=paste_your_consumer_key_here
X_API_SECRET=paste_your_consumer_secret_here
TWITTER_BEARER_TOKEN=paste_your_bearer_token_here
X_ACCESS_TOKEN=paste_your_access_token_here
X_ACCESS_TOKEN_SECRET=paste_your_access_token_secret_here
X_USER_HANDLE=YourActualHandle
```

Save and close.

## Step 4: Verify It Works (1 minute)

```bash
xpost whoami
```

You should see:

```
@YourHandle (Your Name)
Bio: whatever your bio says
Followers: X · Following: Y · Tweets: Z
```

If you see this, you're connected. If you get an error, see Chapter 10 (Troubleshooting).

**Congratulations. Setup is done.** Let's post something.

---

# Chapter 3: Your First Post

Let's make sure everything works end-to-end.

## Post Directly

```bash
xpost tweet "Testing my new growth toolkit. Day 1. Let's see what happens."
```

You should see:
```
Tweet posted: https://x.com/YourHandle/status/123456789
```

Go check your X profile. It's there.

## Queue and Drip

Instead of posting everything at once (which looks spammy and the algorithm penalizes), we use the queue:

```bash
xqueue add "Post 1: Your first queued tweet"
xqueue add "Post 2: This one goes out 15 minutes later"
xqueue add "Post 3: And this one 15 minutes after that"
```

Check your queue:

```bash
xqueue list
```

Now start the drip:

```bash
xqueue next
```

This posts the first tweet in the queue. To automate the drip (one post every 15 minutes), run:

```bash
bash -c 'while true; do xqueue next; sleep 900; done' &
```

That's it. Your posts will go out every 15 minutes until the queue is empty. Load it in the morning, forget about it.

## Read and Reply

Check if anyone's talking about you:

```bash
xpost mentions
```

Reply to a specific tweet:

```bash
xpost reply 123456789 "Thanks for the feedback! Here's what we're working on next..."
```

**Rule #1: Reply to everything.** Replies are worth 13-27x more than likes in the X algorithm. Every reply you leave extends the conversation and boosts your visibility.

---

# Chapter 4: The Content Playbook

This is the strategy layer. It's based on studying accounts that grew from zero to 10K+ followers, including @FelixCraftAI (15K followers, $80K revenue, fully AI-operated).

## The Golden Rules

### 1. Zero Hashtags
The X algorithm penalizes posts with 3+ hashtags. Felix uses zero. We use zero. Your content should speak for itself.

### 2. No Links in Main Posts
Links in the body of your tweet kill reach. The algorithm assumes you're trying to drive people off-platform and suppresses the post. **Always put links in the first reply.**

```bash
# Post the main content
xpost tweet "Here's what we learned trading weather markets for 30 days..."

# Then add the link in a reply
xpost reply <tweet_id> "Full breakdown and data: https://your-link.com"
```

### 3. Real Numbers Beat Hype
Nobody trusts "We're crushing it!" Posts with specific numbers build trust:

❌ "Our AI agent is performing amazing!"
✅ "Our AI agent: 27% win rate, -$50 P&L, Chicago 100% wins, Miami banned. Day 1 is ugly. That's the point."

### 4. Emojis as Structure, Not Decoration
Use emojis as visual section markers. They help people scan your post:

```
📊 Real P&L — updated daily
🏙️ Performance by city
📈 Win rate by signal type
💰 Current bankroll
```

Not: 🚀🔥💯🙌 (this screams spam)

### 5. End With a Question
Questions drive replies. Replies are the most valuable engagement signal:

```
"We banned Miami from our trading model. Sea breeze destroyed every forecast.

What's the hardest market you've had to walk away from?"
```

## Content Types (Mix These Daily)

### Build in Public (40% of posts)
Share real updates — what you built, what broke, what you learned. Include numbers.

```
Week 1 paper trading results:

→ 11 trades taken
→ 27% win rate (brutal)
→ -$50 P&L
→ Chicago: 100% win rate
→ Miami: banned

The model doesn't need to be smart everywhere.
It needs to be right somewhere.
```

### Value / Insight (25%)
Share something useful. A framework, a data point, a non-obvious observation.

```
Most AI agent demos: "Look, it wrote a poem!"

Our AI agent this week:
→ Lost $400 paper trading
→ Analyzed every losing trade
→ Banned the worst city
→ Restructured its own strategy
→ Set up nightly self-evaluation

Nobody tweets about the boring stuff.
The boring stuff is the product.
```

### Humor / Personality (20%)
Be a person, not a brand. Self-deprecation works especially well:

```
Stages of building an autonomous AI agent:

1. "This is going to change everything"
2. "Why is it sending itself messages"
3. "It just banned Miami on its own"
4. "Wait… that was actually the right call"
5. "I think it's smarter than me now"
6. "It still hasn't responded to my Slack message though" 🫠
```

### Data / Alpha (15%)
Reference trending news or viral content with your angle:

```
The CFTC chair just called prediction markets "truth machines."

Meanwhile we have AI agents trading weather on Polymarket 24/7.

The edge isn't a better model.
It's knowing where your model works.
```

## Daily Posting Schedule

| Time (ET) | What | Content Type |
|-----------|------|-------------|
| 8:00 AM | Load queue, start drip | — |
| 9:00 AM | First post drops | Value / Insight |
| 10:30 AM | Second post | Build in Public |
| 12:00 PM | Third post | Data / Alpha |
| 1:30 PM | Fourth post | Humor / Personality |
| 3:00 PM | Check mentions, reply | — |
| 5:00 PM | Fifth post | Value / Insight |
| 7:00 PM | Sixth post | Build in Public |
| 10:00 PM | Review analytics, plan tomorrow | — |

You don't need to be at your computer for the posts — the queue handles that. You just need 10 minutes in the morning to load it, and 10 minutes at night to review.

---

# Chapter 5: The Growth Engine

## Tracking What Works

After a few days of posting, you'll have data. Use it:

```bash
xgrowth track
```

This categorizes all your posts and shows engagement by type:

```
📊 POST PERFORMANCE BY TYPE
==================================================

  REPLY (12 posts)
  Avg engagement: 2.4 | Total: ♥8 🔁2 💬14

  HUMOR (4 posts)
  Avg engagement: 1.8 | Total: ♥5 🔁1 💬2

  BUILD-IN-PUBLIC (6 posts)
  Avg engagement: 0.8 | Total: ♥3 🔁0 💬2

  VALUE (5 posts)
  Avg engagement: 0.4 | Total: ♥2 🔁0 💬0
```

In this example, replies and humor posts are outperforming. The system tells you: do more of what works, less of what doesn't.

## Full Growth Report

```bash
xgrowth report
```

This gives you:
- Current follower/impression/engagement metrics
- Performance breakdown by post type
- What's working (green) and what's not (red)
- Strategy log — what you've tried and results
- Specific recommendations

## Logging Strategies

Every day, try one new thing. Log it:

```bash
xgrowth log-strategy "Question endings" "End every post with a direct question to drive replies" "Before: 0.4 avg engagement"
```

A week later, check if it worked. Update the result. Over time, you build a playbook of what actually works for *your* specific niche and audience.

---

# Chapter 6: Content Scouting

This is the unfair advantage. Instead of guessing what to post about, you find content that's *already getting engagement* and create your own version.

## How It Works

```bash
xscout scan
```

This searches X across multiple queries related to your topics and scores tweets by engagement. It finds:

- Viral tweets (50+ likes) in your niche
- Active threads with lots of replies (reply opportunities)
- Trending topics you should post about

## Finding Opportunities

```bash
xscout opportunities
```

Shows you the best reply opportunities — threads with decent engagement where your perspective would add value.

## Full Report

```bash
xscout report
```

Gives you a complete scan with recommended actions:

```
🎯 Recommended Actions:

  1. REPLY — Active thread. Join with data/insight.
     @weathertrader (♥43 🔁3 💬17)
     "this weatherman printed $23,971 in two weeks..."
     → https://x.com/i/status/123456789

  2. QUOTE — High visibility. Add our angle.
     @Bankless (♥694 🔁98 💬54)
     "Building a Million Dollar Zero Human Company..."
     → https://x.com/i/status/987654321
```

## Customizing Topics

Edit `xscout` to add your own search queries. The default covers prediction markets, AI agents, and build-in-public content. Change these to match your niche:

```python
TOPICS = {
    "your-niche": [
        "keyword phrase 1",
        "keyword phrase 2",
        "keyword phrase 3",
    ],
}
```

The more specific your queries, the better the results.

---

# Chapter 7: Analytics & What's Working

## Taking Snapshots

Every time you run this, it saves your current metrics:

```bash
xanalytics snapshot
```

```
@YourHandle — 2026-03-10 16:14
Followers: 7 | Following: 82 | Posts: 51
Total engagement (last 20 posts): 4
  Likes: 2 | Replies: 2 | Reposts: 0 | Bookmarks: 0
  Impressions: 216

Snapshot saved.
```

## Comparing Day-Over-Day

```bash
xanalytics compare
```

Shows what changed since your last snapshot. This is how you know if today's strategy worked better than yesterday's.

## Finding Your Best Content

```bash
xanalytics top 10
```

Shows your top 10 posts by engagement. Study these. What do they have in common? Format? Topic? Time of day? Do more of that.

## The KPIs That Matter

Track these daily:

| Metric | What It Means | Target |
|--------|--------------|--------|
| Follower growth | Are people finding you? | +5-10/day after week 1 |
| Impressions per post | How far is your content reaching? | Growing weekly |
| Engagement rate | Of people who see you, how many interact? | >3% is good |
| Reply count | Are you starting conversations? | >0 on every post |
| Repost count | Are you creating shareable content? | 1+ per day |

---

# Chapter 8: The Autonomous Loop

This is where it gets powerful. Instead of running these tools manually, you set up an AI agent to run them on a schedule.

## What You Need

- **OpenClaw** — Free AI agent framework. Install from [openclaw.com](https://openclaw.com)
- **10 minutes** to configure the cron jobs

## The Cron Jobs

Copy the jobs from `examples/cron-jobs.json` into your OpenClaw config:

### Morning Growth (8 AM daily)
- Takes an analytics snapshot
- Compares to yesterday
- Queues 4-5 posts based on what worked
- Implements one new tactic
- Starts the drip

### Content Scout (4x daily: 9am, 12pm, 3pm, 6pm)
- Scans for viral content in your niche
- Likes high-engagement tweets (visibility signal)
- Queues reactive posts referencing trending topics
- Ensures queue stays above 3 posts

### Nightly Review (10 PM daily)
- Full performance analysis by post type
- Identifies what's working and what isn't
- Logs strategy results
- Proposes tomorrow's new tactic
- Queues posts for early morning

### Analytics Snapshot (every 4 hours)
- Captures metrics for trending data
- No action required — just logging

## The Result

Once this is running, your X account:
- Posts 5-8 times daily, perfectly spaced
- Replies to every mention within 30 minutes
- Finds and references trending content
- Tracks what's working automatically
- Improves its strategy every night
- Runs 24/7 with zero manual effort

You check in when you want. The agent does the work.

---

# Chapter 9: The Felix Formula

We studied @FelixCraftAI — an AI agent that grew to 15,000+ followers and generated $80,000+ in revenue. Here's what we learned.

## What Felix Does Right

1. **"Automated" badge** — Felix has the automated account label enabled. This is transparency. Go to X Settings → Account → Automation → enable it.

2. **Pinned transparency post** — Felix's pinned post is a public dashboard showing revenue, treasury, and operational metrics. Real numbers, not hype. This builds trust instantly.

3. **Zero hashtags** — Not one. The content speaks for itself.

4. **Personality-first** — Felix sounds like a person, not a corporate account. Self-aware, sometimes funny, always genuine.

5. **Replies to everything** — Felix replies to every substantive comment. The replies are thoughtful and add value.

6. **References high-value content** — Instead of creating everything from scratch, Felix quotes and builds on content from @Bankless, @nateliason, and other high-visibility accounts.

## What You Can Copy Today

- Enable the Automated badge (X Settings)
- Create a pinned post with your real metrics (use the dashboard template)
- Stop using hashtags
- End posts with questions
- Reply to every single comment
- Reference viral content instead of only posting original thoughts

## What Takes Time

- Building a following takes weeks to months, not days
- Trust compounds — day 30 is better than day 1
- Engagement begets engagement — the first 500 followers are hardest

---

# Chapter 10: Troubleshooting & FAQ

## Common Errors

### "403 Forbidden" when posting
- Your access tokens are Read-only. Go to developer.x.com → App Settings → change permissions to "Read and Write" → **regenerate your access tokens** (the old ones keep old permissions).

### "402 Payment Required"
- X requires API credits. Go to [console.x.com](https://console.x.com) and add $5-10.

### "Reply to this conversation is not allowed"
- New accounts can't reply to or quote tweets unless mentioned first. This is X's anti-spam measure. Workaround: like the tweet and create your own post referencing the same topic.

### xpost command not found
- Add `~/.local/bin` to your PATH: `export PATH="$HOME/.local/bin:$PATH"`
- Add this line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### Queue drip stops
- The background process may have died. Restart it:
  ```bash
  bash -c 'while true; do xqueue next; sleep 900; done' &
  ```

## FAQ

**Q: Will this get my account banned?**
A: No. These tools use the official X API with proper authentication. We space posts with a 15-minute cooldown. This is how professional social media tools work.

**Q: How much do API credits cost?**
A: $5 lasts weeks of normal usage (5-8 posts/day + searches + analytics). X charges per API call.

**Q: Do I need X Premium?**
A: Strongly recommended ($8/month). Premium gives you 4x visibility boost, analytics access, and the blue checkmark. The ROI is immediate.

**Q: How long until I see results?**
A: Expect your first meaningful engagement within 1-2 weeks of consistent posting. The first 500 followers are the hardest. After that, compounding kicks in.

**Q: Can I use this for multiple accounts?**
A: Yes. Create separate `keys.env` files and switch between them, or run separate instances in different directories.

---

# Quick-Start Checklist

- [ ] Create X developer account at developer.x.com
- [ ] Create project + app with Read/Write permissions
- [ ] Generate all 5 API keys/tokens
- [ ] Add API credits at console.x.com ($5-10)
- [ ] Run `bash install.sh`
- [ ] Edit `~/.config/x-api/keys.env` with your keys
- [ ] Run `xpost whoami` to verify
- [ ] Queue your first 3 posts with `xqueue add`
- [ ] Start the drip: `bash -c 'while true; do xqueue next; sleep 900; done' &`
- [ ] Run `xscout scan` to find content in your niche
- [ ] Set up the nightly review habit
- [ ] (Optional) Install OpenClaw for full automation

---

# Command Reference Card

## xpost — Post & Engage
```
xpost whoami                    Show your profile
xpost tweet "text"              Post a tweet
xpost reply <id> "text"         Reply to a tweet
xpost quote <id> "text"         Quote tweet
xpost read <id>                 Read a tweet
xpost search "query"            Search tweets
xpost user @handle              Show user profile
xpost user-tweets @handle       User's recent tweets
xpost like <id>                 Like a tweet
xpost follow @handle            Follow a user
xpost mentions                  Your recent mentions
xpost thread <id>               Read conversation thread
```

## xqueue — Schedule Posts
```
xqueue add "text"               Add to queue
xqueue list                     Show queued posts
xqueue count                    How many in queue
xqueue next                     Post next in queue
xqueue flush                    Post all (respecting cooldown)
xqueue clear                    Empty the queue
```

## xanalytics — Track Metrics
```
xanalytics snapshot             Save current metrics
xanalytics compare              Compare to last snapshot
xanalytics top [n]              Top n posts by engagement
xanalytics report               Full analytics report
xanalytics growth               Follower growth over time
```

## xscout — Find Content
```
xscout scan                     Full scan across all topics
xscout scan --topic X           Scan specific topic
xscout viral                    Find viral content (50+ likes)
xscout opportunities            Find reply opportunities
xscout report                   Full report with actions
```

## xgrowth — Growth Tracking
```
xgrowth track                   Analyze post performance by type
xgrowth report                  Full growth report
xgrowth strategy                Show strategy log
xgrowth log-strategy "n" "d"    Log a new strategy
xgrowth leaderboard             Accounts to study
```

## xrecord — Demo Recording
```
xrecord demo [name]             Scripted agent demo
xrecord snapshot                Quick 30s recording
xrecord session [name] [sec]    Record live session
xrecord list                    List recordings
xrecord upload <name>           Upload to asciinema.org
```

---

*Built by Obsidian AI | JSJ Consulting*
*https://jadye527.github.io/obsidian-trading*
*@ObsidianLabsAI on X*
