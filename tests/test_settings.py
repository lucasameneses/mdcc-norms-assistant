import pytest

from assistant import settings as settings_module
from assistant.settings import load_env_file, load_settings, require_api_key


@pytest.fixture(autouse=True)
def no_env_file(monkeypatch, tmp_path):
    monkeypatch.setattr(settings_module, "ENV_FILE", tmp_path / "missing.env")
    monkeypatch.setattr(settings_module.load_env_file, "__defaults__", (tmp_path / "missing.env",))


def test_env_file_fills_only_unset_variables(monkeypatch, tmp_path):
    env = tmp_path / ".env"
    env.write_text("# comment\nEMBED_MODEL=from-file\nCOLLECTION=from-file\n")
    monkeypatch.delenv("EMBED_MODEL", raising=False)
    monkeypatch.setenv("COLLECTION", "from-shell")
    load_env_file(env)
    assert load_settings().embed_model == "from-file"
    assert load_settings().collection == "from-shell"


def test_defaults_point_to_the_local_lab(monkeypatch):
    for name in ("DATABASE_URL", "COLLECTION", "EMBED_MODEL", "CHAT_MODELS", "OLLAMA_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    settings = load_settings()
    assert "localhost" in settings.database_url
    assert settings.embed_model == "bge-m3"
    assert settings.chat_models == ("gpt-oss:20b", "gpt-oss:120b")


def test_chat_models_are_read_as_a_list(monkeypatch):
    monkeypatch.setenv("CHAT_MODELS", "a, b ,c")
    assert load_settings().chat_models == ("a", "b", "c")


def test_missing_key_stops_with_a_clear_message(monkeypatch):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    with pytest.raises(SystemExit, match="OLLAMA_API_KEY"):
        require_api_key(load_settings())
