def test_parse_tweets_extracts_text_metrics_and_weighted_score(load_tool_module):
    module = load_tool_module("xscout")
    output = """
@alice · 2026-03-09
First line of the post
Second line of the post
♥ 12  🔁 3  💬 2  id:111
---
@bob · 2026-03-08
Single line post
---
""".strip()

    tweets = module.parse_tweets(output)

    assert tweets == [
        {
            "author": "@alice",
            "date": "2026-03-09",
            "text": "First line of the post\nSecond line of the post",
            "likes": 12,
            "retweets": 3,
            "replies": 2,
            "id": "111",
            "engagement": 31,
        },
        {
            "author": "@bob",
            "date": "2026-03-08",
            "text": "Single line post",
            "likes": 0,
            "retweets": 0,
            "replies": 0,
            "id": "",
            "engagement": 0,
        },
    ]


def test_parse_tweets_ignores_non_tweet_lines(load_tool_module):
    module = load_tool_module("xscout")
    output = """
Search returned 2 results
@carol · 2025-12-31
Useful thread
♥ 50  🔁 4  💬 1  id:222
---
Footer text
""".strip()

    tweets = module.parse_tweets(output)

    assert len(tweets) == 1
    assert tweets[0]["author"] == "@carol"
    assert tweets[0]["engagement"] == 67


def test_scan_deduplicates_by_tweet_id_and_sorts_by_engagement(
    monkeypatch, load_tool_module, make_scout_tweet
):
    module = load_tool_module("xscout")
    tweets_by_query = {
        "query-a": [
            make_scout_tweet(
                author="@alpha",
                text="Higher scoring duplicate",
                likes=20,
                retweets=5,
                replies=1,
                tweet_id="dup-1",
                engagement=40,
            ),
            make_scout_tweet(
                author="@beta",
                text="Top unique tweet",
                likes=30,
                retweets=10,
                replies=2,
                tweet_id="unique-1",
                engagement=70,
            ),
        ],
        "query-b": [
            make_scout_tweet(
                author="@gamma",
                text="Lower scoring duplicate that should be dropped",
                likes=5,
                tweet_id="dup-1",
                engagement=5,
            ),
            make_scout_tweet(
                author="@delta",
                text="Another unique tweet",
                likes=10,
                retweets=3,
                tweet_id="unique-2",
                engagement=19,
            ),
        ],
    }

    monkeypatch.setattr(module, "TOPICS", {"focus-topic": ["query-a", "query-b"]})
    monkeypatch.setattr(module, "xpost_search", lambda query: tweets_by_query[query])

    results = module.scan("focus-topic")

    assert [tweet["id"] for tweet in results] == ["unique-1", "dup-1", "unique-2"]
    assert all(tweet["topic"] == "focus-topic" for tweet in results)
    assert results[1]["text"] == "Higher scoring duplicate"
