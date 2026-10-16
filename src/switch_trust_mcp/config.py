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
from urllib.parse import urlsplit, urlunsplit

# The Switch Trust instance hosts a credential may be sent to. Each entry is
# matched exactly or as a parent suffix (a ``.<entry>`` subdomain).
ALLOWED_SWITCH_TRUST_HOSTS = ("switchagents.ai",)

# Env var names for the API key and the instance base URL. Tuples leave room for
# future aliases, but there is a single supported name for each today.
API_KEY_ENV_VARS = ("SWITCH_TRUST_API_KEY",)
INSTANCE_ENV_VARS = ("SWITCH_TRUST_INSTANCE",)

# Schemes the localhost carve-out below will accept.
_LOCALHOST_SCHEMES = ("http", "https")

# Leading labels that name an edge service rather than an instance; see
# derive_api_url.
_EDGE_SUBDOMAIN_LABELS = ("app", "api", "ingestion")

# The single host the cleartext-http carve-out accepts. Matched exactly: no
# ``*.localhost`` (those go through DNS and a resolver could answer with a
# routable address) and no IP literals — one spelling keeps the carve-out easy
# to reason about. Point a local backend at ``http://localhost:PORT``.
_LOCALHOST = "localhost"

# Characters a (lowercased) hostname may contain. Anything else — percent
# escapes, IDNA, whitespace — is rejected rather than interpreted, so no two
# parsers can disagree about which host a validated URL names.
_HOSTNAME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789.-")


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
    """Validate that ``instance`` is an https:// origin on an allowlisted host.

    Returns the canonical origin ``scheme://host[:port]`` when valid, else
    ``None``. Fails closed: a missing/empty value, a parse error, a non-https
    scheme, or a host outside ``ALLOWED_SWITCH_TRUST_HOSTS`` all yield ``None``
    so credentials are never attached to an untrusted host. So do userinfo, an
    invalid port, a path other than ``/``, a query, or a fragment: the value is
    a base URL, and anything beyond an origin is a mistake or a trick.

    The result is rebuilt from the parsed parts rather than echoing the input,
    so the HTTP client parses exactly the URL validated here.
    """
    if not instance:
        return None
    try:
        parsed = urlsplit(instance)
        port = parsed.port
    except ValueError:
        return None
    host = parsed.hostname
    if not host or not set(host) <= _HOSTNAME_CHARS:
        return None
    if "@" in parsed.netloc or parsed.path not in ("", "/"):
        return None
    if parsed.query or parsed.fragment:
        return None
    netloc = host if port is None else f"{host}:{port}"
    canonical = urlunsplit((parsed.scheme, netloc, "", "", ""))
    # Local development against a backend on this machine.
    if parsed.scheme in _LOCALHOST_SCHEMES and host == _LOCALHOST:
        return canonical
    # Require an explicit https scheme (rejects http:// cleartext and
    # scheme-less values that urlsplit would treat as a bare path).
    if parsed.scheme != "https":
        return None
    # Exact host or a subdomain of an allowed domain. The leading dot in the
    # suffix check prevents look-alikes such as "evilswitchagents.ai".
    if not any(
        host == allowed or host.endswith(f".{allowed}")
        for allowed in ALLOWED_SWITCH_TRUST_HOSTS
    ):
        return None
    return canonical


def derive_api_url(instance: str) -> str:
    """Derive the ``api.`` URL that serves the REST API for a validated instance.

    ``instance`` names the web app (``https://app.switchagents.ai``); the API is
    on ``api.`` of the same deployment. A leading edge label is replaced and any
    other first label is kept, so ``app.switchagents.ai`` and
    ``switchagents.ai`` both give ``api.switchagents.ai``, and an ``api.`` URL is
    returned unchanged.
    ``localhost`` is returned unchanged: one origin serves everything.
    """
    parsed = urlsplit(instance)
    host = parsed.hostname or ""
    if host == _LOCALHOST:
        return instance
    head, _, rest = host.partition(".")
    # `rest` must survive the strip: on api.switchagents.ai the label is all
    # there is in front of the apex.
    base = rest if head in _EDGE_SUBDOMAIN_LABELS and rest else host
    netloc = f"api.{base}" if parsed.port is None else f"api.{base}:{parsed.port}"
    return urlunsplit(parsed._replace(netloc=netloc))


def load_config() -> Config:
    """Load and validate configuration from the environment.

    Raises ``ConfigError`` with an actionable message if the API key is missing
    or the instance URL is absent/invalid. Used as-is by the hosted HTTP
    transport too: that mode serves one shared Switch Trust credential to every
    caller (see its own, separate access-token gate), the same credential/
    instance pair stdio mode has always read.
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


