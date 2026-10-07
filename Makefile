.PHONY: install install-dev test build clean release-audit license-check sbom vuln-scan secret-scan lock-deps

# Gate targets below must never pipe their exit status away: a recipe reports
# the status of the *last* command in a pipeline, so `pip-audit | tee` passes
# even when the audit fails. Redirect to a file and cat it instead.
#
# `SHELL := /bin/bash` + `.SHELLFLAGS := -o pipefail -c` would be the tidier fix
# and is deliberately NOT used: macOS ships GNU Make 3.81, which predates
# .SHELLFLAGS and ignores it silently, so the gate would work in CI and quietly
# not work on a maintainer's machine.

# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,audit]"

test:
	pytest

build: clean
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info

# ---------------------------------------------------------------------------
# Release audit (mirrors switch-trust-sdk-py / switch-trust-cli)
#
# lock-deps is deliberately NOT part of release-audit: requirements.lock is
# generated upstream and mirrored here, so regenerating it during an audit would
# be overwritten by the next sync. Run it only to preview a dependency change.
# ---------------------------------------------------------------------------

release-audit: license-check sbom vuln-scan secret-scan
	@echo ""
	@echo "=== Release audit complete ==="
	@echo "Outputs in release/:"
	@ls -1 release/*.json release/*.csv release/*.txt 2>/dev/null
	@echo ""

# Packages whose license field carries full license text rather than a short
# SPDX identifier (so --allow-only can't match them). Manually verified permissive:
#   switch-trust-mcp — Apache-2.0 (this project)
IGNORE_PACKAGES := --ignore-packages switch-trust-mcp

license-check:
	@mkdir -p release
	@echo "=== License review ==="
	pip-licenses \
		--format=csv \
		--with-urls \
		--with-authors \
		--output-file=release/licenses.csv
	pip-licenses \
		--format=json \
		--with-urls \
		--with-authors \
		--output-file=release/licenses.json
	@echo "License summary:"
	@pip-licenses --summary --order=count
	@echo ""
	@echo "Checking for copyleft/restricted licenses..."
	@pip-licenses $(IGNORE_PACKAGES) --allow-only="Apache Software License;\
Apache Software License; BSD License;\
Apache Software License; MIT License;\
Apache License 2.0;\
Apache 2.0;\
Apache-2.0;\
Apache-2.0 AND CNRI-Python;\
Apache-2.0 AND MIT;\
Apache-2.0 OR BSD-2-Clause;\
Apache-2.0 OR BSD-3-Clause;\
Apache-2.0 OR MIT;\
Apache 2.0 License;\
Apache License;\
Apache;\
BSD License;\
BSD-2-Clause;\
BSD-3-Clause;\
0BSD;\
BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0;\
BSD 3-Clause OR Apache-2.0;\
3-Clause BSD License;\
MIT License;\
MIT;\
MIT-0;\
MIT OR Apache-2.0;\
MIT-CMU;\
ISC License (ISCL);\
ISC;\
Mozilla Public License 2.0 (MPL 2.0);\
MPL-2.0;\
MPL-2.0 AND (Apache-2.0 OR MIT);\
MPL-2.0 AND MIT;\
Python Software Foundation License;\
PSF;\
PSF-2.0;\
Public Domain;\
The Unlicense (Unlicense);\
Historical Permission Notice and Disclaimer (HPND);\
GNU Lesser General Public License v2 or later (LGPLv2+);\
GNU Lesser General Public License v3 or later (LGPLv3+);\
Zope Public License;\
ZPL-2.1;\
UNKNOWN" \
		2>&1 || (echo "WARNING: Some packages have licenses that need manual review — see above" && exit 1)
	@echo ""
	@echo "Packages with UNKNOWN license (need manual verification):"
	@pip-licenses --format=csv | grep UNKNOWN || echo "  (none)"
	@echo ""
	@echo "All known licenses are Apache-2.0 compatible."

sbom:
	@mkdir -p release
	@echo "=== SBOM generation (CycloneDX) ==="
	cyclonedx-py environment \
		-o release/sbom.json \
		--of json \
		--pyproject pyproject.toml
	@echo "SBOM written to release/sbom.json"

# What the vulnerability gate scans. Empty means "this virtualenv", which is the
# useful default locally. The release workflow overrides it with
# `--requirement requirements.lock` — the runtime closure that actually ships —
# so a CVE in pip-licenses or another dev-only tool cannot block a release:
#
#   make release-audit AUDIT_TARGET="--requirement requirements.lock"
AUDIT_TARGET ?=

# `|| true` on the first run is on purpose: the JSON report is wanted even when
# the scan finds something. The second run is the gate — it fails the audit.
vuln-scan:
	@mkdir -p release
	@echo "=== Dependency vulnerability scan ==="
	pip-audit $(AUDIT_TARGET) --format=json --output=release/vulnerabilities.json || true
	pip-audit $(AUDIT_TARGET) --desc > release/vulnerabilities.txt 2>&1 || ( \
		cat release/vulnerabilities.txt; \
		echo "FAIL: vulnerable dependencies — see release/vulnerabilities.json"; \
		exit 1)
	@cat release/vulnerabilities.txt
	@echo ""

secret-scan:
	@mkdir -p release
	@echo "=== Secret scan (gitleaks) ==="
	gitleaks detect --source . --no-git --redact \
		--report-path=release/gitleaks-report.json \
		--report-format=json \
		--exit-code 1 \
		|| (echo "FAIL: secrets detected — see release/gitleaks-report.json" && exit 1)
	@echo "=== Secret scan (gitleaks) - git history ==="
	gitleaks detect --source . --redact \
		--report-path=release/gitleaks-history-report.json \
		--report-format=json \
		--exit-code 1 \
		|| (echo "FAIL: secrets detected in git history - see release/gitleaks-history-report.json" && exit 1)
	@echo "=== Commit metadata scan (corporate emails in authors, committers, messages) ==="
	@if git log --format='%ae%n%ce%n%B' | grep -Eiq '@([a-z0-9-]+\.)*(sandboxaq|sandboxquantum)\.com([^a-z0-9-]|$$)'; then \
		echo "FAIL: corporate email in commit metadata:"; \
		git log --format='%h %ae %ce' | grep -Ei '(sandboxaq|sandboxquantum)\.com' | head -20; \
		exit 1; \
	fi
	@echo "No secrets detected."

lock-deps:
	@echo "=== Locking dependencies ==="
	pip-compile --strip-extras --output-file=requirements.lock pyproject.toml
	@echo "Locked dependencies written to requirements.lock"
