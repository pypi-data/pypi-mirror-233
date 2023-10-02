from __future__ import annotations
from toolforge_weld.config import load_config, Config
from functools import lru_cache


@lru_cache(maxsize=None)
def get_loaded_config() -> Config:
    return load_config(client_name="toolforge")
