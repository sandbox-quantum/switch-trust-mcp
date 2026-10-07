# Security Policy

## Supported Versions

`switch-trust-mcp` is currently in active development. Security fixes are applied to
the latest released version on PyPI.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a Vulnerability

Please **do not** report security vulnerabilities through public GitHub issues,
discussions, or pull requests.

Instead, report them privately using GitHub's
[private vulnerability reporting](https://github.com/sandbox-quantum/switch-trust-mcp/security/advisories/new)
feature (the "Report a vulnerability" button under the repository's **Security**
tab).

When reporting, please include as much of the following as possible:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof of concept
- Affected version(s)
- Any suggested remediation

We will acknowledge receipt of your report and work with you on a coordinated
disclosure. Please give us a reasonable amount of time to address the issue
before any public disclosure.

## Scope

This policy covers the `switch-trust-mcp` package in this repository.

The server is a local stdio MCP server and a **read-only** HTTP client of your
Switch Trust instance. Its security-relevant surface is small and deliberately so:

- **Credential handling.** The API key is read from `SWITCH_TRUST_API_KEY`, sent
  only in the `Authorization: ApiKey ...` request header, and never logged or
  written to disk.
- **Credential targeting.** `SWITCH_TRUST_INSTANCE` is validated against a fail-closed
  allowlist before any credential is attached: an `https://` scheme is required,
  and the host must match an allowlisted domain exactly or as a subdomain of it.
  Anything else — cleartext `http://`, an unknown host, a look-alike domain — is
  rejected rather than downgraded.
- **Egress.** The server issues `GET` requests to that one validated host and
  nowhere else. It ships no telemetry or analytics, spawns no subprocesses, and
  writes no files. `find_issues_for_file` matches paths client-side, so no local
  file content or working-tree path is sent to the backend.
- **Request paths.** Every identifier interpolated into an authenticated URL —
  issue, object, finding and asset ids, the tenant and workspace ids the backend
  hands back, remediation folder names — is validated as a plain path segment
  and percent-encoded before the request is built. Traversal, separators, query
  and fragment delimiters, and control characters are rejected outright, and
  rejection happens *before* any request, so the API key is never attached to a
  path outside the documented API.
- **Bounded work.** Tool arguments that control how much the server fetches are
  clamped (page sizes to 100, `find_issues_for_file` to 500 issues and 300
  backend requests), so a malfunctioning or hostile MCP client cannot turn one
  tool call into unbounded load on your instance. When those bounds truncate a
  scan the result says so explicitly rather than looking complete.
- **Untrusted response data.** Remediation documents are located through a JSON
  map served by the instance. Folder names from that map are validated as plain
  path segments before use, so a malformed or tampered map cannot walk the
  request off the documented asset prefix, nor — when
  `SWITCH_TRUST_REMEDIATION_DIR` is set — read outside that directory.

Reports related to any of the above are especially welcome, as are reports about
dependency vulnerabilities.

### A note on tool output and prompt injection

This server returns content produced by your Switch Trust instance — remediation
markdown, finding descriptions, and code snippets drawn from scanned
repositories — directly into a coding agent's context. That content is only as
trustworthy as the code and configuration it was derived from. Treat MCP tool
results as data, not as instructions, and review any change an agent proposes on
the strength of them.

This is a property of how agents consume MCP tool output generally rather than a
defect specific to this server, but it is the most likely way it participates in
an attack, so we would rather state it plainly than leave it implicit.

## Release integrity

The source here is generated from an internal repository and released by
automation; nothing is published by hand. Because this repository is public and
has a large number of collaborators, "someone pushed a tag" is not by itself
evidence that a release was intended, so three independent controls stand
between a tag and a PyPI upload.

**Tag creation is restricted.** A repository ruleset limits creation, update and
deletion of `refs/tags/v*` to the release automation's deploy key, so
collaborators cannot create, move, or delete a version tag. GitHub scopes that
bypass to deploy keys as a class rather than to one key, so it holds because the
release key is the only deploy key on the repository; adding another, or
editing the ruleset, is an audited repository-admin action.

**Release tags are signed.** Every `vX.Y.Z` tag is an annotated tag, SSH-signed
with that key. Its public half is committed to
[`.github/release-signers`](.github/release-signers), so the attribution is
reproducible by anyone:

```bash
git -c gpg.format=ssh \
    -c gpg.ssh.allowedSignersFile=.github/release-signers \
    verify-tag v0.1.0
```

`.github/workflows/publish.yml` runs that same check before building, and also
requires the tagged commit to be an ancestor of `main` (which is pull-request
protected) and the tag to match the version declared in `pyproject.toml`.

**Publishing is gated.** Uploads use PyPI Trusted Publishing over OIDC, so there
is no long-lived API token to steal. The publish job runs in a `pypi`
environment that accepts deployments only from `v*` tags and requires approval
from a maintainer before the upload runs; administrators cannot bypass that
approval.

**The release is audited, and the audited artifact is the published one.** Every
release runs the full audit against the tagged commit — test suite, lockfile
freshness, licence review, CycloneDX SBOM, dependency vulnerability scan of the
shipped runtime closure, and a secret scan of the tree and its history — and the
reports are retained against that commit. The build then records a `SHA256SUMS`
over the distributions and carries its digest to the publish job out of band, so
an artifact altered between building and uploading fails the comparison rather
than reaching PyPI. Distributions are published with PEP 740 attestations and
carry a signed build-provenance attestation, so a downloaded wheel can be tied
back to the commit and workflow run that produced it:

```bash
gh attestation verify switch_trust_mcp-0.1.0-py3-none-any.whl \
  --repo sandbox-quantum/switch-trust-mcp
```

If you can demonstrate a way to get an artifact onto PyPI under this project
without going through all three, we consider that a vulnerability — please
report it as described above.
