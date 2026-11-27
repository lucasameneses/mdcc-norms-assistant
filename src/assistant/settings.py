"""Configuration read from the environment, with defaults for the local docker compose lab."""

import os
from dataclasses import dataclass
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


@dataclass(frozen=True)
class Settings:
    database_url: str
    collection: str
    embed_url: str
    embed_model: str
    chat_url: str
    api_key: str
    chat_models: tuple[str, ...]
    judge_model: str


def load_env_file(path: Path = ENV_FILE) -> None:
    """Read KEY=value lines from .env without overriding variables already set."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        name, sep, value = line.partition("=")
        if sep and not name.strip().startswith("#"):
            os.environ.setdefault(name.strip(), value.strip())


def load_settings() -> Settings:
    load_env_file()
    return Settings(
        database_url=os.environ.get("DATABASE_URL", "postgresql+psycopg://rag:rag@localhost:5432/rag"),
        collection=os.environ.get("COLLECTION", "mdcc-article"),
        embed_url=os.environ.get("OLLAMA_EMBED_URL", "http://localhost:11434"),
        embed_model=os.environ.get("EMBED_MODEL", "bge-m3"),
        chat_url=os.environ.get("OLLAMA_CHAT_URL", "https://ollama.com"),
        api_key=os.environ.get("OLLAMA_API_KEY", ""),
        chat_models=tuple(m.strip() for m in os.environ.get("CHAT_MODELS", "gpt-oss:20b,gpt-oss:120b").split(",") if m.strip()),
        judge_model=os.environ.get("JUDGE_MODEL", "glm-5.3"),
    )


def require_api_key(settings: Settings) -> str:
    if not settings.api_key:
        raise SystemExit("OLLAMA_API_KEY is empty: copy .env.example to .env and fill in the key.")
    return settings.api_key
