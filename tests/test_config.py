import pytest

from shop_assistant import config


def test_constants_match_srs():
    assert config.STALE_DAYS == 60          # FR-16
    assert config.MAX_RESULTS == 5          # FR-18
    assert config.FETCH_LIMIT == 500        # FR-1
    assert config.HISTORY_TURNS == 10       # FR-17
    assert set(config.CATEGORIES) == {"kiyim", "poyabzal", "aksessuar", "boshqa"}


def test_data_paths_are_gitignored():
    ignored = (config.ROOT / ".gitignore").read_text()
    assert "data/" in ignored and "session/" in ignored and ".env" in ignored   # NFR-6


def test_secret_missing_raises(monkeypatch):
    monkeypatch.delenv("TG_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="TG_BOT_TOKEN"):
        config.secret("TG_BOT_TOKEN")


def test_secret_unknown_key():
    with pytest.raises(KeyError):
        config.secret("NOT_A_SECRET")


def test_secret_present(monkeypatch):
    monkeypatch.setenv("TG_BOT_TOKEN", "123:abc")
    assert config.secret("TG_BOT_TOKEN") == "123:abc"


def test_ollama_defaults_point_anthropic_sdk_at_ollama():
    assert config.MODEL == "gemma4:31b" and config.EMBED_MODEL == "bge-m3"
    assert config.OLLAMA_URL.startswith("http")
    import os
    assert os.environ["ANTHROPIC_BASE_URL"] == config.OLLAMA_URL
