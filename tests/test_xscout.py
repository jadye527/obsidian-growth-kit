import importlib.machinery
import importlib.util
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
XSCOUT_PATH = ROOT / "tools" / "xscout"


def load_xscout_module():
    loader = importlib.machinery.SourceFileLoader("xscout_module", str(XSCOUT_PATH))
    spec = importlib.util.spec_from_loader("xscout_module", loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_parse_tweets_extracts_text_metrics_and_weighted_score():
    module = load_xscout_module()
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


def test_parse_tweets_ignores_non_tweet_lines():
    module = load_xscout_module()
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


def test_scan_deduplicates_by_tweet_id_and_sorts_by_engagement(monkeypatch):
    module = load_xscout_module()
    tweets_by_query = {
        "query-a": [
            {
                "author": "@alpha",
                "date": "2026-03-10",
                "text": "Higher scoring duplicate",
                "likes": 20,
                "retweets": 5,
                "replies": 1,
                "id": "dup-1",
                "engagement": 40,
            },
            {
                "author": "@beta",
                "date": "2026-03-10",
                "text": "Top unique tweet",
                "likes": 30,
                "retweets": 10,
                "replies": 2,
                "id": "unique-1",
                "engagement": 70,
            },
        ],
        "query-b": [
            {
                "author": "@gamma",
                "date": "2026-03-10",
                "text": "Lower scoring duplicate that should be dropped",
                "likes": 5,
                "retweets": 0,
                "replies": 0,
                "id": "dup-1",
                "engagement": 5,
            },
            {
                "author": "@delta",
                "date": "2026-03-10",
                "text": "Another unique tweet",
                "likes": 10,
                "retweets": 3,
                "replies": 0,
                "id": "unique-2",
                "engagement": 19,
            },
        ],
    }

    monkeypatch.setattr(module, "TOPICS", {"focus-topic": ["query-a", "query-b"]})
    monkeypatch.setattr(module, "xpost_search", lambda query: tweets_by_query[query])

    results = module.scan("focus-topic")

    assert [tweet["id"] for tweet in results] == ["unique-1", "dup-1", "unique-2"]
    assert all(tweet["topic"] == "focus-topic" for tweet in results)
    assert results[1]["text"] == "Higher scoring duplicate"
