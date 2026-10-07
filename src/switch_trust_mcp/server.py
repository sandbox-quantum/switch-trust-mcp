"""AI-SPM MCP server (Phase 1: read-only, remote-backed).

A local stdio MCP server that lets a coding agent read a Switch Trust instance's
already-enriched AI-SPM issues, inventory, and remediation guidance so it can fix
the flagged code. It is a thin, authenticated REST client over the Switch Trust
API — no scanner runs locally and no backend changes are required.

Run:  switch-trust-mcp
Env:  SWITCH_TRUST_API_KEY (sk_...) and SWITCH_TRUST_INSTANCE (https://<host>)
"""

from __future__ import annotations

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from switch_trust_mcp import client as client_mod
from switch_trust_mcp.client import ClientError, SwitchTrustClient
from switch_trust_mcp.config import ConfigError, load_config
from switch_trust_mcp.remediation import RemediationDocs

logger = logging.getLogger(__name__)

mcp = FastMCP("switch-trust-mcp")

# Lazily initialized shared singletons (config errors surface on first tool use,
# not at import time, so the server process can still start).
_client: SwitchTrustClient | None = None
_remediation: RemediationDocs | None = None


def _get_client() -> SwitchTrustClient:
    global _client
    if _client is None:
        config = load_config()
        _client = SwitchTrustClient(config.instance, config.api_key)
    return _client


def _get_remediation() -> RemediationDocs:
    global _remediation
    if _remediation is None:
        # Shares the client so docs are fetched from the same instance origin
        # (or a local dir when SWITCH_TRUST_REMEDIATION_DIR is set).
        _remediation = RemediationDocs(_get_client())
    return _remediation


def _handle(fn):
    """Turn expected backend/config errors into a readable tool result."""
    try:
        return fn()
    except (ClientError, ConfigError) as exc:
        return {"error": str(exc)}


# --- defensive field extraction --------------------------------------------
# The API JSON shapes are stable but not statically typed here, so these helpers
# look through the common key spellings rather than assuming one.


