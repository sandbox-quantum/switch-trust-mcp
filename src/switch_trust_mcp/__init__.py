"""switch-trust-mcp: the Switch Trust platform MCP server for coding agents.

v1 exposes read-only AI-SPM issues, inventory, and remediation guidance from a
Switch Trust instance. The package is named for the platform (not AI-SPM
specifically) so it can grow to cover additional Switch Trust product domains
over time.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("switch-trust-mcp")
except PackageNotFoundError:  # not installed (e.g. running from a source checkout)
    __version__ = "0.0.0-dev"

__all__ = ["__version__"]
