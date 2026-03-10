import importlib.machinery
import importlib.util
import os
import pathlib

import pytest


@pytest.fixture(scope="session")
def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def load_tool_module(repo_root):
    def _load(tool_name: str):
        tool_path = repo_root / "tools" / tool_name
        loader = importlib.machinery.SourceFileLoader(
            f"{tool_name}_module", str(tool_path)
        )
        spec = importlib.util.spec_from_loader(f"{tool_name}_module", loader)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    return _load


@pytest.fixture
def make_queue_tweet():
    def _make(text: str = "queued tweet", added: int = 0, **overrides):
        tweet = {"text": text, "added": added}
        tweet.update(overrides)
        return tweet

    return _make


@pytest.fixture
def make_queue():
    def _make(*tweets, last_posted: int = 0):
        return {"tweets": list(tweets), "last_posted": last_posted}

    return _make


@pytest.fixture
def make_scout_tweet():
    def _make(
        author: str = "@author",
        date: str = "2026-03-10",
        text: str = "Useful post",
        likes: int = 0,
        retweets: int = 0,
        replies: int = 0,
        tweet_id: str = "tweet-1",
        engagement: int = 0,
        **overrides,
    ):
        tweet = {
            "author": author,
            "date": date,
            "text": text,
            "likes": likes,
            "retweets": retweets,
            "replies": replies,
            "id": tweet_id,
            "engagement": engagement,
        }
        tweet.update(overrides)
        return tweet

    return _make


@pytest.fixture
def install_env(tmp_path):
    fake_home = tmp_path / "fake-home"
    fake_home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pip_log = tmp_path / "pip.log"

    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    return {
        "bin_dir": bin_dir,
        "env": env,
        "fake_home": fake_home,
        "pip_log": pip_log,
    }
