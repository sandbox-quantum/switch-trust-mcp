"""Loader for rule-level remediation guidance.

The rule-keyed remediation markdown has no backend API — it is served to the web
UI as static assets by the instance's web server at ``/assets/docs-remediations/``.
This loader fetches those same assets at runtime over HTTP (via the shared
``SwitchTrustClient``) and assembles them, mirroring the UI.

Layout under ``/assets/docs-remediations/``:
  - ``rule-name-to-remediation-folder-map.json`` maps a human-readable
    ``rule_name`` -> a folder name (or ``""`` when a rule has no docs).
  - each ``<folder>/`` holds up to six markdown fragments.

For offline development and tests, set ``SWITCH_TRUST_REMEDIATION_DIR`` (or pass
``root``) to a local directory laid out the same way; the loader then reads from
disk and never touches the network.

The ``rule_name`` key matches the ``rule_name`` field returned by the issues API.

``get_markdown`` returns those fetched fragments verbatim — the same document the
UI renders for humans. ``get_agent_markdown`` additionally wraps them in
``remediation_procedure.md``, the agent-facing instructions for choosing and
applying a remediation. That procedure is rule-independent, so it is bundled here
(one place to edit, versioned with the tool contract) rather than baked into every
generated per-rule fragment.
"""

from __future__ import annotations

import functools
import importlib.resources
import json
import os
import pathlib
from typing import Any

from switch_trust_mcp.client import SwitchTrustClient, is_safe_path_segment

# Ordered (fragment-file stem -> display heading). Order controls the assembled
# markdown; missing/empty files are skipped.
_FRAGMENTS: tuple[tuple[str, str], ...] = (
    ("short-explanation", "Summary"),
    ("explanation", "Explanation"),
    ("risk", "Risk"),
    ("how-to-resolve-mcp", "How to resolve"),
    ("specifications", "Specifications"),
    ("reference", "References"),
)

_MAP_FILENAME = "rule-name-to-remediation-folder-map.json"
# Env override for tests / offline dev: a directory containing the map file and
# the per-rule folders.
_DIR_ENV_VAR = "SWITCH_TRUST_REMEDIATION_DIR"

# Bundled agent-facing procedure. Package data, so it must stay listed in
# pyproject.toml and the sync allowlist; it wraps the fetched guidance at this
# placeholder.
_PROCEDURE_FILENAME = "remediation_procedure.md"
_PROCEDURE_PLACEHOLDER = "{{remediation_guidance}}"


@functools.lru_cache(maxsize=1)
def _procedure_template() -> str | None:
    """Read the bundled procedure template, or ``None`` if it is missing.

    A missing file means the package was built without its data, not a runtime
    condition — callers degrade to bare guidance rather than failing the tool.
    ``test_procedure_asset_is_bundled`` turns that packaging mistake into a test
    failure instead.
    """
    try:
        return (
            importlib.resources.files("switch_trust_mcp")
            .joinpath(_PROCEDURE_FILENAME)
            .read_text(encoding="utf-8")
        )
    except (OSError, ModuleNotFoundError):
        return None


class RemediationDocs:
    """Reads and assembles rule-level remediation markdown.

    Fetches over HTTP from the instance's static assets by default; reads from a
    local directory when ``root`` / ``SWITCH_TRUST_REMEDIATION_DIR`` is set (offline
    dev, tests). The folder-map and fetched fragments are cached in-memory for the
    session.
    """

    def __init__(
        self,
        client: SwitchTrustClient | None = None,
        *,
        root: str | os.PathLike[str] | None = None,
    ) -> None:
        override = root if root is not None else os.getenv(_DIR_ENV_VAR)
        if override:
            self._root: pathlib.Path | None = pathlib.Path(override)
            self._client: SwitchTrustClient | None = None
        else:
            if client is None:
                raise ValueError(
                    "RemediationDocs requires an HTTP client when no local "
                    f"override ({_DIR_ENV_VAR}) is set"
                )
            self._root = None
            self._client = client
        self._map: dict[str, str] | None = None
        self._fragment_cache: dict[tuple[str, str], str | None] = {}

    # -- folder map --------------------------------------------------------

    def _load_map(self) -> dict[str, str]:
        if self._map is None:
            raw: Any
            if self._root is not None:
                # Best-effort like the HTTP path: a missing or corrupt map must
                # degrade to "no docs", not fail the calling tool.
                try:
                    raw = json.loads(
                        (self._root / _MAP_FILENAME).read_text(encoding="utf-8")
                    )
                except (OSError, ValueError):
                    raw = None
            else:
                assert self._client is not None
                raw = self._client.fetch_remediation_map()
            # Folder names are joined onto a filesystem path (local mode) or a
            # URL (HTTP mode), so reject anything that is not a plain path
            # segment here, at the one place the untrusted map is parsed. A
            # dropped entry simply reads as "this rule has no docs".
            self._map = {
                k: v
                for k, v in (raw if isinstance(raw, dict) else {}).items()
                if isinstance(k, str)
                and isinstance(v, str)
                and (v == "" or is_safe_path_segment(v))
            }
        return self._map

    def folder_for_rule(self, rule_name: str) -> str | None:
        """Return the folder for a rule, ``""`` if mapped-but-no-docs, else ``None``."""
        return self._load_map().get(rule_name)

    # -- fragments ---------------------------------------------------------

    def _fragment(self, folder: str, stem: str) -> str | None:
        key = (folder, stem)
        if key not in self._fragment_cache:
            self._fragment_cache[key] = self._read_fragment(folder, stem)
        return self._fragment_cache[key]

    def _read_fragment(self, folder: str, stem: str) -> str | None:
        if self._root is not None:
            node = self._root / folder / f"{stem}.md"
            try:
                return node.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return None
        assert self._client is not None
        return self._client.fetch_remediation_fragment(folder, stem)

    # -- assembly ----------------------------------------------------------

    def get_markdown(self, rule_name: str) -> str | None:
        """Assemble the remediation markdown for a rule name.

        Returns a combined markdown string, or ``None`` when the rule is unknown,
        explicitly mapped to no docs (``""``), or has no non-empty fragments.
        Callers should fall back to the per-finding ``remediation`` text.
        """
        folder = self._load_map().get(rule_name)
        if not folder:  # None (unknown) or "" (mapped, no docs)
            return None

        sections: list[str] = []
        for stem, heading in _FRAGMENTS:
            content = self._fragment(folder, stem)
            if content and content.strip():
                sections.append(f"## {heading}\n\n{content.strip()}")

        if not sections:
            return None
        return "\n\n".join(sections)

    def get_agent_markdown(self, rule_name: str) -> str | None:
        """``get_markdown`` wrapped in the agent-facing remediation procedure.

        Returns ``None`` on the same conditions as ``get_markdown`` — with no
        options to choose from, the procedure alone is noise.
        """
        guidance = self.get_markdown(rule_name)
        if not guidance:
            return None
        template = _procedure_template()
        if not template:
            return guidance
        return template.replace(_PROCEDURE_PLACEHOLDER, guidance).strip()
