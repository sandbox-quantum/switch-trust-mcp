"""Thin authenticated REST client for the Switch Trust API.

All read endpoints are tenant + workspace scoped:

    /api/v1/{scope}/tenants/{tenant_id}/workspaces/{workspace_id}{rest}

An ``ApiKey sk_...`` credential is hard-pinned by the backend to exactly one
tenant and one *active* workspace, and the URL scope must match the token's
claims (403 otherwise). So the client discovers the tenant and workspace once
(``GET /v1/auth/tenants``) and reuses them for every scoped call. The developer
never configures IDs.

The transport, auth header, and base URL come from the generated OpenAPI
clients (``_platform_api`` / ``_auth_api``): this module composes them behind
the security wrapper below (scope auto-resolution, the ``encode_path_segment``
allowlist, the ``_SCOPES`` check, ``ApiKey`` auth, and no-secret-logging). Each
generated client's ``base_url`` carries the API prefix (``/api/v1`` for the
platform, ``/v1/auth`` for auth), so the paths this module builds are relative
to it — the same paths the generated typed endpoint functions use, which read
tools can call through the very same clients. The list endpoints use
a generic ``field__op=value`` filter engine that is dynamic by design and cannot
be typed, so those calls go through the client's httpx with explicit params.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

import httpx

from switch_trust_mcp._auth_api.client import AuthenticatedClient as _AuthClient
from switch_trust_mcp._platform_api.api import eval_ as _eval_api
from switch_trust_mcp._platform_api.api.aispm_guardrails import (
    get_aispm_guardrail_categories,
    get_aispm_guardrail_interaction_counts,
    get_aispm_guardrail_outcomes,
)
from switch_trust_mcp._platform_api.api.aispm_llm_interactions import (
    get_aispm_llm_interaction_details,
)
from switch_trust_mcp._platform_api.api.aispm_llm_sessions import (
    get_aispm_llm_session_detail,
    get_aispm_llm_sessions,
)

# Importing each eval_ operation submodule by name is required to populate it
# as an attribute of the ``eval_`` package (a bare `import ... as _eval_api`
# does not). The bound names below are intentionally unused directly: the
# generated module names are identical to the SwitchTrustClient methods below, so
# call sites go through `_eval_api.<op>.sync` instead to avoid shadowing.
from switch_trust_mcp._platform_api.api.eval_ import (  # noqa: F401
    get_agent_endpoint,
    get_agent_evaluation,
    get_agent_evaluation_summary,
    get_evaluation,
    get_evaluation_run,
    list_agent_evaluations,
    list_evaluation_run_results,
    list_evaluation_runs,
    list_evaluations,
)
from switch_trust_mcp._platform_api.api.guardrails import (
    get_aispm_policy,
    list_aispm_policies,
)
from switch_trust_mcp._platform_api.api.roi import (
    roi_get_analysis,
    roi_get_latest_analyses,
    roi_list_agent_activity,
    roi_list_analyses,
    roi_list_interactions,
)
from switch_trust_mcp._platform_api.client import AuthenticatedClient as _PlatformClient
from switch_trust_mcp._platform_api.models.common_request_error import (
    CommonRequestError,
)
from switch_trust_mcp._platform_api.models.get_aispm_agent_edges_edge import (
    GetAispmAgentEdgesEdge,
)
from switch_trust_mcp._platform_api.models.get_aispm_mcp_server_edges_edge import (
    GetAispmMcpServerEdgesEdge,
)
from switch_trust_mcp._platform_api.models.get_aispm_model_edges_edge import (
    GetAispmModelEdgesEdge,
)
from switch_trust_mcp._platform_api.models.get_aispm_tool_edges_edge import (
    GetAispmToolEdgesEdge,
)
from switch_trust_mcp._platform_api.models.list_agent_evaluations_order import (
    ListAgentEvaluationsOrder,
)
from switch_trust_mcp._platform_api.models.list_aispm_policies_order import (
    ListAispmPoliciesOrder,
)
from switch_trust_mcp._platform_api.models.list_evaluation_run_results_order import (
    ListEvaluationRunResultsOrder,
)
from switch_trust_mcp._platform_api.models.list_evaluation_runs_order import (
    ListEvaluationRunsOrder,
)
from switch_trust_mcp._platform_api.models.list_evaluations_approach import (
    ListEvaluationsApproach,
)
from switch_trust_mcp._platform_api.models.list_evaluations_order import (
    ListEvaluationsOrder,
)
from switch_trust_mcp._platform_api.models.roi_list_analyses_order import (
    RoiListAnalysesOrder,
)
from switch_trust_mcp._platform_api.models.roi_list_interactions_order import (
    RoiListInteractionsOrder,
)

# Asset scopes (route segments in the Switch Trust API).
SCOPE_ISSUES = "issues"
SCOPE_MODELS = "aispm-models"
SCOPE_AGENTS = "aispm-agents"
SCOPE_TOOLS = "aispm-tools"
SCOPE_MCP_SERVERS = "aispm-mcp-servers"

# The complete set; ``_scoped`` refuses anything else rather than trusting that
# every caller passes one of the constants above.
_SCOPES = frozenset(
    {SCOPE_ISSUES, SCOPE_MODELS, SCOPE_AGENTS, SCOPE_TOOLS, SCOPE_MCP_SERVERS}
)

# The four asset scopes expose a "get one edge" sub-resource
# (``/{id}/{edge}``), and each has its own backend-defined edge enum — they are
# not interchangeable (e.g. agents reach their MCP servers via
# "aispm_mcp_server_dependencies", tools via "mcp_servers"; MCP servers have no
# "agents" edge at all). ``get_asset_edge`` validates against the matching enum
# below so a mismatched edge name is a ``ClientError`` naming the real options,
# not a bare 404 after a round trip.
_EDGE_ENUMS_BY_SCOPE: dict[str, type] = {
    SCOPE_AGENTS: GetAispmAgentEdgesEdge,
    SCOPE_TOOLS: GetAispmToolEdgesEdge,
    SCOPE_MCP_SERVERS: GetAispmMcpServerEdgesEdge,
    SCOPE_MODELS: GetAispmModelEdgesEdge,
}

# Rule-level remediation markdown has no backend API; it is served as static
# assets by the instance's web server on the same origin, mirroring the web UI.
# These are best-effort enrichment, so the fetch helpers below return None on any
# failure and never raise — they must not break the primary issue/inventory calls.
_REMEDIATION_ASSET_PREFIX = "/assets/docs-remediations"
_REMEDIATION_MAP_FILE = "rule-name-to-remediation-folder-map.json"

# Every value interpolated into a request path — record identifiers from the
# caller, tenant/workspace ids from the backend, remediation folder and fragment
# names from the instance's JSON map — has to be a plain path segment. One
# expression covers the whole hostile set: the leading-alphanumeric requirement
# rejects "", "." and "..", and the character class rejects "/", "\", "?", "#"
# and "%" (so percent-encoded separators too), whitespace and control
# characters. Most real identifiers are a UUID or a slug like
# "ai_ext_agent-confused-deputy-48"; AI-SPM issue ids are the one exception —
# the backend keys them as "<rule_id>|<severity>" (matched there on
# ``rule_id || '|' || severity``), so "|" is allowed too. It is not
# a structural URL character like the ones above, and ``encode_path_segment``
# percent-encodes it (``%7C``) before it ever reaches the request.
#
# ``\Z``, not ``$``: Python's ``$`` also matches just before a trailing newline,
# which would let "iss1\n" through.
_SAFE_PATH_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._|-]*\Z")

# Nothing legitimate is anywhere near this long; the bound keeps a malformed
# caller from building a multi-megabyte URL.
_MAX_SEGMENT_LENGTH = 256


def is_safe_path_segment(value: str) -> bool:
    """True if ``value`` is a plain path segment: no separators, no traversal."""
    return bool(_SAFE_PATH_SEGMENT.match(value))


class ClientError(Exception):
    """Raised for HTTP or transport failures against the backend."""


class _ScrubbedAuthenticatedClient(_PlatformClient):
    """``AuthenticatedClient`` variant safe to retain on ``self``.

    The base class is an attrs class with no ``repr=False`` on ``token``, so
    its generated ``__repr__`` would print the API key. This subclass exists
    solely so a typed client can be kept around (for the ``sync()`` calls in
    ``_typed``) without that risk; nothing else about it differs.
    """

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self._base_url!r})"


def encode_path_segment(kind: str, value: str) -> str:
    """Validate an identifier and encode it as exactly one URL path segment.

    Raised errors reach the caller as a tool result, and — the point of the
    check — no request is issued, so the API key is never attached to a path the
    method's contract does not describe.

    ``quote`` is a no-op for everything this grammar accepts (Python never
    escapes ``A-Za-z0-9._-~``); it is here so that the path is *built* by an
    encoder rather than by string interpolation, and widening the grammar later
    cannot silently reintroduce a structural character.
    """
    if not isinstance(value, str) or not value:
        raise ClientError(f"invalid {kind}: expected a non-empty identifier")
    if len(value) > _MAX_SEGMENT_LENGTH:
        raise ClientError(
            f"invalid {kind}: longer than {_MAX_SEGMENT_LENGTH} characters"
        )
    if not is_safe_path_segment(value):
        raise ClientError(
            f"invalid {kind}: {value!r} is not a plain identifier "
            "(letters, digits, '.', '_' and '-' only)"
        )
    return quote(value, safe="")


def _optional_enum(enum_cls: type, kind: str, value: str | None) -> Any:
    """Convert an optional caller string to ``enum_cls``.

    Returns ``None`` when ``value`` is unset, so callers can omit the kwarg
    entirely rather than pass an explicit ``None`` — the generated
    ``_get_kwargs`` calls ``.value`` on anything that isn't its ``Unset``
    sentinel, so an explicit ``None`` would crash it. Raises ``ClientError``
    (not a bare ``ValueError``) on an invalid value, matching every other
    malformed-input path in this module.
    """
    if not value:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        valid = ", ".join(repr(member.value) for member in enum_cls)
        raise ClientError(
            f"invalid {kind}: {value!r} (expected one of {valid})"
        ) from None


class SwitchTrustClient:
    """Read-only REST client. Not thread-safe (single stdio session)."""

    def __init__(
        self,
        instance: str,
        api_key: str,
        *,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        # The validated instance URL this client is bound to. Exposed so callers
        # report what is actually in use rather than re-reading the environment,
        # which may hold a value that failed validation.
        self.instance = instance

        # ``Authorization: ApiKey <key>`` — the same scheme the events ingestion
        # path uses. The generated ``AuthenticatedClient`` puts the key in the
        # header only, but it also keeps it as an attrs ``token`` field whose
        # default ``__repr__`` would print it. The platform client is retained
        # (as a ``_ScrubbedAuthenticatedClient``, whose ``__repr__`` omits
        # ``token``) so typed ``sync()`` calls have something to pass as
        # ``client=``; the auth client has no typed calls, so it is used only
        # transiently to build its httpx client and then discarded — the key is
        # never stored on ``self`` in a repr-able form and never logged.
        # ``base_url`` carries the API prefix so paths built here are relative
        # to it, matching the generated typed endpoint functions.
        #
        # All three clients hit the same origin, so they share one connection
        # pool via a single transport rather than opening one pool each.
        transport = transport or httpx.HTTPTransport()
        httpx_args = {"transport": transport}
        platform = _ScrubbedAuthenticatedClient(
            base_url=f"{instance}/api/v1",
            token=api_key,
            prefix="ApiKey",
            timeout=httpx.Timeout(timeout),
            httpx_args=httpx_args,
        )
        auth = _AuthClient(
            base_url=f"{instance}/v1/auth",
            token=api_key,
            prefix="ApiKey",
            timeout=httpx.Timeout(timeout),
            httpx_args=httpx_args,
        )
        self._platform_client = platform
        self._platform_http = platform.get_httpx_client()
        self._auth_http = auth.get_httpx_client()

        # Rule-level remediation markdown is served as static assets off the
        # origin root (not under /api/v1), so it needs a client bound to the
        # bare instance. Same credential, header-only, same shared transport.
        self._static_http = httpx.Client(
            base_url=instance,
            headers={"Authorization": f"ApiKey {api_key}"},
            timeout=timeout,
            transport=transport,
        )

        self._tenant_id: str | None = None
        self._workspace_id: str | None = None

    def close(self) -> None:
        self._platform_http.close()
        self._auth_http.close()
        self._static_http.close()

    def __enter__(self) -> SwitchTrustClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- scope discovery ---------------------------------------------------

    def resolve_scope(self) -> tuple[str, str]:
        """Resolve (tenant_id, workspace_id) from the API key, cached per session."""
        if self._tenant_id and self._workspace_id:
            return self._tenant_id, self._workspace_id

        payload = self._request(self._auth_http, "GET", "/tenants")
        for tenant in _iter_tenants(payload):
            metadata = tenant.get("metadata") or tenant.get("Metadata") or {}
            tenant_id = metadata.get("tenant_id")
            workspace_id = metadata.get("active_workspace_id") or metadata.get(
                "workspace_id"
            )
            if tenant_id and workspace_id:
                # These come from the backend rather than the caller, but they
                # are interpolated into every credentialed path below, so they
                # get the same treatment. Fail here rather than on the first
                # scoped call, where the cause would be less obvious.
                for kind, value in (
                    ("tenant_id", tenant_id),
                    ("active_workspace_id", workspace_id),
                ):
                    encode_path_segment(kind, value)
                self._tenant_id = tenant_id
                self._workspace_id = workspace_id
                return tenant_id, workspace_id

        raise ClientError(
            "Could not resolve tenant_id/active_workspace_id from "
            "GET /v1/auth/tenants — check that the API key's org has the "
            "'tenant_id' and 'active_workspace_id' metadata set."
        )

    # -- low-level ---------------------------------------------------------

    def _request(
        self,
        http: httpx.Client,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Issue a request through a generated client's httpx and return JSON.

        ``path`` is relative to the client's ``base_url`` (which carries the
        ``/api/v1`` or ``/v1/auth`` prefix). List endpoints use a dynamic
        ``field__op=value`` filter engine that the spec cannot type, so params
        are passed straight through rather than via the generated typed
        functions, which accept only the documented query parameters.
        """
        try:
            response = http.request(method, path, params=_clean_params(params))
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ClientError(
                f"{method} {path} -> HTTP {exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise ClientError(f"{method} {path} failed: {type(exc).__name__}") from exc
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise ClientError(f"{method} {path} -> malformed JSON response") from exc

    def _scoped(
        self, scope: str, rest: str = "", params: dict[str, Any] | None = None
    ) -> Any:
        """Issue a GET against a tenant/workspace-scoped path.

        ``rest`` is assembled by the callers below and must already be built
        from ``encode_path_segment`` output — it is the one part of the path
        this method cannot validate for itself.
        """
        if scope not in _SCOPES:
            raise ClientError(f"unknown API scope {scope!r}")
        tenant_id, workspace_id = self.resolve_scope()
        # Relative to the platform client's base_url, which ends in /api/v1.
        path = (
            f"/{scope}"
            f"/tenants/{encode_path_segment('tenant_id', tenant_id)}"
            f"/workspaces/{encode_path_segment('workspace_id', workspace_id)}{rest}"
        )
        return self._request(self._platform_http, "GET", path, params=params)

    def _typed(self, sync_fn: Any, *args: Any, **kwargs: Any) -> Any:
        """Call a generated ``sync()`` function through the retained typed
        client and convert its parsed attrs model to a plain dict via the
        model's own ``to_dict()``.

        Raises ``ClientError`` on an error-shaped response (``CommonRequestError``)
        or an undocumented status (``sync()`` returns ``None``).
        """
        result = sync_fn(*args, client=self._platform_client, **kwargs)
        if result is None:
            raise ClientError(f"{sync_fn.__module__} -> undocumented response status")
        if isinstance(result, CommonRequestError):
            raise ClientError(f"{sync_fn.__module__} -> {result.to_dict()}")
        return result.to_dict()

    # -- issues ------------------------------------------------------------

    def list_issues(self, params: dict[str, Any] | None = None) -> Any:
        return self._scoped(SCOPE_ISSUES, "", params)

    def get_issue(self, issue_id: str) -> Any:
        issue = encode_path_segment("issue_id", issue_id)
        return self._scoped(SCOPE_ISSUES, f"/{issue}")

    def get_issue_objects(
        self, issue_id: str, params: dict[str, Any] | None = None
    ) -> Any:
        issue = encode_path_segment("issue_id", issue_id)
        return self._scoped(SCOPE_ISSUES, f"/{issue}/objects", params)

    def get_object_details(
        self, issue_id: str, object_id: str, params: dict[str, Any] | None = None
    ) -> Any:
        issue = encode_path_segment("issue_id", issue_id)
        obj = encode_path_segment("object_id", object_id)
        return self._scoped(SCOPE_ISSUES, f"/{issue}/objects/{obj}/details", params)

    def get_object_detail(self, issue_id: str, object_id: str, detail_id: str) -> Any:
        issue = encode_path_segment("issue_id", issue_id)
        obj = encode_path_segment("object_id", object_id)
        detail = encode_path_segment("detail_id", detail_id)
        return self._scoped(SCOPE_ISSUES, f"/{issue}/objects/{obj}/details/{detail}")

    # -- inventory assets --------------------------------------------------

    def list_assets(self, scope: str, params: dict[str, Any] | None = None) -> Any:
        return self._scoped(scope, "", params)

    def get_asset(self, scope: str, asset_id: str) -> Any:
        return self._scoped(scope, f"/{encode_path_segment('asset_id', asset_id)}")

    def get_asset_edge(
        self,
        scope: str,
        asset_id: str,
        edge: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        # ``edge`` is chosen from a fixed tuple by the tool layer today, and the
        # backend 404s on an unknown one. Checked against the scope's real
        # OpenAPI-generated edge enum (``_EDGE_ENUMS_BY_SCOPE``) so a stale or
        # copy-pasted edge name fails immediately with the valid options, not a
        # bare 404 after a round trip — see the enum for why the four scopes
        # cannot share one edge vocabulary.
        edge_enum = _EDGE_ENUMS_BY_SCOPE.get(scope)
        if edge_enum is not None:
            try:
                edge_enum(edge)
            except ValueError:
                valid = ", ".join(sorted(e.value for e in edge_enum))
                raise ClientError(
                    f"{edge!r} is not a valid edge for scope {scope!r}; "
                    f"expected one of: {valid}"
                ) from None
        asset = encode_path_segment("asset_id", asset_id)
        return self._scoped(
            scope, f"/{asset}/{encode_path_segment('edge', edge)}", params
        )

    # -- guardrail policies & LLM-interaction analytics ---------------------

    def list_guardrail_policies(
        self,
        name: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {"name": name, "page": page, "page_size": page_size}
        order_enum = _optional_enum(ListAispmPoliciesOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(list_aispm_policies.sync, tenant_id, workspace_id, **kwargs)

    def get_guardrail_policy(self, policy_id: str) -> Any:
        policy_id = encode_path_segment("policy_id", policy_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(get_aispm_policy.sync, tenant_id, workspace_id, policy_id)

    def _guardrail_analytics(
        self,
        module: Any,
        agent_id: str | None,
        start_time: str | None,
        end_time: str | None,
    ) -> Any:
        """Shared by the categories/counts/outcomes dashboards below.

        Typed for ``start_time``/``end_time``; ``agent_id`` is injected into
        the built params afterward because the generated spec does not
        document it on this route yet, even though the backend (and the UI's
        ``getInteractionCounts`` et al.) support it.
        """
        tenant_id, workspace_id = self.resolve_scope()
        kwargs = module._get_kwargs(
            tenant_id, workspace_id, start_time=start_time, end_time=end_time
        )
        if agent_id is not None:
            kwargs["params"]["agent_id"] = agent_id
        return self._request(
            self._platform_http,
            kwargs["method"].upper(),
            kwargs["url"],
            params=kwargs["params"],
        )

    def get_guardrail_categories(
        self,
        agent_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> Any:
        return self._guardrail_analytics(
            get_aispm_guardrail_categories, agent_id, start_time, end_time
        )

    def get_guardrail_interaction_counts(
        self,
        agent_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> Any:
        return self._guardrail_analytics(
            get_aispm_guardrail_interaction_counts, agent_id, start_time, end_time
        )

    def get_guardrail_outcomes(
        self,
        agent_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> Any:
        return self._guardrail_analytics(
            get_aispm_guardrail_outcomes, agent_id, start_time, end_time
        )

    def list_llm_interactions(self, params: dict[str, Any] | None = None) -> Any:
        # No typed function exists for this endpoint at all — the generated
        # signature declares zero query params — so this stays on raw httpx,
        # like list_issues/list_assets, just outside the asset _SCOPES set.
        tenant_id, workspace_id = self.resolve_scope()
        path = (
            "/aispm-llm-interactions"
            f"/tenants/{encode_path_segment('tenant_id', tenant_id)}"
            f"/workspaces/{encode_path_segment('workspace_id', workspace_id)}"
        )
        return self._request(self._platform_http, "GET", path, params=params)

    def get_llm_interaction(self, interaction_id: str) -> Any:
        interaction_id = encode_path_segment("interaction_id", interaction_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            get_aispm_llm_interaction_details.sync,
            tenant_id,
            workspace_id,
            interaction_id,
        )

    def list_llm_sessions(
        self,
        agent_id: str,
        sort: str | None = None,
        sort_dir: str | None = None,
        cursor: str | None = None,
        page_size: int | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            get_aispm_llm_sessions.sync,
            tenant_id,
            workspace_id,
            agent_id=agent_id,
            sort=sort,
            sort_dir=sort_dir,
            cursor=cursor,
            page_size=page_size,
        )

    def get_llm_session(self, session_id: str) -> Any:
        session_id = encode_path_segment("session_id", session_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            get_aispm_llm_session_detail.sync, tenant_id, workspace_id, session_id
        )

    # -- ROI / cost-optimization analytics -----------------------------------

    def list_roi_agents(
        self,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            roi_list_agent_activity.sync,
            tenant_id,
            workspace_id,
            page=page,
            page_size=page_size,
        )

    def list_roi_interactions(
        self,
        agent_id: str,
        since: str | None = None,
        until: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {
            "agent_id": agent_id,
            "since": since,
            "until": until,
            "page": page,
            "page_size": page_size,
        }
        order_enum = _optional_enum(RoiListInteractionsOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(
            roi_list_interactions.sync, tenant_id, workspace_id, **kwargs
        )

    def list_roi_analyses(
        self,
        agent_id: str | None = None,
        analysis_type: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {
            "agent_id": agent_id,
            "analysis_type": analysis_type,
            "page": page,
            "page_size": page_size,
        }
        order_enum = _optional_enum(RoiListAnalysesOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(roi_list_analyses.sync, tenant_id, workspace_id, **kwargs)

    def get_latest_roi_analyses(self, agent_id: str, analysis_types: str) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            roi_get_latest_analyses.sync,
            tenant_id,
            workspace_id,
            agent_id=agent_id,
            analysis_types=analysis_types,
        )

    def get_roi_analysis(self, analysis_id: str) -> Any:
        analysis_id = encode_path_segment("analysis_id", analysis_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(roi_get_analysis.sync, tenant_id, workspace_id, analysis_id)

    # -- evaluations & red-teaming (eval) -----------------------------------

    def list_evaluations(
        self,
        name: str | None = None,
        approach: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {"name": name, "page": page, "page_size": page_size}
        approach_enum = _optional_enum(ListEvaluationsApproach, "approach", approach)
        if approach_enum is not None:
            kwargs["approach"] = approach_enum
        order_enum = _optional_enum(ListEvaluationsOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(
            _eval_api.list_evaluations.sync, tenant_id, workspace_id, **kwargs
        )

    def get_evaluation(self, evaluation_id: str) -> Any:
        evaluation_id = encode_path_segment("evaluation_id", evaluation_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            _eval_api.get_evaluation.sync, tenant_id, workspace_id, evaluation_id
        )

    def list_agent_evaluations(
        self,
        agent_id: str | None = None,
        evaluation_id: str | None = None,
        name: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {
            "agent_id": agent_id,
            "evaluation_id": evaluation_id,
            "name": name,
            "page": page,
            "page_size": page_size,
        }
        order_enum = _optional_enum(ListAgentEvaluationsOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(
            _eval_api.list_agent_evaluations.sync, tenant_id, workspace_id, **kwargs
        )

    def get_agent_evaluation(self, agent_evaluation_id: str) -> Any:
        agent_evaluation_id = encode_path_segment(
            "agent_evaluation_id", agent_evaluation_id
        )
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            _eval_api.get_agent_evaluation.sync,
            tenant_id,
            workspace_id,
            agent_evaluation_id,
        )

    def get_agent_evaluation_summary(self, agent_id: str) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            _eval_api.get_agent_evaluation_summary.sync,
            tenant_id,
            workspace_id,
            agent_id=agent_id,
        )

    def list_evaluation_runs(
        self,
        evaluation_id: str | None = None,
        agent_evaluation_id: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {
            "evaluation_id": evaluation_id,
            "agent_evaluation_id": agent_evaluation_id,
            "page": page,
            "page_size": page_size,
        }
        order_enum = _optional_enum(ListEvaluationRunsOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(
            _eval_api.list_evaluation_runs.sync, tenant_id, workspace_id, **kwargs
        )

    def get_evaluation_run(self, evaluation_run_id: str) -> Any:
        evaluation_run_id = encode_path_segment("evaluation_run_id", evaluation_run_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            _eval_api.get_evaluation_run.sync,
            tenant_id,
            workspace_id,
            evaluation_run_id,
        )

    def list_evaluation_run_results(
        self,
        evaluation_run_id: str,
        page: int | None = None,
        page_size: int | None = None,
        order: str | None = None,
    ) -> Any:
        # Unlike the other eval list methods, evaluation_run_id here is a path
        # param (results are nested under one run), not a query filter.
        evaluation_run_id = encode_path_segment("evaluation_run_id", evaluation_run_id)
        tenant_id, workspace_id = self.resolve_scope()
        kwargs: dict[str, Any] = {"page": page, "page_size": page_size}
        order_enum = _optional_enum(ListEvaluationRunResultsOrder, "order", order)
        if order_enum is not None:
            kwargs["order"] = order_enum
        return self._typed(
            _eval_api.list_evaluation_run_results.sync,
            tenant_id,
            workspace_id,
            evaluation_run_id,
            **kwargs,
        )

    def get_agent_endpoint(self, agent_id: str) -> Any:
        # endpoint_credential/endpoint_headers come back redacted server-side
        # on this public route; nothing to scrub client-side.
        agent_id = encode_path_segment("agent_id", agent_id)
        tenant_id, workspace_id = self.resolve_scope()
        return self._typed(
            _eval_api.get_agent_endpoint.sync, tenant_id, workspace_id, agent_id
        )

    # -- remediation docs (static assets) ----------------------------------

    def _get_static(self, path: str) -> httpx.Response | None:
        """GET a static asset off the instance origin; None on 404/any error.

        Unlike ``_request``, transport and non-404 HTTP errors are swallowed:
        remediation docs are optional enrichment and must never fail a tool.
        """
        try:
            response = self._static_http.get(path)
        except httpx.HTTPError:
            return None
        if response.status_code == 404:
            return None
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            return None
        return response

    def fetch_remediation_map(self) -> dict[str, Any] | None:
        """Fetch the rule-name -> folder map, or None if unavailable."""
        response = self._get_static(
            f"{_REMEDIATION_ASSET_PREFIX}/{_REMEDIATION_MAP_FILE}"
        )
        if response is None or not response.content:
            return None
        try:
            data = response.json()
        except ValueError:
            return None
        return data if isinstance(data, dict) else None

    def fetch_remediation_fragment(self, folder: str, stem: str) -> str | None:
        """Fetch one ``<folder>/<stem>.md`` markdown fragment, or None.

        Returns None without issuing a request if either name is not a plain path
        segment, so no caller can steer the credentialed client off the prefix.
        """
        if not (is_safe_path_segment(folder) and is_safe_path_segment(stem)):
            return None
        response = self._get_static(f"{_REMEDIATION_ASSET_PREFIX}/{folder}/{stem}.md")
        if response is None:
            return None
        return response.text or None


def _iter_tenants(payload: Any) -> list[dict[str, Any]]:
    """Normalize the /v1/auth/tenants response into a list of tenant dicts.

    The endpoint may return a bare list or a wrapped object; handle both.
    """
    if isinstance(payload, list):
        return [t for t in payload if isinstance(t, dict)]
    if isinstance(payload, dict):
        for key in ("tenants", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [t for t in value if isinstance(t, dict)]
        # A single tenant object.
        if payload.get("metadata") or payload.get("Metadata"):
            return [payload]
    return []


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drop keys with ``None`` values so they are not sent as query params."""
    if not params:
        return None
    return {k: v for k, v in params.items() if v is not None}
