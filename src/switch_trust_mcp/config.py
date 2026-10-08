"""Configuration and fail-closed host validation for the AI-SPM MCP server.

The MCP server is a thin, read-only client of the Switch Trust backend. It needs
only two things from the environment: an API key (``sk_...``) and the Switch
Trust instance base URL. The tenant/workspace are auto-discovered at runtime
from the key (see ``client.py``), so they are deliberately NOT configuration.

Never log the API key.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

# The Switch Trust instance hosts a credential may be sent to. Each entry is
# matched exactly or as a parent suffix (a ``.<entry>`` subdomain).
ALLOWED_SWITCH_TRUST_HOSTS = ("switchagents.ai",)

# Env var names for the API key and the instance base URL. Tuples leave room for
# future aliases, but there is a single supported name for each today.
API_KEY_ENV_VARS = ("SWITCH_TRUST_API_KEY",)
INSTANCE_ENV_VARS = ("SWITCH_TRUST_INSTANCE",)

# Schemes the localhost carve-out below will accept.
_LOCALHOST_SCHEMES = ("http", "https")

# The single host the cleartext-http carve-out accepts. Matched exactly: no
# ``*.localhost`` (those go through DNS and a resolver could answer with a
# routable address) and no IP literals — one spelling keeps the carve-out easy
# to reason about. Point a local backend at ``http://localhost:PORT``.
_LOCALHOST = "localhost"


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    """Resolved, validated configuration. ``api_key`` must never be logged."""

    instance: str
    api_key: str


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def validate_switch_trust_instance(instance: str | None) -> str | None:
    """Validate that ``instance`` is an https:// URL on an allowlisted host.

    Returns the normalized URL (no trailing slash) when valid, else ``None``.
    Fails closed: a missing/empty value, a parse error, a non-https scheme, or a
    host outside ``ALLOWED_SWITCH_TRUST_HOSTS`` all yield ``None`` so credentials
    are never attached to an untrusted host.
    """
    if not instance:
        return None
    try:
        parsed = urlparse(instance)
    except ValueError:
        return None
    host = parsed.hostname
    if host is None:
        return None
    host = host.lower()
    # Local development against a backend on this machine.
    if parsed.scheme in _LOCALHOST_SCHEMES and host == _LOCALHOST:
        return instance.rstrip("/")
    # Require an explicit https scheme (rejects http:// cleartext and
    # scheme-less values that urlparse would treat as a bare path).
    if parsed.scheme != "https":
        return None
    # Exact host or a subdomain of an allowed domain. The leading dot in the
    # suffix check prevents look-alikes such as "evilswitchagents.ai".
    if not any(
        host == allowed or host.endswith(f".{allowed}")
        for allowed in ALLOWED_SWITCH_TRUST_HOSTS
    ):
        return None
    return instance.rstrip("/")


def load_config() -> Config:
    """Load and validate configuration from the environment.

    Raises ``ConfigError`` with an actionable message if the API key is missing
    or the instance URL is absent/invalid.
    """
    api_key = _first_env(API_KEY_ENV_VARS)
    if not api_key:
        raise ConfigError(
            "No API key set. Provide one of: " + ", ".join(API_KEY_ENV_VARS)
        )

    raw_instance = _first_env(INSTANCE_ENV_VARS)
    instance = validate_switch_trust_instance(raw_instance)
    if instance is None:
        raise ConfigError(
            "No valid instance URL set. Provide one of "
            f"{', '.join(INSTANCE_ENV_VARS)} as an https:// URL on one of: "
            + ", ".join(ALLOWED_SWITCH_TRUST_HOSTS)
            + " — or http://localhost:PORT for local development."
        )

    return Config(instance=instance, api_key=api_key)
