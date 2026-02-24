# Flux-RX Config Module: Global settings
from __future__ import annotations

from typing import Any, Optional


class Config:
    def __init__(self):
        self._risk_free_rate = 0.04
        self._default_theme = "flux"
        self._default_period = "5y"
        self._cache_dir: Optional[str] = None
        self._timeout = 30

    @property
    def risk_free_rate(self) -> float:
        return self._risk_free_rate

    @risk_free_rate.setter
    def risk_free_rate(self, value: float):
        self._risk_free_rate = value

    @property
    def default_theme(self) -> str:
        return self._default_theme

    @default_theme.setter
    def default_theme(self, value: str):
        self._default_theme = value

    @property
    def default_period(self) -> str:
        return self._default_period

    @default_period.setter
    def default_period(self, value: str):
        self._default_period = value

    @property
    def cache_dir(self) -> Optional[str]:
        return self._cache_dir

    @cache_dir.setter
    def cache_dir(self, value: str):
        self._cache_dir = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value


_GLOBAL_CONFIG = Config()


def get_config() -> Config:
    return _GLOBAL_CONFIG


def set_config(**kwargs):
    config = get_config()
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            raise AttributeError(f"Config has no attribute '{key}'")
