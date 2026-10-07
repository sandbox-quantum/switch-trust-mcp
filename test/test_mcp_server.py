"""Unit tests for the AI-SPM MCP server (config, client, remediation, tools).

All tests are hermetic: the REST client is exercised with an httpx MockTransport
and the tool layer is driven with a fake client, so no network or live backend is
needed. Shape assumptions match the Switch Trust API responses.
"""

import json
import os

import httpx
import pytest

from switch_trust_mcp import client as client_mod
from switch_trust_mcp import config as config_mod
from switch_trust_mcp import remediation as remediation_mod
from switch_trust_mcp import server as server_mod
from switch_trust_mcp.client import ClientError, SwitchTrustClient
from switch_trust_mcp.config import (
    ConfigError,
    load_config,
    validate_switch_trust_instance,
)
from switch_trust_mcp.remediation import RemediationDocs

VALID_INSTANCE = "https://flintai.dev"


def _remediation_dir():
    return os.path.join(os.path.dirname(__file__), "testdata", "remediation")


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------


class TestValidateSwitchTrustInstance:
    def test_accepts_allowlisted_https_host(self):
        assert (
            validate_switch_trust_instance("https://flintai.dev")
            == "https://flintai.dev"
        )

    def test_strips_trailing_slash(self):
        assert (
            validate_switch_trust_instance("https://flintai.dev/")
            == "https://flintai.dev"
        )

    def test_rejects_http_scheme(self):
        assert validate_switch_trust_instance("http://flintai.dev") is None

    def test_rejects_non_allowlisted_host(self):
        assert validate_switch_trust_instance("https://evil.com") is None

    def test_accepts_localhost_over_http(self):
        # Local-dev carve-out: cleartext is fine when it never leaves the host.
        assert (
            validate_switch_trust_instance("http://localhost:3030/")
            == "http://localhost:3030"
        )

    def test_rejects_loopback_ip_literals(self):
        # The carve-out is deliberately one spelling: use http://localhost:PORT.
        assert validate_switch_trust_instance("http://127.0.0.1:3030") is None
        assert validate_switch_trust_instance("http://[::1]:3030") is None

    def test_rejects_localhost_lookalike_hosts(self):
        # These all resolve through DNS and could point anywhere.
        assert validate_switch_trust_instance("http://localhost.evil.com") is None
        assert validate_switch_trust_instance("http://notlocalhost") is None
        assert validate_switch_trust_instance("http://api.localhost") is None

    def test_rejects_non_http_scheme_on_localhost(self):
        assert validate_switch_trust_instance("ftp://localhost:3030") is None
        assert validate_switch_trust_instance("file://localhost/etc/passwd") is None

    def test_rejects_lookalike_host(self):
        assert validate_switch_trust_instance("https://evilflintai.dev") is None
        assert (
            validate_switch_trust_instance("https://flintai.dev.attacker.com") is None
        )

    def test_rejects_empty_and_none(self):
        assert validate_switch_trust_instance(None) is None
        assert validate_switch_trust_instance("") is None


class TestLoadConfig:
    def test_reads_env_vars(self, monkeypatch):
        monkeypatch.setenv("SWITCH_TRUST_API_KEY", "sk_switch_trust")
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", VALID_INSTANCE)
        config = load_config()
        assert config.api_key == "sk_switch_trust"
        assert config.instance == VALID_INSTANCE

    def test_missing_key_raises(self, monkeypatch):
        for name in config_mod.API_KEY_ENV_VARS:
            monkeypatch.delenv(name, raising=False)
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", VALID_INSTANCE)
        with pytest.raises(ConfigError):
            load_config()

    def test_invalid_instance_raises(self, monkeypatch):
        monkeypatch.setenv("SWITCH_TRUST_API_KEY", "sk_switch_trust")
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", "http://flintai.dev")
        with pytest.raises(ConfigError):
            load_config()

    def test_accepts_localhost_instance(self, monkeypatch):
        monkeypatch.setenv("SWITCH_TRUST_API_KEY", "sk_switch_trust")
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", "http://localhost:3030/")
        assert load_config().instance == "http://localhost:3030"


# --------------------------------------------------------------------------
# remediation
# --------------------------------------------------------------------------


class TestRemediationDocs:
    def test_assembles_present_fragments(self):
        docs = RemediationDocs(root=_remediation_dir())
        markdown = docs.get_markdown("Missing input guardrails")
        assert markdown is not None
        assert "## Summary" in markdown
        assert "## How to resolve" in markdown
        assert "input guardrails" in markdown

    def test_unknown_rule_returns_none(self):
        docs = RemediationDocs(root=_remediation_dir())
        assert docs.get_markdown("No such rule") is None

    def test_rule_mapped_to_no_docs_returns_none(self):
        docs = RemediationDocs(root=_remediation_dir())
        assert docs.get_markdown("Rule without docs") is None

    def test_empty_fragments_return_none(self):
        docs = RemediationDocs(root=_remediation_dir())
        assert docs.get_markdown("Rule with empty fragments") is None

    def test_requires_client_or_override(self, monkeypatch):
        # No override and no client is a programming error, not a runtime path.
        monkeypatch.delenv("SWITCH_TRUST_REMEDIATION_DIR", raising=False)
        with pytest.raises(ValueError):
            RemediationDocs()

    def test_missing_local_map_returns_none(self, tmp_path):
        docs = RemediationDocs(root=tmp_path)
        assert docs.get_markdown("Missing input guardrails") is None

    def test_corrupt_local_map_returns_none(self, tmp_path):
        (tmp_path / "rule-name-to-remediation-folder-map.json").write_text(
            "{not json", encoding="utf-8"
        )
        docs = RemediationDocs(root=tmp_path)
        assert docs.get_markdown("Missing input guardrails") is None

    def test_non_object_local_map_returns_none(self, tmp_path):
        (tmp_path / "rule-name-to-remediation-folder-map.json").write_text(
            '["not", "a", "map"]', encoding="utf-8"
        )
        docs = RemediationDocs(root=tmp_path)
        assert docs.get_markdown("Missing input guardrails") is None

    @pytest.mark.parametrize(
        "folder",
        ["../secrets", "..", ".", "/etc", "nested/folder", "back\\slash", ".hidden"],
    )
    def test_traversal_folder_in_map_is_dropped(self, tmp_path, folder):
        # A tampered map must not be able to read outside the docs directory.
        (tmp_path / "rule-name-to-remediation-folder-map.json").write_text(
            json.dumps({"Evil": folder}), encoding="utf-8"
        )
        docs = RemediationDocs(root=tmp_path)
        assert docs.folder_for_rule("Evil") is None
        assert docs.get_markdown("Evil") is None

    def test_traversal_folder_does_not_read_outside_root(self, tmp_path):
        # The loader only ever reads its six known fragment stems, so the planted
        # file has to be named like one to be reachable at all — otherwise this
        # test would pass with or without the guard.
        (tmp_path / "short-explanation.md").write_text("TOP SECRET", encoding="utf-8")
        root = tmp_path / "docs"
        root.mkdir()
        (root / "rule-name-to-remediation-folder-map.json").write_text(
            json.dumps({"Evil": ".."}), encoding="utf-8"
        )
        # Without the guard this assembles <root>/../short-explanation.md.
        assert RemediationDocs(root=root).get_markdown("Evil") is None

    def test_plain_folder_still_accepted(self, tmp_path):
        (tmp_path / "rule-name-to-remediation-folder-map.json").write_text(
            json.dumps({"Fine": "ai_ext_agent-confused-deputy-48"}), encoding="utf-8"
        )
        docs = RemediationDocs(root=tmp_path)
        assert docs.folder_for_rule("Fine") == "ai_ext_agent-confused-deputy-48"


