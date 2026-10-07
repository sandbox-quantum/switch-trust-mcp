# Contributing

`switch-trust-mcp` is developed inside SandboxAQ's internal monorepo and mirrored to
this public repository automatically. **This repo is generated** — commits made
directly here to the mirrored source (`src/`, `test/`, `pyproject.toml`,
`README.md`) will be overwritten by the next sync.

## How to propose a change

- **Security vulnerabilities:** please do **not** open a public issue — see
  [`SECURITY.md`](SECURITY.md) for private disclosure.
- **Bug reports and feature requests:** please open an issue on this repository.
- **Code changes:** the maintainers apply changes to the upstream source and the
  next release syncs them here. If you have a patch, attach it to an issue or open
  a PR for discussion — a maintainer will land the equivalent change upstream and
  credit you.

## Local development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'      # or: pip install -e .
pytest
```

`requirements.lock` pins the full runtime dependency closure; it is generated
upstream and mirrored here, so edits to it are overwritten by the next sync.

To reproduce the release audit (licenses, SBOM, vulnerabilities, secrets) you
also need the audit extra and [gitleaks](https://github.com/gitleaks/gitleaks):

```bash
pip install -e '.[audit]'
make release-audit           # writes reports to release/
```

The remediation guidance is fetched at runtime from your Switch Trust instance.
For offline work, point the loader at a local copy of the docs:

```bash
export SWITCH_TRUST_REMEDIATION_DIR=/path/to/docs-remediations
```

## Releasing (maintainers)

Releases are cut upstream. The sync then pushes a signed `vX.Y.Z` tag here, which
triggers the build and publish-to-PyPI workflow
(`.github/workflows/publish.yml`) via PyPI trusted publishing.

Tags are not something a maintainer pushes by hand: a ruleset restricts
`refs/tags/v*` to the release automation, and the publish workflow refuses any
tag it cannot verify. See [`SECURITY.md`](SECURITY.md#release-integrity).
