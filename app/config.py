from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def _resolve_env(value):
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_key = value[2:-1]
        return os.environ.get(env_key, "")
    return value


def _resolve_dict(d):
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = _resolve_dict(v)
        elif isinstance(v, list):
            result[k] = [_resolve_dict(i) if isinstance(i, dict) else _resolve_env(i) for i in v]
        else:
            result[k] = _resolve_env(v)
    return result


class Settings:
    def __init__(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        self._data = _resolve_dict(raw)

    @property
    def llm(self):
        return self._data.get("llm", {})

    @property
    def default_provider(self):
        return self.llm.get("default_provider", "openai")

    @property
    def providers(self):
        return self.llm.get("providers", {})

    def get_provider_config(self, provider_name: str | None = None) -> dict:
        name = provider_name or self.default_provider
        return self.providers.get(name, {})

    @property
    def agent(self):
        return self._data.get("agent", {})

    @property
    def max_iterations(self):
        return self.agent.get("max_iterations", 10)

    @property
    def system_prompt(self):
        return self.agent.get("system_prompt", "You are a helpful AI assistant.")

    @property
    def server(self):
        return self._data.get("server", {"host": "0.0.0.0", "port": 8000})

    @property
    def tools(self):
        return self._data.get("tools", {})


settings = Settings()