class TestRemediationProcedure:
    """The bundled agent procedure wrapped around the fetched docs."""

    def test_procedure_asset_is_bundled(self):
        # Guards the packaging wiring: pyproject package-data and the sync
        # ALLOWLIST.
        # Losing any of them ships a wheel whose remediation guidance silently
        # degrades to bare docs.
        template = remediation_mod._procedure_template()
        assert template is not None
        assert remediation_mod._PROCEDURE_PLACEHOLDER in template

    def test_wraps_guidance(self):
        docs = RemediationDocs(root=_remediation_dir())
        wrapped = docs.get_agent_markdown("Missing input guardrails")
        assert wrapped is not None
        # Both halves present, and the docs sit inside the delimiters.
        assert "## How to resolve" in wrapped
        assert "Task:" in wrapped
        assert remediation_mod._PROCEDURE_PLACEHOLDER not in wrapped
        body = wrapped.split("<remediation_guidance>")[1].split(
            "</remediation_guidance>"
        )[0]
        assert "## Summary" in body

    def test_unknown_rule_returns_none_unwrapped(self):
        # No options to choose from -> the procedure alone would be noise.
        docs = RemediationDocs(root=_remediation_dir())
        assert docs.get_agent_markdown("No such rule") is None

    def test_missing_asset_degrades_to_bare_guidance(self, monkeypatch):
        monkeypatch.setattr(remediation_mod, "_procedure_template", lambda: None)
        docs = RemediationDocs(root=_remediation_dir())
        assert docs.get_agent_markdown("Missing input guardrails") == docs.get_markdown(
            "Missing input guardrails"
        )


class TestRemediationDocsHttp:
    """Fetch-over-HTTP path: docs are served as static assets on the instance."""

    @staticmethod
    def _client(handler):
        return SwitchTrustClient(
            VALID_INSTANCE, "sk_test", transport=httpx.MockTransport(handler)
        )

    def test_fetches_and_assembles_over_http(self, monkeypatch):
        monkeypatch.delenv("SWITCH_TRUST_REMEDIATION_DIR", raising=False)

        def handler(request):
            path = request.url.path
            if (
                path
                == "/assets/docs-remediations/rule-name-to-remediation-folder-map.json"
            ):
                return httpx.Response(
                    200, json={"Missing input guardrails": "guardrails"}
                )
            if path == "/assets/docs-remediations/guardrails/short-explanation.md":
                return httpx.Response(200, text="Add guardrails to your inputs.")
            if path == "/assets/docs-remediations/guardrails/how-to-resolve-mcp.md":
                return httpx.Response(200, text="Wrap the call in a guardrail.")
            return httpx.Response(404)

        docs = RemediationDocs(self._client(handler))
        markdown = docs.get_markdown("Missing input guardrails")
        assert markdown is not None
        assert "## Summary" in markdown
        assert "Add guardrails to your inputs." in markdown
        assert "## How to resolve" in markdown
        # Absent fragments (404) are simply skipped.
        assert "## Risk" not in markdown
        # Unmapped rule -> None (fall back to per-finding remediation).
        assert docs.get_markdown("No such rule") is None

    def test_missing_map_returns_none(self, monkeypatch):
        monkeypatch.delenv("SWITCH_TRUST_REMEDIATION_DIR", raising=False)

        def handler(request):
            return httpx.Response(404)

        docs = RemediationDocs(self._client(handler))
        assert docs.get_markdown("Missing input guardrails") is None

    def test_transport_error_returns_none(self, monkeypatch):
        monkeypatch.delenv("SWITCH_TRUST_REMEDIATION_DIR", raising=False)

        def handler(request):
            raise httpx.ConnectError("down")

        docs = RemediationDocs(self._client(handler))
        # Best-effort: a dead assets origin must not raise.
        assert docs.get_markdown("Missing input guardrails") is None

    def test_traversal_folder_issues_no_request(self, monkeypatch):
        monkeypatch.delenv("SWITCH_TRUST_REMEDIATION_DIR", raising=False)
        paths = []

        def handler(request):
            paths.append(request.url.path)
            if request.url.path.endswith(".json"):
                return httpx.Response(200, json={"Evil": "../../../admin"})
            return httpx.Response(200, text="should never be fetched")

        docs = RemediationDocs(self._client(handler))
        assert docs.get_markdown("Evil") is None
        # Only the map was fetched; no fragment request escaped the prefix.
        assert paths == [
            "/assets/docs-remediations/rule-name-to-remediation-folder-map.json"
        ]


class TestSafePathSegment:
    @pytest.mark.parametrize(
        "value",
        [
            "guardrails",
            "ai_ext_agent-confused-deputy-48",
            "a",
            "a.b",
            "A1_-.",
            "ER-v1-arbitrary_code_execution_via_tool_or_eval|CRITICAL",
        ],
    )
    def test_accepts_plain_segments(self, value):
        assert client_mod.is_safe_path_segment(value)

    @pytest.mark.parametrize(
        "value",
        ["", ".", "..", "../x", "a/b", "a\\b", "/abs", ".hidden", "a b", "a?b", "a%2f"],
    )
    def test_rejects_separators_and_traversal(self, value):
        assert not client_mod.is_safe_path_segment(value)

    def test_client_rejects_unsafe_fragment_without_requesting(self):
        requested = []

        def handler(request):
            requested.append(request.url.path)
            return httpx.Response(200, text="nope")

        client = _make_client(handler)
        assert client.fetch_remediation_fragment("../etc", "passwd") is None
        assert client.fetch_remediation_fragment("ok", "../../etc/passwd") is None
        assert requested == []


# --------------------------------------------------------------------------
# client (httpx MockTransport)
# --------------------------------------------------------------------------


def _make_client(handler):
    return SwitchTrustClient(
        VALID_INSTANCE, "sk_test", transport=httpx.MockTransport(handler)
    )


