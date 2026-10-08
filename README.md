# switch-trust-mcp

A local [MCP](https://modelcontextprotocol.io) server (stdio) that gives a coding
agent read-only access to a Switch Trust backend's **AI-SPM issues, inventory,
guardrails, cost optimization and remediation guidance** so it can fix the flagged
code.

It is a thin, authenticated REST client over the Switch Trust API — no scanner runs
locally and no backend changes are required. Everything valuable (AI-reasoned
findings, rule-based issues, public-asset vuln enrichment, remediation guidance)
is already computed server-side and served over the existing API / static assets.

## Install & run

The idiomatic way is via the published wheel with `uvx` (no clone, no build step):

```bash
uvx switch-trust-mcp
```

## Configuration

Set two environment variables:

| Variable                 | Meaning                                                        |
| ------------------------ | --------------------------------------------------------------- |
| `SWITCH_TRUST_API_KEY`   | Switch Trust API key (`sk_...`).                                |
| `SWITCH_TRUST_INSTANCE`  | Switch Trust instance base URL, e.g. `https://app.switchagents.ai`. |

The instance URL is validated against a fail-closed host allowlist before any
credential is attached.

The **tenant and workspace are auto-discovered** from the API key at startup —
you do not configure any IDs. A key is pinned to exactly one tenant + active
workspace by the backend.

The API key is only ever sent in the `Authorization: ApiKey ...` header and is
never logged.

## Wiring into a coding agent

Add to your MCP client config (Claude Code `.mcp.json`, Cursor, etc.):

```jsonc
{
  "mcpServers": {
    "switch-trust-mcp": {
      "command": "uvx",
      "args": ["switch-trust-mcp"],
      "env": {
        "SWITCH_TRUST_API_KEY": "sk_...",
        "SWITCH_TRUST_INSTANCE": "https://app.switchagents.ai"
      }
    }
  }
}
```

## Tools

**Fix-focused**

- `get_context` — show the resolved instance / tenant / workspace.
- `list_issues(severity?, rule_id?, category?, search?, page_size?, cursor?)` —
  list issues; paginated, `page_size` capped at 100.
- `get_issue(issue_id, page_size?, cursor?)` — issue detail + assembled
  rule-level remediation guidance + a page of affected objects; `objects` is
  paginated the same way as `list_issues`.
- `get_finding_detail(issue_id, object_id, detail_id?)` — per-finding file path,
  code snippet, evidence, and inline remediation.
- `find_issues_for_file(path, max_issues?)` — issues whose findings reference a
  given working-tree file (client-side scan; matches by shared path suffix).
  The scan follows pagination but is bounded — `max_issues` is capped at 500 and
  the call at 300 backend requests — and returns a `scan` block reporting
  `complete`, `issues_scanned`, `requests` and `errors`. **`complete: false`
  means the caps were hit and the file may have findings this result omits**;
  treat it as "unknown", not as "clean", and narrow the search with
  `list_issues` filters instead.
- `get_remediation_guidance(rule_name)` — rule-level remediation markdown.

**Inventory browse**

- `list_models | list_agents | list_tools | list_mcp_servers(name?, severity?, supplier?, library?, page_size?, cursor?)`
- `get_model | get_agent | get_tool | get_mcp_server(asset_id)` — detail plus
  attached issues, related assets, and code locations.

**Guardrails & LLM-interaction analytics**

- `list_guardrail_policies(search?, page?, page_size?)` — page-numbered (not
  cursor-based); `page_size` capped at 100.
- `get_guardrail_policy(policy_id)` — policy detail: name, description,
  user/assistant detector configuration.
- `get_guardrail_interaction_counts | get_guardrail_outcomes | get_guardrail_categories(agent_id?)`
  — guardrail-decision dashboards across LLM interactions, optionally scoped
  to one agent.
- `list_llm_interactions(search?, agent_id?, page_size?, cursor?)` — prompt/
  response pairs with guardrail outcomes; rows are trimmed (long text
  truncated, per-turn events omitted) for context budget. `page_size` capped
  at 100.
- `get_interaction(interaction_id)` — one interaction's full detail.
- `list_llm_sessions(agent_id, sort?, sort_dir?, page_size?, cursor?)` —
  grouped conversation turns for one agent (required). `page_size` capped at 100.
- `get_llm_session(session_id)` — one session's aggregate cost/tokens/turns
  plus the full per-turn list.

**ROI / cost-optimization**

- `list_roi_agents(page?, page_size?)` — per-agent LLM activity summaries
  (`latest_interaction_time`, `interaction_count`). `page_size` capped at 100.
- `list_roi_interactions(agent_id, since?, until?, page?, page_size?, order?)`
  — one agent's raw LLM interaction rows (with computed `cost_usd`) — the
  source data the cost-optimization analyses read. `agent_id` required;
  `since`/`until` are RFC3339 timestamps. `page_size` capped at 100.
- `list_roi_analyses(agent_id?, analysis_type?, page?, page_size?, order?)` —
  cost-optimization analysis results (findings + estimated `$` savings),
  latest first. `analysis_type` is one of `tool_bloat`, `model_optimizer`,
  `verbosity`, `context_cache_waste`, `retry_loop_waste`. `page_size` capped
  at 100.
- `get_latest_roi_analyses(agent_id, analysis_types)` — the latest *finished*
  result per type for one agent, i.e. its current recommendations. Both
  arguments are required; a type with no finished run is simply absent from
  the result.
- `get_roi_analysis(analysis_id)` — one analysis result's full detail.

**Red-teaming / eval**

- `list_evaluations(search?, approach?, page?, page_size?, order?)` —
  evaluation definitions (probes/metrics), including red-teaming adversarial
  probes; `approach` is `probe` or `metric`. Page-numbered; `page_size`
  capped at 100.
- `get_evaluation(evaluation_id)` — full definition detail, including
  `attack_techniques` / `adversarial_goals` / `num_prompts` / `max_turns` for
  adversarial-probe evaluations.
- `list_agent_evaluations(agent_id?, evaluation_id?, search?, page?, page_size?, order?)`
  — agent↔evaluation assignments, each with `latest_run_status`/`progress`/
  `summary` and a `score_trend` (last 5 scores). Page-numbered; `page_size`
  capped at 100.
- `get_agent_evaluation(agent_evaluation_id)` — one assignment's full detail.
- `get_agent_evaluation_summary(agent_id)` — one agent's evaluation health
  rollup: health score, per-category OWASP coverage, and score trend.
- `list_evaluation_runs(evaluation_id?, agent_evaluation_id?, page?, page_size?, order?)`
  — runs; `status` is `queued`/`running`/`finished`/`error`. Page-numbered;
  `page_size` capped at 100.
- `get_evaluation_run(evaluation_run_id)` — one run's detail.
- `list_evaluation_run_results(evaluation_run_id, page?, page_size?, order?)`
  — one run's per-prompt results; `status` is `passed`/`failed`/`error`/
  `scored`. There is no single-result detail endpoint, so `conversation`
  transcripts are trimmed rather than dropped: every turn is kept but each
  turn's text is truncated to 300 characters. Page-numbered; `page_size`
  capped at 100.
- `get_agent_endpoint(agent_id)` — an agent's red-teaming target-endpoint
  config (`endpoint_url`, `endpoint_auth_type`, `model_type`, `config`);
  secrets are redacted server-side and always come back empty.

## Remediation guidance

Rule-level remediation markdown has **no dedicated API** — it is served by the
instance's web server as static assets at `{instance}/assets/docs-remediations/…`
(the same origin and files the web UI reads). This server fetches them at runtime
over HTTP through the shared client and caches them per session; nothing is
bundled into the package. When a rule has no docs (or the assets origin is
unreachable), fall back to the per-finding `remediation` text from
`get_finding_detail`.

For offline development or tests, set `SWITCH_TRUST_REMEDIATION_DIR` to a local directory
laid out like the assets (`rule-name-to-remediation-folder-map.json` + per-rule
folders); the loader then reads from disk and never touches the network.

## Development

- Layout: `src/switch_trust_mcp/` (`src/` layout), tests under `test/`.
- Editable install: `pip install -e '.[dev]'`, then run `switch-trust-mcp`.
- Docs are fetched from your instance at runtime; for offline work point
  `SWITCH_TRUST_REMEDIATION_DIR` at a local copy of the docs directory.

## Tests

```bash
pytest
```

Tests are hermetic (httpx `MockTransport` for the client and the remediation-docs
fetch, a fake client + `SWITCH_TRUST_REMEDIATION_DIR` for the tools), so they need no
network or live backend.