def _extract_rule_name(record: dict[str, Any]) -> str | None:
    for key in ("rule_name", "ruleName", "name"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _extract_id(record: dict[str, Any]) -> str | None:
    for key in ("id", "issue_id", "issueId", "instance_id", "instanceId"):
        value = record.get(key)
        if value:
            return str(value)
    return None


def _iter_rows(payload: Any) -> list[dict[str, Any]]:
    """Extract the row list from a paged or bare-list response."""
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        for key in ("data", "rows", "items", "results", "objects", "details"):
            value = payload.get(key)
            if isinstance(value, list):
                return [r for r in value if isinstance(r, dict)]
    return []


def _next_cursor(payload: Any) -> str | None:
    """The cursor for the next page, or None when the listing is exhausted.

    The backend returns ``{"data": [...], "cursor": "..."}`` and empties the
    cursor on the last page.
    """
    if isinstance(payload, dict):
        for key in ("cursor", "nextCursor", "next_cursor"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def _rows_to_dicts(payload: Any) -> dict[str, Any]:
    """Convert a tabular ``{cursor, header, rows, total}`` engine-query
    response (guardrail/session/interaction endpoints) into row dicts.

    ``_iter_rows``/``_next_cursor`` assume dict-shaped rows; this shape pairs
    a shared ``header`` list against each ``rows`` entry instead.
    """
    if not isinstance(payload, dict):
        return {"data": [], "cursor": None, "total": None}
    header = payload.get("header") or []
    rows = payload.get("rows") or []
    return {
        # strict=False: a backend row shorter/longer than header must not crash
        # the whole listing over one malformed record.
        "data": [dict(zip(header, row, strict=False)) for row in rows],
        "cursor": payload.get("cursor"),
        "total": payload.get("total"),
    }


def _trim_interaction_row(row: dict[str, Any]) -> dict[str, Any]:
    """Truncate the large free-text fields of an interaction row for list views.

    Full content is available via get_interaction; list results stay compact.
    """
    trimmed = dict(row)
    # Header spelling from the engine-query response is not pinned down here
    # (could be snake_case columns or camelCase), so check both.
    for key in ("prompt_text", "promptText", "response_text", "responseText"):
        value = trimmed.get(key)
        if isinstance(value, str) and len(value) > 200:
            trimmed[key] = value[:200] + "…"
    trimmed.pop("events", None)
    return trimmed


def _trim_run_result(row: dict[str, Any]) -> dict[str, Any]:
    """Compact an evaluation run-result row's conversation transcript.

    Unlike _trim_interaction_row, every turn is kept (turn sequence is the
    signal a multi-turn red-team attack needs) but each turn's text is
    truncated to 300 chars. There is no get_evaluation_run_result detail
    endpoint to fall back to for full text, so this is a real (if narrow)
    information loss for very long transcripts rather than a "see get_x for
    full detail" trim — use the product UI for full-fidelity review.
    """
    trimmed = dict(row)
    conversation = trimmed.get("conversation")
    messages = conversation.get("messages") if isinstance(conversation, dict) else None
    if not isinstance(messages, list):
        return trimmed
    turns = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        content = msg.get("content") or {}
        role = content.get("role") if isinstance(content, dict) else None
        parts = content.get("parts") if isinstance(content, dict) else None
        text = (
            "\n".join(
                p.get("text", "")
                for p in parts
                if isinstance(p, dict) and p.get("text")
            )
            if isinstance(parts, list)
            else ""
        )
        if len(text) > 300:
            text = text[:300] + "…"
        turns.append({"role": role, "text": text})
    trimmed["conversation"] = {"turn_count": len(turns), "messages": turns}
    return trimmed


# --- request budgeting -------------------------------------------------------
# find_issues_for_file fans out: one objects call per issue, one details call per
# object, and every level is itself paginated. Unbounded, one tool call from a
# malfunctioning or hostile MCP client becomes thousands of authenticated backend
# requests. Bounded but silent, it tells an agent a file is clean when the answer
# was merely truncated — the worse failure of the two, since the agent then ships
# the change. Hence: hard caps, and a `scan` block in the result stating whether
# the answer is complete.

_DEFAULT_PAGE_SIZE = 25
_MAX_PAGE_SIZE = 100
_DEFAULT_MAX_ISSUES = 50
_MAX_ISSUES_SCANNED = 500
_MAX_BACKEND_REQUESTS = 300


def _clamp(value: Any, high: int, default: int) -> int:
    """Coerce a caller-supplied count into ``[1, high]``.

    ``bool`` is an ``int`` in Python and ``True`` as a page size is a bug, not a
    request for one row, so it falls back to the default like any other
    non-integer.
    """
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return default
    return min(value, high)


class _Budget:
    """One tool call's allowance of backend requests."""

    def __init__(self, max_requests: int) -> None:
        self._remaining = max_requests
        self.spent = 0
        self.exhausted = False

    def take(self) -> bool:
        if self._remaining <= 0:
            self.exhausted = True
            return False
        self._remaining -= 1
        self.spent += 1
        return True


def _iter_pages(
    fetch: Any, budget: _Budget, page_size: int, limit: int | None = None
) -> Any:
    """Yield rows from a cursor-paginated endpoint until it, or the budget, ends.

    A backend that keeps handing back the same cursor cannot spin here forever:
    every page costs one unit of the shared budget.
    """
    cursor: str | None = None
    yielded = 0
    while True:
        if not budget.take():
            return
        params: dict[str, Any] = {"pageSize": page_size}
        if cursor:
            params["cursor"] = cursor
        payload = fetch(params)
        for row in _iter_rows(payload):
            yield row
            yielded += 1
            if limit is not None and yielded >= limit:
                return
        cursor = _next_cursor(payload)
        if not cursor:
            return


def _finding_paths(detail: dict[str, Any]) -> list[str]:
    """Collect candidate file paths a finding references."""
    paths: list[str] = []

    def add(value: Any) -> None:
        if isinstance(value, str) and value:
            paths.append(value)

    add(detail.get("path"))
    add(detail.get("file"))
    for item in detail.get("evidence") or []:
        if isinstance(item, dict):
            add(item.get("path"))
            add(item.get("file"))
    return paths


def _paths_match(finding_path: str, target: str) -> bool:
    """Best-effort match between a finding's (repo-relative) path and a query path.

    The working-tree path may be absolute or repo-relative and the finding path
    is repo-relative, so match on a shared path suffix in either direction.
    """
    fp = finding_path.replace("\\", "/").strip("/")
    tp = target.replace("\\", "/").strip("/")
    if not fp or not tp:
        return False
    if fp == tp:
        return True
    return fp.endswith("/" + tp) or tp.endswith("/" + fp)


# --- tools: fix-focused core -----------------------------------------------


@mcp.tool()
def get_context() -> dict[str, Any]:
    """Show the resolved backend scope (instance, tenant, workspace).

    Useful to confirm the API key maps to the workspace you expect before
    querying issues.
    """

    def run() -> dict[str, Any]:
        client = _get_client()
        tenant_id, workspace_id = client.resolve_scope()
        return {
            # The validated URL in use, not the raw env var — those differ when
            # SWITCH_TRUST_INSTANCE failed host validation.
            "instance": client.instance,
            "tenant_id": tenant_id,
            "workspace_id": workspace_id,
        }

    return _handle(run)


@mcp.tool()
def list_issues(
    severity: list[str] | None = None,
    rule_id: list[str] | None = None,
    category: list[str] | None = None,
    search: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List AI-SPM issues for the workspace.

    Filters: severity (CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL), rule_id,
    category (vulnerability_category), and search (substring match on rule name).
    Results are paginated: pass the returned cursor to fetch the next page.
    page_size is capped at 100. Use get_issue for full detail and remediation
    guidance on a specific issue.
    """

    def run() -> Any:
        params: dict[str, Any] = {
            "severity": severity,
            "rule_id": rule_id,
            "vulnerability_category": category,
            "pageSize": _clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            "cursor": cursor,
        }
        if search:
            params["rule_name__ilk"] = f"%{search}%"
        return _get_client().list_issues(params)

    return _handle(run)


@mcp.tool()
def get_issue(
    issue_id: str,
    page_size: int = _DEFAULT_PAGE_SIZE,
    cursor: str | None = None,
) -> Any:
    """Get full detail for one issue plus rule-level remediation guidance.

    Returns the issue record, the assembled remediation guidance markdown for the
    issue's rule (when available), and a page of affected objects (assets). The
    objects list is paginated the same way as list_issues: page_size is capped at
    100, and objects.cursor carries forward to fetch the next page. Use
    get_finding_detail for the code location of a specific occurrence.
    """

    def run() -> Any:
        client = _get_client()
        issue = client.get_issue(issue_id)
        issue_record = issue if isinstance(issue, dict) else {}
        rule_name = _extract_rule_name(issue_record)
        guidance = None
        if rule_name:
            guidance = _get_remediation().get_markdown(rule_name)
        objects = client.get_issue_objects(
            issue_id,
            {
                "pageSize": _clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
                "cursor": cursor,
            },
        )
        return {
            "issue": issue,
            "rule_name": rule_name,
            "remediation_guidance": guidance,
            "objects": objects,
        }

    return _handle(run)


@mcp.tool()
def get_finding_detail(
    issue_id: str, object_id: str, detail_id: str | None = None
) -> Any:
    """Get per-finding detail: file path, code snippet, evidence, and remediation.

    Provide the issue_id and object_id (from get_issue's objects). Omit detail_id
    to list all findings for that object, or pass one to fetch a single finding.
    """

    def run() -> Any:
        client = _get_client()
        if detail_id:
            return client.get_object_detail(issue_id, object_id, detail_id)
        return client.get_object_details(issue_id, object_id)

    return _handle(run)


@mcp.tool()
def find_issues_for_file(path: str, max_issues: int = _DEFAULT_MAX_ISSUES) -> Any:
    """Find issues whose findings reference a given working-tree file.

    Convenience for the edit loop: scans up to max_issues issues and returns the
    findings whose file path matches `path` (matched by shared path suffix, so an
    absolute or repo-relative path both work), each with its rule, severity, path,
    and inline remediation text. The backend cannot filter by file, so this is a
    client-side scan and may be slow for large workspaces.

    The scan is bounded: max_issues is capped at 500 and the whole call at 300
    backend requests. Check the returned `scan.complete` — when it is false the
    caps were hit and the file may have findings this result does not list, so
    do not read it as "no issues here". Narrow the search with list_issues
    filters and follow up on specific issues instead.
    """

    def run() -> Any:
        client = _get_client()
        limit = _clamp(max_issues, _MAX_ISSUES_SCANNED, _DEFAULT_MAX_ISSUES)
        page_size = _clamp(limit, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE)
        budget = _Budget(_MAX_BACKEND_REQUESTS)
        matches: list[dict[str, Any]] = []
        issues_scanned = 0
        errors = 0

        for issue_row in _iter_pages(
            client.list_issues, budget, page_size, limit=limit
        ):
            issues_scanned += 1
            issue_id = _extract_id(issue_row)
            if not issue_id:
                continue
            rule_name = _extract_rule_name(issue_row)
            severity = issue_row.get("severity")
            try:
                objects = _iter_pages(
                    lambda params, i=issue_id: client.get_issue_objects(i, params),
                    budget,
                    page_size,
                )
                for obj in objects:
                    object_id = _extract_id(obj)
                    if not object_id:
                        continue
                    # Scoped per object: one unreadable object should not cost
                    # the rest of the issue's findings.
                    try:
                        details = _iter_pages(
                            lambda params, i=issue_id, o=object_id: (
                                client.get_object_details(i, o, params)
                            ),
                            budget,
                            page_size,
                        )
                        for detail in details:
                            matched = [
                                fp
                                for fp in _finding_paths(detail)
                                if _paths_match(fp, path)
                            ]
                            if matched:
                                matches.append(
                                    {
                                        "issue_id": issue_id,
                                        "object_id": object_id,
                                        "detail_id": _extract_id(detail),
                                        "rule_name": rule_name,
                                        "severity": severity,
                                        "matched_paths": matched,
                                        "remediation": detail.get("remediations")
                                        or detail.get("remediation"),
                                        "code_snippet": _first_snippet(detail),
                                    }
                                )
                    except ClientError:
                        errors += 1
            except ClientError:
                errors += 1

        # Deliberately conservative: a workspace holding exactly `limit` issues
        # reports incomplete, because from here that is indistinguishable from
        # one holding more.
        stopped_by = None
        if budget.exhausted:
            stopped_by = "requests"
        elif issues_scanned >= limit:
            stopped_by = "issues"
        return {
            "path": path,
            "matches": matches,
            "match_count": len(matches),
            "scan": {
                "complete": stopped_by is None and errors == 0,
                "issues_scanned": issues_scanned,
                "requests": budget.spent,
                "errors": errors,
                "stopped_by": stopped_by,
            },
        }

    return _handle(run)


def _first_snippet(detail: dict[str, Any]) -> str | None:
    snippet = detail.get("code_snippet")
    if isinstance(snippet, str) and snippet:
        return snippet
    for item in detail.get("evidence") or []:
        if isinstance(item, dict):
            value = item.get("code_snippet") or item.get("codeSnippet")
            if isinstance(value, str) and value:
                return value
    return None


@mcp.tool()
def get_remediation_guidance(rule_name: str) -> dict[str, Any]:
    """Get the rule-level remediation guidance markdown for a rule name.

    The rule_name matches the value shown on issues (see get_issue). Returns None
    guidance for rules without docs — use the per-finding remediation from
    get_finding_detail in that case.

    The guidance is wrapped in the procedure for choosing and applying a
    remediation; get_issue returns the same docs unwrapped, for browsing.
    """

    def run() -> dict[str, Any]:
        return {
            "rule_name": rule_name,
            "remediation_guidance": _get_remediation().get_agent_markdown(rule_name),
        }

    return _handle(run)


# --- tools: inventory browse ------------------------------------------------


def _asset_filter_params(
    name: str | None,
    severity: str | None,
    supplier: str | None,
    library: str | None,
    page_size: int,
    cursor: str | None,
) -> dict[str, Any]:
    # Switch Trust asset endpoints use the generic Expr filter engine: field__op=value.
    params: dict[str, Any] = {
        "pageSize": _clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
        "cursor": cursor,
    }
    if name:
        params["name__ilk"] = f"%{name}%"
    if severity:
        params["severity__eq"] = severity
    if supplier:
        params["supplier__eq"] = supplier
    if library:
        params["library__eq"] = library
    return params


def _list_assets(scope: str, **kwargs: Any) -> Any:
    return _handle(
        lambda: _get_client().list_assets(scope, _asset_filter_params(**kwargs))
    )


def _get_asset_with_edges(scope: str, asset_id: str, edges: tuple[str, ...]) -> Any:
    def run() -> Any:
        client = _get_client()
        result: dict[str, Any] = {"asset": client.get_asset(scope, asset_id)}
        for edge in edges:
            result[edge] = client.get_asset_edge(scope, asset_id, edge)
        return result

    return _handle(run)


@mcp.tool()
def list_models(
    name: str | None = None,
    severity: str | None = None,
    supplier: str | None = None,
    library: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List inventoried AI models. Filters: name, severity, supplier, library.

    page_size is capped at 100; page with the returned cursor for more.
    """
    return _list_assets(
        client_mod.SCOPE_MODELS,
        name=name,
        severity=severity,
        supplier=supplier,
        library=library,
        page_size=page_size,
        cursor=cursor,
    )


@mcp.tool()
def list_agents(
    name: str | None = None,
    severity: str | None = None,
    supplier: str | None = None,
    library: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List inventoried AI agents. Filters: name, severity, supplier, library.

    page_size is capped at 100; page with the returned cursor for more.
    """
    return _list_assets(
        client_mod.SCOPE_AGENTS,
        name=name,
        severity=severity,
        supplier=supplier,
        library=library,
        page_size=page_size,
        cursor=cursor,
    )


@mcp.tool()
def list_tools(
    name: str | None = None,
    severity: str | None = None,
    supplier: str | None = None,
    library: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List inventoried agent tools. Filters: name, severity, supplier, library.

    page_size is capped at 100; page with the returned cursor for more.
    """
    return _list_assets(
        client_mod.SCOPE_TOOLS,
        name=name,
        severity=severity,
        supplier=supplier,
        library=library,
        page_size=page_size,
        cursor=cursor,
    )


@mcp.tool()
def list_mcp_servers(
    name: str | None = None,
    severity: str | None = None,
    supplier: str | None = None,
    library: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List inventoried MCP servers. Filters: name, severity, supplier, library.

    page_size is capped at 100; page with the returned cursor for more.
    """
    return _list_assets(
        client_mod.SCOPE_MCP_SERVERS,
        name=name,
        severity=severity,
        supplier=supplier,
        library=library,
        page_size=page_size,
        cursor=cursor,
    )


@mcp.tool()
def get_model(asset_id: str) -> Any:
    """Get a model's detail plus its attached issues and code locations."""
    return _get_asset_with_edges(
        client_mod.SCOPE_MODELS, asset_id, ("issues", "locations")
    )


@mcp.tool()
def get_agent(asset_id: str) -> Any:
    """Get an agent's detail plus its issues, MCP servers, and code locations."""
    return _get_asset_with_edges(
        client_mod.SCOPE_AGENTS,
        asset_id,
        ("issues", "aispm_mcp_server_dependencies", "locations"),
    )


@mcp.tool()
def get_tool(asset_id: str) -> Any:
    """Get a tool's detail plus its agents, issues, and code locations."""
    return _get_asset_with_edges(
        client_mod.SCOPE_TOOLS, asset_id, ("agents", "issues", "locations")
    )


@mcp.tool()
def get_mcp_server(asset_id: str) -> Any:
    """Get an MCP server's detail plus its issues and code locations.

    Agents using this server are embedded in ``asset`` directly (the backend
    has no standalone "agents" edge for the MCP-server scope).
    """
    return _get_asset_with_edges(
        client_mod.SCOPE_MCP_SERVERS, asset_id, ("issues", "locations")
    )


# --- tools: guardrail policies & LLM-interaction analytics -----------------


@mcp.tool()
def list_guardrail_policies(
    search: str | None = None, page: int = 1, page_size: int = 25
) -> Any:
    """List guardrail policies (input/output detector configurations).

    Filters: search (substring match on policy name). Page-numbered, not
    cursor-based — pass the next page number to page through results.
    page_size is capped at 100. Use get_guardrail_policy for full detail.
    """

    def run() -> Any:
        return _get_client().list_guardrail_policies(
            name=search,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
        )

    return _handle(run)


@mcp.tool()
def get_guardrail_policy(policy_id: str) -> Any:
    """Get one guardrail policy's detail: name, description, and the
    user/assistant detector configuration."""

    def run() -> Any:
        return _get_client().get_guardrail_policy(policy_id)

    return _handle(run)


@mcp.tool()
def get_guardrail_interaction_counts(agent_id: str | None = None) -> Any:
    """Guardrail-decision counts (ok/blocked/redacted/alerted/errored) across
    LLM interactions, optionally scoped to one agent."""

    def run() -> Any:
        return _get_client().get_guardrail_interaction_counts(agent_id=agent_id)

    return _handle(run)


@mcp.tool()
def get_guardrail_outcomes(agent_id: str | None = None) -> Any:
    """Guardrail outcome totals across LLM interactions, optionally scoped to
    one agent. Same underlying data as get_guardrail_interaction_counts,
    without the per-category breakdown."""

    def run() -> Any:
        return _get_client().get_guardrail_outcomes(agent_id=agent_id)

    return _handle(run)


@mcp.tool()
def get_guardrail_categories(agent_id: str | None = None) -> Any:
    """Guardrail-detector-category counts across LLM interactions,
    optionally scoped to one agent."""

    def run() -> Any:
        return _get_client().get_guardrail_categories(agent_id=agent_id)

    return _handle(run)


@mcp.tool()
def list_llm_interactions(
    search: str | None = None,
    agent_id: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List LLM interactions (prompt/response pairs) with guardrail outcomes.

    Filters: search (substring match on prompt text), agent_id. Cursor-paginated:
    pass the returned cursor to fetch the next page. Rows are trimmed (long
    prompt/response text truncated, per-turn events omitted) to protect context
    budget — use get_interaction for full detail on a specific interaction.
    page_size is capped at 100.
    """

    def run() -> Any:
        params: dict[str, Any] = {
            "agent_id": agent_id,
            "pageSize": _clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            "cursor": cursor,
        }
        if search:
            params["prompt_text__ilk"] = f"%{search}%"
        payload = _rows_to_dicts(_get_client().list_llm_interactions(params))
        payload["data"] = [_trim_interaction_row(row) for row in payload["data"]]
        return payload

    return _handle(run)


@mcp.tool()
def get_interaction(interaction_id: str) -> Any:
    """Get one LLM interaction's full detail (prompt, response, guardrail events)."""

    def run() -> Any:
        rows = _rows_to_dicts(_get_client().get_llm_interaction(interaction_id))["data"]
        return rows[0] if rows else {}

    return _handle(run)


@mcp.tool()
def list_llm_sessions(
    agent_id: str,
    sort: str | None = None,
    sort_dir: str | None = None,
    page_size: int = 25,
    cursor: str | None = None,
) -> Any:
    """List LLM sessions (grouped conversation turns) for one agent (required).

    Cursor-paginated; page_size is capped at 100. Use get_llm_session for a
    session's aggregate cost/tokens/turns plus the full per-turn list.
    """

    def run() -> Any:
        payload = _get_client().list_llm_sessions(
            agent_id=agent_id,
            sort=sort,
            sort_dir=sort_dir,
            cursor=cursor,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
        )
        return _rows_to_dicts(payload)

    return _handle(run)


@mcp.tool()
def get_llm_session(session_id: str) -> Any:
    """Get one LLM session's detail: aggregate cost/tokens/turns and the
    full per-turn list."""

    def run() -> Any:
        return _get_client().get_llm_session(session_id)

    return _handle(run)


# --- tools: ROI / cost-optimization analytics -------------------------------


@mcp.tool()
def list_roi_agents(page: int | None = None, page_size: int = 25) -> Any:
    """List agents' LLM activity summaries (latest_interaction_time,
    interaction_count) for the workspace. Drives ROI/cost-optimization
    analysis: an agent with no recent activity has nothing new to analyze.

    page_size is capped at 100.
    """

    def run() -> Any:
        return _get_client().list_roi_agents(
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
        )

    return _handle(run)


@mcp.tool()
def list_roi_interactions(
    agent_id: str,
    since: str | None = None,
    until: str | None = None,
    page: int | None = None,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List one agent's raw LLM interaction rows (with computed cost_usd) —
    the source data the ROI cost-optimization analyses read.

    agent_id is required. since/until are optional RFC3339 timestamps bounding
    interaction_time. page_size is capped at 100.
    """

    def run() -> Any:
        return _get_client().list_roi_interactions(
            agent_id=agent_id,
            since=since,
            until=until,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )

    return _handle(run)


@mcp.tool()
def list_roi_analyses(
    agent_id: str | None = None,
    analysis_type: str | None = None,
    page: int | None = None,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List ROI/cost-optimization analysis results (findings + estimated $
    savings), latest first.

    Filters: agent_id, analysis_type (tool_bloat, model_optimizer, verbosity,
    context_cache_waste, retry_loop_waste). page_size is capped at 100. Use
    get_latest_roi_analyses for just the current recommendation per type, or
    get_roi_analysis for one result's full detail.
    """

    def run() -> Any:
        return _get_client().list_roi_analyses(
            agent_id=agent_id,
            analysis_type=analysis_type,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )

    return _handle(run)


@mcp.tool()
def get_latest_roi_analyses(agent_id: str, analysis_types: list[str]) -> Any:
    """Get the latest *finished* ROI analysis result per type for one agent —
    the agent's current cost-optimization recommendations.

    Both agent_id and analysis_types are required. Returns a dict keyed by
    analysis_type; a type with no finished run yet is simply absent from the
    result rather than erroring.
    """

    def run() -> Any:
        return _get_client().get_latest_roi_analyses(
            agent_id=agent_id,
            analysis_types=",".join(analysis_types),
        )

    return _handle(run)


@mcp.tool()
def get_roi_analysis(analysis_id: str) -> Any:
    """Get one ROI analysis result by ID (findings, estimated $ savings,
    status, timestamps)."""

    def run() -> Any:
        return _get_client().get_roi_analysis(analysis_id)

    return _handle(run)


# --- tools: evaluations & red-teaming (eval) --------------------------------


@mcp.tool()
def list_evaluations(
    search: str | None = None,
    approach: str | None = None,
    page: int = 1,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List evaluation definitions (probes/metrics), including red-teaming
    adversarial probes.

    Filters: search (substring match on name), approach ('probe' or 'metric').
    Attack-technique/goal detail for adversarial_probe evaluations lives in
    each item's config. Page-numbered; page_size is capped at 100. Use
    get_evaluation for full config detail.
    """

    def run() -> Any:
        return _get_client().list_evaluations(
            name=search,
            approach=approach,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )

    return _handle(run)


@mcp.tool()
def get_evaluation(evaluation_id: str) -> Any:
    """Get one evaluation definition's full detail, including its config
    (attack_techniques/adversarial_goals/num_prompts/max_turns for
    adversarial_probe evaluations)."""

    def run() -> Any:
        return _get_client().get_evaluation(evaluation_id)

    return _handle(run)


@mcp.tool()
def list_agent_evaluations(
    agent_id: str | None = None,
    evaluation_id: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List agent<->evaluation assignments with their latest-run status.

    Filters: agent_id, evaluation_id, search (substring match on name). Each
    row includes evaluation_name, latest_run_status/progress/summary, and a
    score_trend (last 5 scores). Page-numbered; page_size is capped at 100.
    Use get_agent_evaluation for full detail, get_agent_evaluation_summary
    for the OWASP-coverage/health rollup across all of one agent's
    evaluations.
    """

    def run() -> Any:
        return _get_client().list_agent_evaluations(
            agent_id=agent_id,
            evaluation_id=evaluation_id,
            name=search,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )

    return _handle(run)


@mcp.tool()
def get_agent_evaluation(agent_evaluation_id: str) -> Any:
    """Get one agent<->evaluation assignment's full detail."""

    def run() -> Any:
        return _get_client().get_agent_evaluation(agent_evaluation_id)

    return _handle(run)


@mcp.tool()
def get_agent_evaluation_summary(agent_id: str) -> Any:
    """Get one agent's evaluation health rollup: health (score/previous_score),
    coverage (per-category pass/at-risk/not-run counts), and score trend over
    time. agent_id is required."""

    def run() -> Any:
        return _get_client().get_agent_evaluation_summary(agent_id)

    return _handle(run)


@mcp.tool()
def list_evaluation_runs(
    evaluation_id: str | None = None,
    agent_evaluation_id: str | None = None,
    page: int = 1,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List evaluation runs. Filters: evaluation_id, agent_evaluation_id.

    status is one of queued/running/finished/error. Page-numbered; page_size
    is capped at 100. Use get_evaluation_run for one run's full detail and
    list_evaluation_run_results for its per-prompt results.
    """

    def run() -> Any:
        return _get_client().list_evaluation_runs(
            evaluation_id=evaluation_id,
            agent_evaluation_id=agent_evaluation_id,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )

    return _handle(run)


@mcp.tool()
def get_evaluation_run(evaluation_run_id: str) -> Any:
    """Get one evaluation run's detail: status, progress, summary, timestamps."""

    def run() -> Any:
        return _get_client().get_evaluation_run(evaluation_run_id)

    return _handle(run)


@mcp.tool()
def list_evaluation_run_results(
    evaluation_run_id: str,
    page: int = 1,
    page_size: int = 25,
    order: str | None = None,
) -> Any:
    """List one run's per-prompt results (score, status, conversation transcript).

    status is one of passed/failed/error/scored. There is no separate detail
    endpoint for a single result, so conversation turns are trimmed here for
    context budget rather than dropped: every turn is kept (turn sequence
    matters for multi-turn attacks) but each turn's text is truncated to 300
    chars. For full-fidelity transcript review, use the product UI.
    Page-numbered; page_size is capped at 100.
    """

    def run() -> Any:
        payload = _get_client().list_evaluation_run_results(
            evaluation_run_id,
            page=page,
            page_size=_clamp(page_size, _MAX_PAGE_SIZE, _DEFAULT_PAGE_SIZE),
            order=order,
        )
        items = payload.get("items") if isinstance(payload, dict) else None
        if isinstance(items, list):
            payload["items"] = [
                _trim_run_result(row) for row in items if isinstance(row, dict)
            ]
        return payload

    return _handle(run)


@mcp.tool()
def get_agent_endpoint(agent_id: str) -> Any:
    """Get one agent's target-endpoint config for red-teaming (endpoint_url,
    endpoint_auth_type, model_type, config). Secrets (endpoint_credential,
    endpoint_headers) are redacted server-side and always come back empty."""

    def run() -> Any:
        return _get_client().get_agent_endpoint(agent_id)

    return _handle(run)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    mcp.run()


if __name__ == "__main__":
    main()
