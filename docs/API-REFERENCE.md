# API Reference

This document lists every CLI command exposed by the tools in `obsidian-growth-kit`.

## Common Pattern

Each tool supports `--help` and `-h`.

## `xpost`

X/Twitter CLI for posting, reading, searching, and managing account actions.

Usage:

```bash
xpost <command> [args] [--json]
xpost --text "text" [--media /path/to/file]
xpost --help
```

Commands:

| Command | Description |
| --- | --- |
| `xpost whoami` | Show the authenticated user. |
| `xpost tweet "text"` | Post a tweet. |
| `xpost --text "text" [--media /path/to/file]` | Post a tweet directly with optional media. |
| `xpost reply <tweet_id> "text"` | Reply to a tweet. |
| `xpost quote <tweet_id> "text"` | Quote-tweet a post. |
| `xpost read <tweet_id>` | Read a single tweet. |
| `xpost user <@handle>` | Show a user profile. |
| `xpost user-tweets <@handle>` | Show a user's recent tweets. |
| `xpost search "query"` | Search recent tweets. |
| `xpost like <tweet_id>` | Like a tweet. |
| `xpost unlike <tweet_id>` | Unlike a tweet. |
| `xpost retweet <tweet_id>` | Retweet a tweet. |
| `xpost unretweet <tweet_id>` | Undo a retweet. |
| `xpost delete <tweet_id>` | Delete one of your tweets. |
| `xpost mentions` | Show your recent mentions. |
| `xpost thread <tweet_id>` | Read a conversation thread. |
| `xpost follow <@handle>` | Follow a user. |
| `xpost unfollow <@handle>` | Unfollow a user. |
| `xpost followers <@handle>` | List followers for a handle. If omitted, uses `X_USER_HANDLE`. |
| `xpost following <@handle>` | List accounts a handle follows. If omitted, uses `X_USER_HANDLE`. |

Options and behavior:

- `--json` is supported by `whoami` and `user`.
- `--media` uploads one file before posting and can be used with `--text`.
- Tweet IDs must be numeric.
- Credentials are loaded from `X_KEYS_FILE` or `~/.config/x-api/keys.env`.

## `xqueue`

Tweet queue and drip scheduler.

Usage:

```bash
xqueue <command> [args]
xqueue --help
```

Commands:

| Command | Description |
| --- | --- |
| `xqueue add "tweet text"` | Add a tweet to the queue. |
| `xqueue list` | Show queued tweets. |
| `xqueue flush` | Post all queued tweets with cooldown delays. |
| `xqueue next` | Post the next queued tweet if cooldown has passed. |
| `xqueue clear` | Clear the queue. |
| `xqueue count` | Show queue size. |

Options and behavior:

- Queue storage uses `X_QUEUE_FILE` or `~/.config/x-api/queue.json`.
- Posting uses a 15-minute minimum interval between tweets.

## `xanalytics`

Snapshot and report tool for followers and post engagement.

Usage:

```bash
xanalytics <command> [args]
xanalytics --help
```

Commands:

| Command | Description |
| --- | --- |
| `xanalytics snapshot` | Fetch current metrics for recent posts and save a snapshot. |
| `xanalytics top [n]` | Show the top `n` posts by engagement. Default is `5`. |
| `xanalytics report` | Show the latest daily engagement report. |
| `xanalytics growth` | Show follower growth across saved snapshots. |
| `xanalytics compare` | Compare the two latest snapshots. |

Options and behavior:

- Keys come from `X_KEYS_FILE` or `~/.config/x-api/keys.env`.
- Analytics data is stored in `X_ANALYTICS_FILE` or `~/.config/x-api/analytics.json`.

## `xscout`

Content discovery tool for viral posts and reply opportunities.

Usage:

```bash
xscout <command> [args]
xscout --help
```

Commands:

| Command | Description |
| --- | --- |
| `xscout scan` | Run a full scan across all topics. |
| `xscout scan --topic <topic>` | Scan a specific topic only. |
| `xscout viral` | Show viral content in the tracked niche. |
| `xscout opportunities` | Show active threads worth replying to. |
| `xscout report` | Generate a formatted scout report with suggested actions. |

Supported topics:

- `ai-agents`
- `build-in-public`
- `prediction-markets`
- `weather-trading`

Options and behavior:

- Results are saved to `~/.config/x-api/scout-results.json`.
- `viral` uses a minimum of `50` likes.
- `opportunities` uses a minimum of `10` likes and at least `1` reply.

## `xgrowth`

Growth analysis and strategy logging tool.

Usage:

```bash
xgrowth <command> [args]
xgrowth --help
```

Commands:

| Command | Description |
| --- | --- |
| `xgrowth track` | Analyze recent posts and categorize performance. |
| `xgrowth report` | Generate a full growth report with recommendations. |
| `xgrowth strategy` | Show the current strategy log and history. |
| `xgrowth log-strategy "name" "description" [metrics]` | Log a new strategy entry. |
| `xgrowth new-strategy` | Show suggested strategy ideas for today. |
| `xgrowth leaderboard` | Show accounts to study and emulate. |

Options and behavior:

- Growth snapshots are stored in `~/.config/x-api/growth-tracker.json`.
- Strategy entries are stored in `~/.config/x-api/strategy-log.json`.

## `xrecord`

Terminal recording helper for demos and shareable artifacts.

Usage:

```bash
xrecord <command> [args]
xrecord --help
```

Commands:

| Command | Description |
| --- | --- |
| `xrecord demo [name]` | Record a scripted demo of the toolchain. |
| `xrecord snapshot` | Record a short status snapshot. |
| `xrecord session [name] [sec]` | Record a live session. |
| `xrecord list` | List saved recordings. |
| `xrecord upload <name>` | Upload a recording to `asciinema.org`. |
| `xrecord svg <name>` | Convert a cast file to SVG with `svg-term`. |

Options and behavior:

- Recordings are stored in `~/.config/x-api/recordings`.
- `session` requires `sec` to be a positive integer when provided.
- `svg` requires `svg-term` to be installed.

## `xmiddleware`

Next.js middleware probe for tunnel host and auth cookie behavior.

Usage:

```bash
xmiddleware probe --url <url> [--host <host>] [--cookie <cookie>] [--timeout <sec>]
xmiddleware --help
```

Commands:

| Command | Description |
| --- | --- |
| `xmiddleware probe --url <url>` | Probe a URL and report whether the response suggests host blocking or cookie rejection. |
| `xmiddleware probe --url <url> --host <host>` | Override the `Host` header to simulate a tunneled hostname against a local server. |
| `xmiddleware probe --url <url> --cookie <cookie>` | Send a raw `Cookie` header to check whether auth survives middleware. |

Options and behavior:

- Redirects are not followed so middleware redirects stay visible.
- The report includes `Location`, `Set-Cookie`, and any `x-middleware-*` headers returned by Next.js.
- Host blocking is inferred from 4xx responses plus host-related error markers in the body.