class TestSwitchTrustClient:
    def test_resolve_scope_from_tenants_list(self):
        def handler(request):
            assert request.url.path == "/v1/auth/tenants"
            assert request.headers["Authorization"] == "ApiKey sk_test"
            return httpx.Response(
                200,
                json=[{"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}],
            )

        client = _make_client(handler)
        assert client.resolve_scope() == ("t1", "w1")

    def test_resolve_scope_from_wrapped_object(self):
        def handler(request):
            return httpx.Response(
                200,
                json={
                    "tenants": [{"Metadata": {"tenant_id": "t2", "workspace_id": "w2"}}]
                },
            )

        assert _make_client(handler).resolve_scope() == ("t2", "w2")

    def test_resolve_scope_failure_raises(self):
        def handler(request):
            return httpx.Response(200, json=[{"metadata": {}}])

        with pytest.raises(ClientError):
            _make_client(handler).resolve_scope()

    def test_scoped_path_construction_and_params(self):
        seen = {}

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            seen["path"] = request.url.path
            seen["query"] = str(request.url.query.decode())
            return httpx.Response(200, json={"data": [], "total": 0})

        client = _make_client(handler)
        client.list_issues({"severity": "HIGH", "pageSize": 5, "cursor": None})
        assert seen["path"] == "/api/v1/issues/tenants/t1/workspaces/w1"
        assert "severity=HIGH" in seen["query"]
        assert "pageSize=5" in seen["query"]
        # None-valued params are dropped.
        assert "cursor" not in seen["query"]

    def test_http_error_raises_client_error(self):
        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            return httpx.Response(403, json={"error": "forbidden"})

        with pytest.raises(ClientError):
            _make_client(handler).get_issue("iss1")

    def test_get_issue_encodes_composite_rule_severity_id(self):
        """AI-SPM issue ids are "<rule_id>|<severity>" (the backend matches on
        rule_id || '|' || severity) — the pipe must survive
        encode_path_segment and reach the backend percent-encoded."""
        seen = {}

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            seen["path"] = request.url.path
            seen["raw_path"] = request.url.raw_path.decode()
            return httpx.Response(200, json={"data": []})

        result = _make_client(handler).get_issue(
            "ER-v1-arbitrary_code_execution_via_tool_or_eval|CRITICAL"
        )
        assert result == {"data": []}
        assert seen["path"] == (
            "/api/v1/issues/tenants/t1/workspaces/w1/"
            "ER-v1-arbitrary_code_execution_via_tool_or_eval|CRITICAL"
        )
        assert "%7C" in seen["raw_path"]

    def test_malformed_json_raises_client_error(self):
        def handler(request):
            # A 200 with a non-JSON body (e.g. an HTML error page from a proxy).
            return httpx.Response(200, text="<html>not json</html>")

        with pytest.raises(ClientError):
            _make_client(handler).resolve_scope()

    def test_asset_edge_path(self):
        seen = {}

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            seen["path"] = request.url.path
            return httpx.Response(200, json={"data": []})

        client = _make_client(handler)
        client.get_asset_edge(client_mod.SCOPE_TOOLS, "tool1", "issues")
        assert (
            seen["path"] == "/api/v1/aispm-tools/tenants/t1/workspaces/w1/tool1/issues"
        )

    def test_asset_edge_rejects_edge_not_in_scope_enum(self):
        # "mcp_servers" is a valid edge for tools, but agents reach their MCP
        # servers via "aispm_mcp_server_dependencies" instead — the four asset
        # scopes do not share one edge vocabulary.
        requested = []

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            requested.append(request.url.path)
            return httpx.Response(200, json={"data": []})

        client = _make_client(handler)
        with pytest.raises(ClientError, match="aispm_mcp_server_dependencies"):
            client.get_asset_edge(client_mod.SCOPE_AGENTS, "agent1", "mcp_servers")
        assert requested == []

    def test_asset_edge_rejects_edge_not_valid_for_mcp_server_scope(self):
        # MCP servers have no standalone "agents" edge; that relation is
        # embedded directly in the MCP server's detail response instead.
        requested = []

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            requested.append(request.url.path)
            return httpx.Response(200, json={"data": []})

        client = _make_client(handler)
        with pytest.raises(ClientError):
            client.get_asset_edge(client_mod.SCOPE_MCP_SERVERS, "mcp1", "agents")
        assert requested == []


def _with_tenant_resolution(handler):
    """Wrap a handler so the first call resolves scope, matching real usage."""

    def wrapped(request):
        if request.url.path == "/v1/auth/tenants":
            return httpx.Response(
                200,
                json=[{"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}],
            )
        return handler(request)

    return wrapped


class TestTypedClientCalls:
    """The typed generated `sync()` path used by guardrail/LLM-interaction reads."""

    def test_scrubbed_authenticated_client_repr_omits_token(self):
        scrubbed = client_mod._ScrubbedAuthenticatedClient(
            base_url="https://flintai.dev/api/v1",
            token="sk_should_not_appear",
            prefix="ApiKey",
        )
        assert "sk_should_not_appear" not in repr(scrubbed)
        assert "sk_should_not_appear" not in str(scrubbed)

    def test_list_guardrail_policies_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={
                    "items": [{"id": "p1", "name": "Policy A"}],
                    "page": 2,
                    "page_size": 10,
                    "total_count": 1,
                    "total_pages": 1,
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.list_guardrail_policies(
            name="foo", page=2, page_size=10, order="ASC"
        )
        assert seen["path"] == "/api/v1/guardrails/policies/tenants/t1/workspaces/w1"
        assert "name=foo" in seen["query"]
        assert "page=2" in seen["query"]
        assert "page_size=10" in seen["query"]
        assert "order=ASC" in seen["query"]
        assert result["items"][0]["id"] == "p1"
        assert result["total_count"] == 1

    def test_list_guardrail_policies_without_order(self):
        # Regression: `order` defaulting to None must not reach the generated
        # `_get_kwargs`, which calls `.value` on anything that isn't its
        # `Unset` sentinel and would crash on a bare `None`.
        seen = {}

        def handler(request):
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={
                    "items": [],
                    "page": 1,
                    "page_size": 25,
                    "total_count": 0,
                    "total_pages": 0,
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.list_guardrail_policies(name="foo", page=1, page_size=25)
        assert "order" not in seen["query"]
        assert result["total_count"] == 0

    def test_get_guardrail_policy_path(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            return httpx.Response(
                200, json={"id": "p1", "name": "Policy A", "description": "d"}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_guardrail_policy("p1")
        assert seen["path"] == "/api/v1/guardrails/policies/tenants/t1/workspaces/w1/p1"
        assert result["name"] == "Policy A"

    def test_typed_raises_client_error_on_error_response(self):
        def handler(request):
            return httpx.Response(403, json={"code": 403, "message": "forbidden"})

        client = _make_client(_with_tenant_resolution(handler))
        with pytest.raises(ClientError):
            client.get_guardrail_policy("p1")

    def test_guardrail_analytics_injects_agent_id(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(200, json={"total": 0, "ok": 0})

        client = _make_client(_with_tenant_resolution(handler))
        client.get_guardrail_interaction_counts(agent_id="a1", start_time="2024-01-01")
        assert seen["path"] == (
            "/api/v1/aispm-llm-interactions-dash/tenants/t1/workspaces/w1/counts"
        )
        assert "agent_id=a1" in seen["query"]
        assert "start_time=2024-01-01" in seen["query"]

    def test_list_llm_interactions_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200, json={"cursor": "", "header": ["id"], "rows": [["i1"]]}
            )

        client = _make_client(_with_tenant_resolution(handler))
        client.list_llm_interactions({"agent_id": "a1", "pageSize": 5})
        assert seen["path"] == "/api/v1/aispm-llm-interactions/tenants/t1/workspaces/w1"
        assert "agent_id=a1" in seen["query"]
        assert "pageSize=5" in seen["query"]

    def test_get_llm_interaction_path_and_tabular_shape(self):
        def handler(request):
            return httpx.Response(
                200,
                json={
                    "cursor": "",
                    "header": ["id", "prompt_text"],
                    "rows": [["i1", "hello"]],
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_llm_interaction("i1")
        assert result["header"] == ["id", "prompt_text"]
        assert result["rows"] == [["i1", "hello"]]

    def test_list_llm_sessions_requires_agent_id(self):
        seen = {}

        def handler(request):
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200, json={"cursor": "", "header": ["session_id"], "rows": []}
            )

        client = _make_client(_with_tenant_resolution(handler))
        client.list_llm_sessions("a1", page_size=10)
        assert "agent_id=a1" in seen["query"]
        assert "pageSize=10" in seen["query"]

    def test_get_llm_session_path(self):
        def handler(request):
            return httpx.Response(
                200, json={"session_id": "s1", "turns": 3, "cost": 0.5}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_llm_session("s1")
        assert result["session_id"] == "s1"
        assert result["turns"] == 3

    def test_list_evaluations_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={
                    "items": [{"id": "e1", "name": "Prompt Injection Probe"}],
                    "page": 1,
                    "page_size": 25,
                    "total_count": 1,
                    "total_pages": 1,
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.list_evaluations(name="foo", approach="probe", order="ASC")
        assert seen["path"] == "/api/v1/eval/evaluations/tenants/t1/workspaces/w1"
        assert "name=foo" in seen["query"]
        assert "approach=probe" in seen["query"]
        assert "order=ASC" in seen["query"]
        assert result["items"][0]["id"] == "e1"

    def test_get_evaluation_path(self):
        def handler(request):
            return httpx.Response(
                200, json={"id": "e1", "name": "Prompt Injection Probe"}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_evaluation("e1")
        assert result["name"] == "Prompt Injection Probe"

    def test_get_evaluation_raises_client_error_on_error_response(self):
        def handler(request):
            return httpx.Response(403, json={"code": 403, "message": "forbidden"})

        client = _make_client(_with_tenant_resolution(handler))
        with pytest.raises(ClientError):
            client.get_evaluation("e1")

    def test_list_agent_evaluations_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={"items": [{"id": "ae1"}], "total_count": 1},
            )

        client = _make_client(_with_tenant_resolution(handler))
        client.list_agent_evaluations(agent_id="agn_1", evaluation_id="e1")
        assert seen["path"] == (
            "/api/v1/eval/agent-evaluations/tenants/t1/workspaces/w1"
        )
        assert "agent_id=agn_1" in seen["query"]
        assert "evaluation_id=e1" in seen["query"]

    def test_get_agent_evaluation_path(self):
        def handler(request):
            return httpx.Response(200, json={"id": "ae1", "evaluation_name": "Probe"})

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_agent_evaluation("ae1")
        assert result["evaluation_name"] == "Probe"

    def test_get_agent_evaluation_summary_requires_agent_id(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200, json={"health": {"score": 90}, "coverage": [], "trend": {}}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_agent_evaluation_summary("agn_1")
        assert seen["path"] == (
            "/api/v1/eval/agent-evaluation-summary/tenants/t1/workspaces/w1"
        )
        assert "agent_id=agn_1" in seen["query"]
        assert result["health"]["score"] == 90

    def test_list_evaluation_runs_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(200, json={"items": [{"id": "run1"}]})

        client = _make_client(_with_tenant_resolution(handler))
        client.list_evaluation_runs(evaluation_id="e1")
        assert seen["path"] == "/api/v1/eval/evaluation-runs/tenants/t1/workspaces/w1"
        assert "evaluation_id=e1" in seen["query"]

    def test_get_evaluation_run_path(self):
        def handler(request):
            return httpx.Response(200, json={"id": "run1", "status": "finished"})

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_evaluation_run("run1")
        assert result["status"] == "finished"

    def test_list_evaluation_run_results_path_is_nested_under_run(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            return httpx.Response(200, json={"items": [{"id": "r1"}]})

        client = _make_client(_with_tenant_resolution(handler))
        client.list_evaluation_run_results("run1")
        assert seen["path"] == (
            "/api/v1/eval/evaluation-runs/tenants/t1/workspaces/w1/run1/results"
        )

    def test_get_agent_endpoint_path(self):
        def handler(request):
            return httpx.Response(
                200, json={"agent_id": "agn_1", "endpoint_url": "https://target"}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_agent_endpoint("agn_1")
        assert result["endpoint_url"] == "https://target"

    def test_list_roi_agents_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={
                    "items": [{"agent_id": "agn_1", "interaction_count": 3}],
                    "total_count": 1,
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.list_roi_agents(page=2, page_size=10)
        assert seen["path"] == "/api/v1/roi/agents/tenants/t1/workspaces/w1"
        assert "page=2" in seen["query"]
        assert "page_size=10" in seen["query"]
        assert result["items"][0]["agent_id"] == "agn_1"

    def test_list_roi_interactions_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(200, json={"items": [], "total_count": 0})

        client = _make_client(_with_tenant_resolution(handler))
        client.list_roi_interactions(
            agent_id="agn_1", since="2024-01-01T00:00:00Z", order="ASC"
        )
        assert seen["path"] == "/api/v1/roi/interactions/tenants/t1/workspaces/w1"
        assert "agent_id=agn_1" in seen["query"]
        assert "order=ASC" in seen["query"]

    def test_list_roi_interactions_without_order(self):
        # Regression: `order` defaulting to None must not reach the generated
        # `_get_kwargs`, which calls `.value` on anything that isn't its
        # `Unset` sentinel and would crash on a bare `None`.
        seen = {}

        def handler(request):
            seen["query"] = request.url.query.decode()
            return httpx.Response(200, json={"items": [], "total_count": 0})

        client = _make_client(_with_tenant_resolution(handler))
        client.list_roi_interactions(agent_id="agn_1")
        assert "order" not in seen["query"]

    def test_list_roi_analyses_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200, json={"items": [{"id": "an1"}], "total_count": 1}
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.list_roi_analyses(agent_id="agn_1", analysis_type="tool_bloat")
        assert seen["path"] == "/api/v1/roi/analyses/tenants/t1/workspaces/w1"
        assert "agent_id=agn_1" in seen["query"]
        assert "analysis_type=tool_bloat" in seen["query"]
        assert result["items"][0]["id"] == "an1"

    def test_get_latest_roi_analyses_path_and_params(self):
        seen = {}

        def handler(request):
            seen["path"] = request.url.path
            seen["query"] = request.url.query.decode()
            return httpx.Response(
                200,
                json={
                    "tool_bloat": {
                        "id": "an1",
                        "agent_id": "agn_1",
                        "analysis_type": "tool_bloat",
                        "status": "finished",
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_latest_roi_analyses(
            agent_id="agn_1", analysis_types="tool_bloat,model_optimizer"
        )
        assert seen["path"] == ("/api/v1/roi/analyses/latest/tenants/t1/workspaces/w1")
        assert "agent_id=agn_1" in seen["query"]
        assert "analysis_types=tool_bloat%2Cmodel_optimizer" in seen["query"]
        assert result["tool_bloat"]["status"] == "finished"

    def test_get_roi_analysis_path(self):
        def handler(request):
            return httpx.Response(
                200,
                json={
                    "id": "an1",
                    "agent_id": "agn_1",
                    "analysis_type": "tool_bloat",
                    "status": "finished",
                    "created_at": "2024-01-01T00:00:00Z",
                },
            )

        client = _make_client(_with_tenant_resolution(handler))
        result = client.get_roi_analysis("an1")
        assert result["status"] == "finished"


class TestPathSegmentValidation:
    """Caller-supplied ids must not reach an authenticated URL unvalidated.

    Every case asserts that *no request was issued at all*: the risk being
    guarded is not a failed call, it is the API key being attached to a path the
    method's contract does not describe.
    """

    @staticmethod
    def _client_and_log():
        requested = []

        def handler(request):
            requested.append(request.url.path)
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            return httpx.Response(200, json={"data": []})

        return _make_client(handler), requested

    HOSTILE = [
        "../admin",
        "..",
        ".",
        "../../../etc/passwd",
        "iss1/objects/other",
        "iss1\\objects",
        "iss%2Fadmin",  # percent-encoded separator
        "..%2F..%2Fadmin",
        "iss1?role=admin",  # query injection
        "iss1#fragment",
        "iss1 admin",
        "iss1\n",  # a '$'-anchored regex would have allowed this
        "iss1\nX-Injected: 1",
        "\x00",
        "",
        "   ",
    ]

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_issue_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_issue(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_object_and_detail_ids_rejected(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_object_details("iss1", bad)
        with pytest.raises(ClientError):
            client.get_object_detail("iss1", "obj1", bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_asset_id_and_edge_rejected(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_asset(client_mod.SCOPE_TOOLS, bad)
        with pytest.raises(ClientError):
            client.get_asset_edge(client_mod.SCOPE_TOOLS, "tool1", bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_guardrail_policy_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_guardrail_policy(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_interaction_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_llm_interaction(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_session_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_llm_session(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_roi_analysis_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_roi_analysis(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_evaluation_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_evaluation(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_agent_evaluation_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_agent_evaluation(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_evaluation_run_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_evaluation_run(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_evaluation_run_id_rejected_in_list_results(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.list_evaluation_run_results(bad)
        assert requested == []

    @pytest.mark.parametrize("bad", HOSTILE)
    def test_agent_endpoint_agent_id_rejected_before_any_request(self, bad):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_agent_endpoint(bad)
        assert requested == []

    def test_unknown_scope_rejected(self):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_asset("../../admin", "tool1")
        assert requested == []

    def test_oversized_id_rejected(self):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_issue("a" * 257)
        assert requested == []

    def test_non_string_id_rejected(self):
        client, requested = self._client_and_log()
        with pytest.raises(ClientError):
            client.get_issue(None)
        assert requested == []

    def test_backend_supplied_scope_is_validated(self):
        """A tampered /v1/auth/tenants response cannot redirect scoped calls."""
        requested = []

        def handler(request):
            requested.append(request.url.path)
            return httpx.Response(
                200,
                json=[
                    {
                        "metadata": {
                            "tenant_id": "../../../admin",
                            "active_workspace_id": "w1",
                        }
                    }
                ],
            )

        client = _make_client(handler)
        with pytest.raises(ClientError):
            client.get_issue("iss1")
        # The discovery call happens; no scoped call follows it.
        assert requested == ["/v1/auth/tenants"]

    def test_legitimate_ids_reach_the_expected_path(self):
        seen = {}

        def handler(request):
            if request.url.path == "/v1/auth/tenants":
                return httpx.Response(
                    200,
                    json=[
                        {"metadata": {"tenant_id": "t1", "active_workspace_id": "w1"}}
                    ],
                )
            seen["path"] = request.url.path
            return httpx.Response(200, json={"data": []})

        client = _make_client(handler)
        uuid = "9995f78b-2649-4e36-baf0-65d47317f3bc"
        client.get_object_detail(uuid, "obj_1.2", "d-3")
        assert seen["path"] == (
            f"/api/v1/issues/tenants/t1/workspaces/w1/{uuid}"
            "/objects/obj_1.2/details/d-3"
        )

    def test_remediation_fragment_rejects_trailing_newline(self):
        # Same regex, and the pre-existing caller of it: '$' matched before a
        # trailing newline, so "ok\n" used to be accepted here.
        client, requested = self._client_and_log()
        assert client.fetch_remediation_fragment("ok\n", "how-to-resolve") is None
        assert requested == []


# --------------------------------------------------------------------------
# server tools (fake client)
# --------------------------------------------------------------------------


class FakeClient:
    def __init__(self):
        self.calls = []
        self.instance = VALID_INSTANCE

    def resolve_scope(self):
        return ("t1", "w1")

    def list_issues(self, params=None):
        self.calls.append(("list_issues", params))
        return {
            "data": [
                {
                    "id": "iss1",
                    "rule_name": "Missing input guardrails",
                    "severity": "HIGH",
                }
            ],
            "total": 1,
        }

    def get_issue(self, issue_id):
        return {
            "id": issue_id,
            "rule_name": "Missing input guardrails",
            "severity": "HIGH",
        }

    def get_issue_objects(self, issue_id, params=None):
        self.calls.append(("get_issue_objects", issue_id, params))
        return {"data": [{"id": "obj1"}]}

    def get_object_details(self, issue_id, object_id, params=None):
        return {
            "details": [
                {
                    "id": "d1",
                    "path": "src/agent.py",
                    "code_snippet": "llm.invoke(user_input)",
                    "remediation": "Add an input guardrail.",
                    "evidence": [{"path": "src/agent.py", "code_snippet": "snip"}],
                }
            ]
        }

    def get_object_detail(self, issue_id, object_id, detail_id):
        return {"id": detail_id, "path": "src/agent.py"}

    def list_assets(self, scope, params=None):
        self.calls.append(("list_assets", scope, params))
        return {"data": [{"id": "m1", "name": "gpt-4o"}]}

    def get_asset(self, scope, asset_id):
        return {"id": asset_id, "scope": scope}

    def get_asset_edge(self, scope, asset_id, edge, params=None):
        return {"edge": edge, "data": []}

    def list_guardrail_policies(self, name=None, page=None, page_size=None, order=None):
        self.calls.append(("list_guardrail_policies", name, page, page_size, order))
        return {"items": [{"id": "p1", "name": "Policy A"}], "total_count": 1}

    def get_guardrail_policy(self, policy_id):
        self.calls.append(("get_guardrail_policy", policy_id))
        return {"id": policy_id, "name": "Policy A", "description": "d"}

    def get_guardrail_interaction_counts(self, agent_id=None):
        self.calls.append(("get_guardrail_interaction_counts", agent_id))
        return {"total": 10, "ok": 8, "blocked": 2}

    def get_guardrail_outcomes(self, agent_id=None):
        self.calls.append(("get_guardrail_outcomes", agent_id))
        return {"total": 10, "ok": 8}

    def get_guardrail_categories(self, agent_id=None):
        self.calls.append(("get_guardrail_categories", agent_id))
        return {"total": 10, "categories": []}

    def list_llm_interactions(self, params=None):
        self.calls.append(("list_llm_interactions", params))
        return {
            "cursor": "",
            "header": ["id", "prompt_text", "response_text"],
            "rows": [["i1", "x" * 300, "y" * 300]],
        }

    def get_llm_interaction(self, interaction_id):
        self.calls.append(("get_llm_interaction", interaction_id))
        return {
            "cursor": "",
            "header": ["id", "prompt_text"],
            "rows": [[interaction_id, "hello"]],
        }

    def list_llm_sessions(
        self, agent_id, sort=None, sort_dir=None, cursor=None, page_size=None
    ):
        self.calls.append(
            ("list_llm_sessions", agent_id, sort, sort_dir, cursor, page_size)
        )
        return {"cursor": "", "header": ["session_id", "turns"], "rows": [["s1", 3]]}

    def get_llm_session(self, session_id):
        self.calls.append(("get_llm_session", session_id))
        return {"session_id": session_id, "turns": 3, "cost": 0.5}

    def list_evaluations(
        self, name=None, approach=None, page=None, page_size=None, order=None
    ):
        self.calls.append(("list_evaluations", name, approach, page, page_size, order))
        return {
            "items": [{"id": "e1", "name": "Prompt Injection Probe"}],
            "total_count": 1,
        }

    def get_evaluation(self, evaluation_id):
        self.calls.append(("get_evaluation", evaluation_id))
        return {
            "id": evaluation_id,
            "name": "Prompt Injection Probe",
            "type": "adversarial_probe",
        }

    def list_agent_evaluations(
        self,
        agent_id=None,
        evaluation_id=None,
        name=None,
        page=None,
        page_size=None,
        order=None,
    ):
        self.calls.append(
            (
                "list_agent_evaluations",
                agent_id,
                evaluation_id,
                name,
                page,
                page_size,
                order,
            )
        )
        return {"items": [{"id": "ae1", "evaluation_name": "Probe"}], "total_count": 1}

    def get_agent_evaluation(self, agent_evaluation_id):
        self.calls.append(("get_agent_evaluation", agent_evaluation_id))
        return {"id": agent_evaluation_id, "evaluation_name": "Probe"}

    def get_agent_evaluation_summary(self, agent_id):
        self.calls.append(("get_agent_evaluation_summary", agent_id))
        return {"health": {"score": 90}, "coverage": [], "trend": {}}

    def list_evaluation_runs(
        self,
        evaluation_id=None,
        agent_evaluation_id=None,
        page=None,
        page_size=None,
        order=None,
    ):
        self.calls.append(
            (
                "list_evaluation_runs",
                evaluation_id,
                agent_evaluation_id,
                page,
                page_size,
                order,
            )
        )
        return {"items": [{"id": "run1", "status": "finished"}], "total_count": 1}

    def get_evaluation_run(self, evaluation_run_id):
        self.calls.append(("get_evaluation_run", evaluation_run_id))
        return {"id": evaluation_run_id, "status": "finished"}

    def list_evaluation_run_results(
        self, evaluation_run_id, page=None, page_size=None, order=None
    ):
        self.calls.append(
            ("list_evaluation_run_results", evaluation_run_id, page, page_size, order)
        )
        return {
            "items": [
                {
                    "id": "r1",
                    "evaluation_run_id": evaluation_run_id,
                    "score": 0.5,
                    "status": "failed",
                    "conversation": {
                        "messages": [
                            {
                                "content": {
                                    "role": "user",
                                    "parts": [{"text": "x" * 400}],
                                }
                            },
                            {
                                "content": {
                                    "role": "assistant",
                                    "parts": [{"text": "sure, here you go"}],
                                }
                            },
                        ]
                    },
                }
            ],
            "total_count": 1,
        }

    def get_agent_endpoint(self, agent_id):
        self.calls.append(("get_agent_endpoint", agent_id))
        return {
            "agent_id": agent_id,
            "endpoint_url": "https://target.example",
            "endpoint_auth_type": "bearer",
            "model_type": "openai",
        }

    def list_roi_agents(self, page=None, page_size=None):
        self.calls.append(("list_roi_agents", page, page_size))
        return {
            "items": [{"agent_id": "agn_1", "interaction_count": 3}],
            "total_count": 1,
        }

    def list_roi_interactions(
        self, agent_id, since=None, until=None, page=None, page_size=None, order=None
    ):
        self.calls.append(
            ("list_roi_interactions", agent_id, since, until, page, page_size, order)
        )
        return {"items": [{"id": "i1", "cost_usd": 0.01}], "total_count": 1}

    def list_roi_analyses(
        self, agent_id=None, analysis_type=None, page=None, page_size=None, order=None
    ):
        self.calls.append(
            ("list_roi_analyses", agent_id, analysis_type, page, page_size, order)
        )
        return {
            "items": [{"id": "an1", "analysis_type": "tool_bloat"}],
            "total_count": 1,
        }

    def get_latest_roi_analyses(self, agent_id, analysis_types):
        self.calls.append(("get_latest_roi_analyses", agent_id, analysis_types))
        return {"tool_bloat": {"id": "an1", "status": "finished"}}

    def get_roi_analysis(self, analysis_id):
        self.calls.append(("get_roi_analysis", analysis_id))
        return {"id": analysis_id, "status": "finished"}


@pytest.fixture
def fake_client(monkeypatch):
    fake = FakeClient()
    monkeypatch.setattr(server_mod, "_client", fake)
    monkeypatch.setenv("SWITCH_TRUST_REMEDIATION_DIR", _remediation_dir())
    monkeypatch.setattr(server_mod, "_remediation", None)
    return fake


class TestServerTools:
    def test_get_context(self, fake_client, monkeypatch):
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", VALID_INSTANCE)
        result = server_mod.get_context()
        assert result["instance"] == VALID_INSTANCE
        assert result["tenant_id"] == "t1"
        assert result["workspace_id"] == "w1"

    def test_get_context_reports_validated_instance_not_env(
        self, fake_client, monkeypatch
    ):
        # The env var can hold a value that failed host validation (the client
        # would never have been built from it); report what is actually in use.
        monkeypatch.setenv("SWITCH_TRUST_INSTANCE", "https://evil.com")
        assert server_mod.get_context()["instance"] == VALID_INSTANCE

    def test_list_issues_builds_filters(self, fake_client):
        server_mod.list_issues(severity=["HIGH"], search="guardrail", page_size=5)
        _, params = fake_client.calls[0]
        assert params["severity"] == ["HIGH"]
        assert params["rule_name__ilk"] == "%guardrail%"
        assert params["pageSize"] == 5

    def test_get_issue_merges_remediation(self, fake_client):
        result = server_mod.get_issue("iss1")
        assert result["rule_name"] == "Missing input guardrails"
        assert "## How to resolve" in result["remediation_guidance"]
        # Browsing, not fixing: no agent procedure attached here.
        assert "Task:" not in result["remediation_guidance"]
        assert result["objects"]["data"][0]["id"] == "obj1"

    def test_get_issue_paginates_objects(self, fake_client):
        server_mod.get_issue("iss1", page_size=5, cursor="abc")
        _, issue_id, params = fake_client.calls[0]
        assert issue_id == "iss1"
        assert params["pageSize"] == 5
        assert params["cursor"] == "abc"

    def test_get_issue_clamps_page_size(self, fake_client):
        server_mod.get_issue("iss1", page_size=9999)
        _, _, params = fake_client.calls[0]
        assert params["pageSize"] == 100

    def test_get_finding_detail_single(self, fake_client):
        result = server_mod.get_finding_detail("iss1", "obj1", "d1")
        assert result["id"] == "d1"

    def test_find_issues_for_file_matches_by_suffix(self, fake_client):
        result = server_mod.find_issues_for_file("agent.py")
        assert result["match_count"] == 1
        match = result["matches"][0]
        assert match["issue_id"] == "iss1"
        assert match["rule_name"] == "Missing input guardrails"
        assert match["remediation"] == "Add an input guardrail."
        assert match["code_snippet"] == "llm.invoke(user_input)"

    def test_find_issues_for_file_no_match(self, fake_client):
        result = server_mod.find_issues_for_file("does/not/exist.py")
        assert result["match_count"] == 0

    def test_get_remediation_guidance(self, fake_client):
        result = server_mod.get_remediation_guidance("Missing input guardrails")
        assert "## Summary" in result["remediation_guidance"]
        # Fixing, not browsing: the agent procedure wraps the docs.
        assert "<remediation_guidance>" in result["remediation_guidance"]
        assert "Task:" in result["remediation_guidance"]

    def test_get_remediation_guidance_unknown(self, fake_client):
        result = server_mod.get_remediation_guidance("Nope")
        assert result["remediation_guidance"] is None

    def test_list_models_filter_params(self, fake_client):
        server_mod.list_models(name="gpt", severity="HIGH")
        call = fake_client.calls[-1]
        assert call[1] == client_mod.SCOPE_MODELS
        params = call[2]
        assert params["name__ilk"] == "%gpt%"
        assert params["severity__eq"] == "HIGH"

    def test_get_agent_includes_edges(self, fake_client):
        result = server_mod.get_agent("a1")
        assert result["asset"]["id"] == "a1"
        assert "issues" in result
        assert "aispm_mcp_server_dependencies" in result
        assert "locations" in result

    def test_get_mcp_server_includes_edges(self, fake_client):
        result = server_mod.get_mcp_server("m1")
        assert result["asset"]["id"] == "m1"
        assert "issues" in result
        assert "locations" in result
        # No "agents" edge exists for this scope; it's embedded in ``asset``.
        assert "agents" not in result

    def test_list_guardrail_policies_params(self, fake_client):
        result = server_mod.list_guardrail_policies(search="foo", page=2, page_size=10)
        _, name, page, page_size, order = fake_client.calls[-1]
        assert name == "foo"
        assert page == 2
        assert page_size == 10
        assert result["items"][0]["id"] == "p1"

    def test_get_guardrail_policy(self, fake_client):
        result = server_mod.get_guardrail_policy("p1")
        assert fake_client.calls[-1] == ("get_guardrail_policy", "p1")
        assert result["name"] == "Policy A"

    def test_get_guardrail_interaction_counts_scoped_by_agent(self, fake_client):
        result = server_mod.get_guardrail_interaction_counts(agent_id="a1")
        assert fake_client.calls[-1] == ("get_guardrail_interaction_counts", "a1")
        assert result["total"] == 10

    def test_get_guardrail_outcomes(self, fake_client):
        server_mod.get_guardrail_outcomes(agent_id="a1")
        assert fake_client.calls[-1] == ("get_guardrail_outcomes", "a1")

    def test_get_guardrail_categories(self, fake_client):
        server_mod.get_guardrail_categories(agent_id="a1")
        assert fake_client.calls[-1] == ("get_guardrail_categories", "a1")

    def test_list_llm_interactions_builds_filters_and_trims_rows(self, fake_client):
        result = server_mod.list_llm_interactions(search="hello", agent_id="a1")
        _, params = fake_client.calls[-1]
        assert params["agent_id"] == "a1"
        assert params["prompt_text__ilk"] == "%hello%"
        row = result["data"][0]
        assert row["id"] == "i1"
        # Long free-text fields are truncated for list-view compactness.
        assert len(row["prompt_text"]) < 300
        assert row["prompt_text"].endswith("…")

    def test_get_interaction_returns_full_row(self, fake_client):
        result = server_mod.get_interaction("i1")
        assert fake_client.calls[-1] == ("get_llm_interaction", "i1")
        assert result == {"id": "i1", "prompt_text": "hello"}

    def test_list_llm_sessions_requires_agent_id(self, fake_client):
        result = server_mod.list_llm_sessions(agent_id="a1", page_size=10)
        call = fake_client.calls[-1]
        assert call[0] == "list_llm_sessions"
        assert call[1] == "a1"
        assert call[5] == 10
        assert result["data"][0]["session_id"] == "s1"

    def test_get_llm_session(self, fake_client):
        result = server_mod.get_llm_session("s1")
        assert fake_client.calls[-1] == ("get_llm_session", "s1")
        assert result["turns"] == 3

    def test_list_evaluations_params(self, fake_client):
        result = server_mod.list_evaluations(search="foo", approach="probe", page=2)
        _, name, approach, page, page_size, order = fake_client.calls[-1]
        assert name == "foo"
        assert approach == "probe"
        assert page == 2
        assert result["items"][0]["id"] == "e1"

    def test_get_evaluation(self, fake_client):
        result = server_mod.get_evaluation("e1")
        assert fake_client.calls[-1] == ("get_evaluation", "e1")
        assert result["type"] == "adversarial_probe"

    def test_list_agent_evaluations_params(self, fake_client):
        result = server_mod.list_agent_evaluations(agent_id="agn_1", search="foo")
        call = fake_client.calls[-1]
        assert call[0] == "list_agent_evaluations"
        assert call[1] == "agn_1"
        assert call[3] == "foo"
        assert result["items"][0]["id"] == "ae1"

    def test_get_agent_evaluation(self, fake_client):
        result = server_mod.get_agent_evaluation("ae1")
        assert fake_client.calls[-1] == ("get_agent_evaluation", "ae1")
        assert result["evaluation_name"] == "Probe"

    def test_get_agent_evaluation_summary(self, fake_client):
        result = server_mod.get_agent_evaluation_summary("agn_1")
        assert fake_client.calls[-1] == ("get_agent_evaluation_summary", "agn_1")
        assert result["health"]["score"] == 90

    def test_list_evaluation_runs_params(self, fake_client):
        result = server_mod.list_evaluation_runs(evaluation_id="e1")
        call = fake_client.calls[-1]
        assert call[0] == "list_evaluation_runs"
        assert call[1] == "e1"
        assert result["items"][0]["status"] == "finished"

    def test_get_evaluation_run(self, fake_client):
        result = server_mod.get_evaluation_run("run1")
        assert fake_client.calls[-1] == ("get_evaluation_run", "run1")
        assert result["status"] == "finished"

    def test_list_evaluation_run_results_trims_conversation(self, fake_client):
        result = server_mod.list_evaluation_run_results("run1")
        call = fake_client.calls[-1]
        assert call[0] == "list_evaluation_run_results"
        assert call[1] == "run1"
        conversation = result["items"][0]["conversation"]
        assert conversation["turn_count"] == 2
        first, second = conversation["messages"]
        assert first["role"] == "user"
        assert len(first["text"]) <= 301
        assert first["text"].endswith("…")
        assert second["role"] == "assistant"
        assert second["text"] == "sure, here you go"

    def test_get_agent_endpoint(self, fake_client):
        result = server_mod.get_agent_endpoint("agn_1")
        assert fake_client.calls[-1] == ("get_agent_endpoint", "agn_1")
        assert result["endpoint_url"] == "https://target.example"

    def test_list_roi_agents(self, fake_client):
        result = server_mod.list_roi_agents(page=2)
        call = fake_client.calls[-1]
        assert call[0] == "list_roi_agents"
        assert call[1] == 2
        assert result["items"][0]["agent_id"] == "agn_1"

    def test_list_roi_interactions(self, fake_client):
        result = server_mod.list_roi_interactions(agent_id="agn_1", order="ASC")
        call = fake_client.calls[-1]
        assert call[0] == "list_roi_interactions"
        assert call[1] == "agn_1"
        assert call[6] == "ASC"
        assert result["items"][0]["id"] == "i1"

    def test_list_roi_analyses(self, fake_client):
        result = server_mod.list_roi_analyses(
            agent_id="agn_1", analysis_type="tool_bloat"
        )
        call = fake_client.calls[-1]
        assert call[0] == "list_roi_analyses"
        assert call[1] == "agn_1"
        assert call[2] == "tool_bloat"
        assert result["items"][0]["id"] == "an1"

    def test_get_latest_roi_analyses_joins_types(self, fake_client):
        result = server_mod.get_latest_roi_analyses(
            agent_id="agn_1", analysis_types=["tool_bloat", "model_optimizer"]
        )
        call = fake_client.calls[-1]
        assert call == (
            "get_latest_roi_analyses",
            "agn_1",
            "tool_bloat,model_optimizer",
        )
        assert result["tool_bloat"]["status"] == "finished"

    def test_get_roi_analysis(self, fake_client):
        result = server_mod.get_roi_analysis("an1")
        assert fake_client.calls[-1] == ("get_roi_analysis", "an1")
        assert result["status"] == "finished"


class PagingFakeClient:
    """Fake backend that paginates, counts requests, and can fail selectively.

    ``page_cap`` mimics a backend clamping pageSize server-side, so a test can
    force multiple pages without asking for a huge result set.
    """

    def __init__(self, total_issues, *, page_cap=10, fail_objects_for=(), stuck=False):
        self.total_issues = total_issues
        self.page_cap = page_cap
        self.fail_objects_for = set(fail_objects_for)
        self.stuck = stuck
        self.requests = 0
        self.page_sizes = []
        self.issue_ids_seen = []
        self.instance = VALID_INSTANCE

    def resolve_scope(self):
        return ("t1", "w1")

    def list_issues(self, params=None):
        self.requests += 1
        params = params or {}
        self.page_sizes.append(params.get("pageSize"))
        size = min(params.get("pageSize") or 25, self.page_cap)
        start = int(params.get("cursor") or 0)
        rows = [
            {"id": f"iss{i}", "rule_name": "R", "severity": "HIGH"}
            for i in range(start, min(start + size, self.total_issues))
        ]
        if self.stuck:
            # A backend that never advances: the budget is the only thing that
            # can stop this.
            return {"data": rows, "cursor": "0"}
        nxt = start + size
        return {"data": rows, "cursor": str(nxt) if nxt < self.total_issues else ""}

    def get_issue_objects(self, issue_id, params=None):
        self.requests += 1
        self.issue_ids_seen.append(issue_id)
        if issue_id in self.fail_objects_for:
            raise ClientError("objects unavailable")
        return {"data": [{"id": f"{issue_id}-obj"}], "cursor": ""}

    def get_object_details(self, issue_id, object_id, params=None):
        self.requests += 1
        return {
            "details": [{"id": f"{object_id}-d", "path": "src/agent.py"}],
            "cursor": "",
        }


@pytest.fixture
def paging_client(monkeypatch):
    def install(client):
        monkeypatch.setattr(server_mod, "_client", client)
        return client

    return install


class TestFindIssuesForFileBounds:
    """The scan is bounded, and says so when the answer is partial."""

    def test_clamps_page_size_and_request_budget(self, paging_client):
        fake = paging_client(PagingFakeClient(10_000, page_cap=100))
        result = server_mod.find_issues_for_file("agent.py", max_issues=1_000_000)
        scan = result["scan"]
        assert max(fake.page_sizes) == server_mod._MAX_PAGE_SIZE
        assert scan["requests"] <= server_mod._MAX_BACKEND_REQUESTS
        assert fake.requests <= server_mod._MAX_BACKEND_REQUESTS
        assert scan["complete"] is False
        assert scan["stopped_by"] == "requests"

    @pytest.mark.parametrize("bad", [0, -1, "50", None, True, 2.5])
    def test_invalid_max_issues_falls_back_to_default(self, paging_client, bad):
        fake = paging_client(PagingFakeClient(1_000, page_cap=100))
        result = server_mod.find_issues_for_file("agent.py", max_issues=bad)
        assert result["scan"]["issues_scanned"] == server_mod._DEFAULT_MAX_ISSUES
        assert max(fake.page_sizes) <= server_mod._MAX_PAGE_SIZE

    def test_follows_cursor_to_completion(self, paging_client):
        # 25 issues, 10 per page: the old single-page scan saw only the first 10.
        fake = paging_client(PagingFakeClient(25, page_cap=10))
        result = server_mod.find_issues_for_file("agent.py", max_issues=50)
        assert result["match_count"] == 25
        assert result["scan"]["complete"] is True
        assert result["scan"]["issues_scanned"] == 25
        assert len(fake.page_sizes) == 3  # three pages of issues walked

    def test_stops_at_issue_limit_and_reports_it(self, paging_client):
        fake = paging_client(PagingFakeClient(100, page_cap=10))
        result = server_mod.find_issues_for_file("agent.py", max_issues=5)
        assert result["scan"]["issues_scanned"] == 5
        assert result["scan"]["stopped_by"] == "issues"
        assert result["scan"]["complete"] is False
        assert fake.issue_ids_seen == [f"iss{i}" for i in range(5)]

    def test_partial_failure_keeps_other_matches(self, paging_client):
        paging_client(PagingFakeClient(3, fail_objects_for={"iss1"}))
        result = server_mod.find_issues_for_file("agent.py", max_issues=50)
        assert result["match_count"] == 2
        assert result["scan"]["errors"] == 1
        assert result["scan"]["complete"] is False

    def test_empty_workspace_terminates(self, paging_client):
        fake = paging_client(PagingFakeClient(0))
        result = server_mod.find_issues_for_file("agent.py")
        assert result["match_count"] == 0
        assert result["scan"]["complete"] is True
        assert fake.requests == 1

    def test_non_advancing_cursor_is_bounded(self, paging_client):
        # A backend that keeps returning the same cursor must not spin forever.
        fake = paging_client(PagingFakeClient(50, page_cap=10, stuck=True))
        result = server_mod.find_issues_for_file("agent.py", max_issues=500)
        assert fake.requests <= server_mod._MAX_BACKEND_REQUESTS
        assert result["scan"]["complete"] is False


class TestPageSizeClamping:
    def test_list_issues_page_size_capped(self, fake_client):
        server_mod.list_issues(page_size=10_000)
        _, params = fake_client.calls[0]
        assert params["pageSize"] == server_mod._MAX_PAGE_SIZE

    def test_list_issues_invalid_page_size_defaults(self, fake_client):
        server_mod.list_issues(page_size=0)
        _, params = fake_client.calls[0]
        assert params["pageSize"] == server_mod._DEFAULT_PAGE_SIZE

    def test_asset_list_page_size_capped(self, fake_client):
        server_mod.list_models(page_size=10_000)
        params = fake_client.calls[-1][2]
        assert params["pageSize"] == server_mod._MAX_PAGE_SIZE

    def test_list_guardrail_policies_page_size_capped(self, fake_client):
        server_mod.list_guardrail_policies(page_size=10_000)
        _, _name, _page, page_size, _order = fake_client.calls[-1]
        assert page_size == server_mod._MAX_PAGE_SIZE

    def test_list_llm_interactions_page_size_capped(self, fake_client):
        server_mod.list_llm_interactions(page_size=10_000)
        _, params = fake_client.calls[-1]
        assert params["pageSize"] == server_mod._MAX_PAGE_SIZE

    def test_list_llm_sessions_page_size_capped(self, fake_client):
        server_mod.list_llm_sessions(agent_id="a1", page_size=10_000)
        call = fake_client.calls[-1]
        assert call[5] == server_mod._MAX_PAGE_SIZE

    def test_list_evaluations_page_size_capped(self, fake_client):
        server_mod.list_evaluations(page_size=10_000)
        call = fake_client.calls[-1]
        assert call[4] == server_mod._MAX_PAGE_SIZE

    def test_list_agent_evaluations_page_size_capped(self, fake_client):
        server_mod.list_agent_evaluations(page_size=10_000)
        call = fake_client.calls[-1]
        assert call[5] == server_mod._MAX_PAGE_SIZE

    def test_list_evaluation_runs_page_size_capped(self, fake_client):
        server_mod.list_evaluation_runs(page_size=10_000)
        call = fake_client.calls[-1]
        assert call[4] == server_mod._MAX_PAGE_SIZE

    def test_list_evaluation_run_results_page_size_capped(self, fake_client):
        server_mod.list_evaluation_run_results("run1", page_size=10_000)
        call = fake_client.calls[-1]
        assert call[3] == server_mod._MAX_PAGE_SIZE

    def test_list_roi_agents_page_size_capped(self, fake_client):
        server_mod.list_roi_agents(page_size=10_000)
        call = fake_client.calls[-1]
        assert call[2] == server_mod._MAX_PAGE_SIZE

    def test_list_roi_interactions_page_size_capped(self, fake_client):
        server_mod.list_roi_interactions(agent_id="agn_1", page_size=10_000)
        call = fake_client.calls[-1]
        assert call[5] == server_mod._MAX_PAGE_SIZE

    def test_list_roi_analyses_page_size_capped(self, fake_client):
        server_mod.list_roi_analyses(page_size=10_000)
        call = fake_client.calls[-1]
        assert call[4] == server_mod._MAX_PAGE_SIZE


class TestErrorHandling:
    def test_client_error_returned_as_dict(self, monkeypatch):
        class Boom:
            def resolve_scope(self):
                raise ClientError("boom")

            def list_issues(self, params=None):
                raise ClientError("boom")

        monkeypatch.setattr(server_mod, "_client", Boom())
        result = server_mod.list_issues()
        assert "error" in result
        assert "boom" in result["error"]

    def test_new_domain_tools_return_error_dict(self, monkeypatch):
        class Boom:
            def resolve_scope(self):
                raise ClientError("boom")

            def list_guardrail_policies(self, **kwargs):
                raise ClientError("boom")

            def list_llm_interactions(self, params=None):
                raise ClientError("boom")

            def list_llm_sessions(self, agent_id, **kwargs):
                raise ClientError("boom")

            def list_evaluations(self, **kwargs):
                raise ClientError("boom")

            def list_agent_evaluations(self, **kwargs):
                raise ClientError("boom")

            def list_evaluation_runs(self, **kwargs):
                raise ClientError("boom")

            def list_evaluation_run_results(self, evaluation_run_id, **kwargs):
                raise ClientError("boom")

            def list_roi_agents(self, **kwargs):
                raise ClientError("boom")

            def list_roi_interactions(self, agent_id, **kwargs):
                raise ClientError("boom")

            def list_roi_analyses(self, **kwargs):
                raise ClientError("boom")

            def get_latest_roi_analyses(self, agent_id, analysis_types):
                raise ClientError("boom")

            def get_roi_analysis(self, analysis_id):
                raise ClientError("boom")

        monkeypatch.setattr(server_mod, "_client", Boom())
        assert "error" in server_mod.list_guardrail_policies()
        assert "error" in server_mod.list_llm_interactions()
        assert "error" in server_mod.list_llm_sessions(agent_id="a1")
        assert "error" in server_mod.list_evaluations()
        assert "error" in server_mod.list_agent_evaluations()
        assert "error" in server_mod.list_evaluation_runs()
        assert "error" in server_mod.list_evaluation_run_results("run1")
        assert "error" in server_mod.list_roi_agents()
        assert "error" in server_mod.list_roi_interactions(agent_id="agn_1")
        assert "error" in server_mod.list_roi_analyses()
        assert "error" in server_mod.get_latest_roi_analyses(
            agent_id="agn_1", analysis_types=["tool_bloat"]
        )
        assert "error" in server_mod.get_roi_analysis("an1")


def test_map_file_is_valid_json():
    # Guard: the bundled fixture map parses (mirrors the real map's format).
    with open(
        os.path.join(_remediation_dir(), "rule-name-to-remediation-folder-map.json")
    ) as f:
        data = json.load(f)
    assert "Missing input guardrails" in data
