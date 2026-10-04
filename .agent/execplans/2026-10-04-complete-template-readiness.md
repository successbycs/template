# Complete reusable-template readiness

This ExecPlan is a living document and must be maintained under `.agent/PLANS.md`.

## Purpose / Big Picture

Make the generic Python-first template demonstrably ready to copy into a future project. A maintainer will be able to use the documented Docker workflow, verify the repository, and exercise the bounded bootstrap command in an isolated copy without changing this template's identity or contacting an external service.

## Progress

- [x] (2026-10-04 01:25Z) Established scope: local repository `/home/chris/template`, Docker/WSL developer workflow, and a disposable copied-template bootstrap proof. No product domain, external integration, deployment, or optional pack is in scope.
- [x] (2026-10-04 01:26Z) Inspected the setup guide, bootstrap script, local verifier, CI workflow, compose file, Dev Container definition, project metadata, and optional-pack boundary.
- [x] (2026-10-04 01:28Z) Ran the documented Docker build, locked sync, canonical verifier (77 passed), health check, local SQLite self-test, and no-op demo. Docker Buildx required the approved host fallback because the normal sandbox cannot update Buildx's host activity file.
- [x] (2026-10-04 01:30Z) Exercised bootstrap in isolated synthetic copies. The initial full copied-project verifier exposed two missing rewrite targets and a source-template-only test assumption; each was corrected and regression-tested.
- [x] (2026-10-04 01:32Z) Ran focused bootstrap tests (4 passed) and the source template's Docker verifier (77 passed). The final bootstrapped copy passed its full verifier with 73 passed and 4 expected skips.
- [x] (2026-10-04 01:33Z) Removed only `/tmp/template-readiness-20261004`, `/tmp/template-readiness-regression-20261004`, and `/tmp/template-readiness-final-20261004` after recording their results.

## Surprises & Discoveries

- Observation: WSLg is temporarily disabled outside this repository so the normal Codex sandbox can operate; the after-state preflight is compatible and a normal disposable `apply_patch` cycle passed.
  Evidence: the 2026-10-04 WSLg experiment record in `.agent/execplans/2026-10-02-run-wslg-disable-spike.md` and Issue #35 comment dated 2026-10-04.

- Observation: `.playwright-cli/` is an unrelated untracked working-tree item.
  Evidence: `git status --short` before this plan's work.

- Observation: Bootstrap originally rewrote only top-level package modules, leaving `app_template` imports in nested `src/app_template/symphony/` modules. A bootstrapped copy therefore failed Ruff before its tests ran.
  Evidence: disposable-copy `scripts/verify.py` reported `I001` for `src/future_template_check/symphony/service.py` because imports still named `app_template`.

- Observation: Bootstrap also left package imports in `scripts/prove_deployed_software.py` and the Compose Symphony command unchanged. After correcting nested modules, the disposable-copy verifier failed pytest collection with `ModuleNotFoundError: No module named 'app_template'`.
  Evidence: final-copy pytest imported `scripts/prove_deployed_software.py`, which still imported `app_template.audit`.

- Observation: A legitimately bootstrapped project contains `.template-bootstrap-state.json`, making source-template bootstrap self-tests inapplicable; they attempted a second, conflicting bootstrap of their parent project.
  Evidence: the disposable copy's verifier reported two bootstrap-test failures before the test fixture gained its state-aware skip.

## Decision Log

- Decision: Retain the template's generic boundary and test bootstrap only in a disposable copy.
  Rationale: Bootstrap intentionally rewrites package and GitHub identity; running it in the source template would violate its reusable identity.
  Date/Author: 2026-10-04 / Codex

- Decision: Use the documented Docker workflow as the primary operational proof, with the existing local virtual environment only as a supporting diagnostic when Docker is unavailable.
  Rationale: `GETTING_STARTED.md` specifies Docker as the supported project dependency environment.
  Date/Author: 2026-10-04 / Codex

- Decision: Rewrite all Python modules beneath `src/app_template`, the deployment-proof script that imports the package, and the Compose command that invokes the distribution CLI.
  Rationale: These are the explicit executable references that must remain consistent after a bounded package/distribution rename. Container paths and generic configuration prefixes are intentionally not renamed.
  Date/Author: 2026-10-04 / Codex

- Decision: Skip bootstrap-self-tests only when their parent repository already has bootstrap state.
  Rationale: The tests prove transformation behavior in the unbootstrapped source template; a copied project should retain its canonical verifier after it has intentionally recorded its new identity.
  Date/Author: 2026-10-04 / Codex

## Outcomes & Retrospective

The supported source-template Docker workflow is operational: image build, locked sync, canonical verification, health, local SQLite self-test, and no-op demo all passed. The source verifier completed with 77 passed tests.

An isolated copy was personalized as `future-template-check`, package `future_template_check`, and GitHub target `example/future-template-check`. Bootstrap was idempotent for those exact values and rejected a conflicting second identity. The resulting copy generated a lockfile, completed a locked Docker sync, and passed `scripts/verify.py` with 73 passed and 4 expected skips. The skips are source-template-only bootstrap tests, explicitly inapplicable once state records the copied project's identity.

Three reproducible bootstrap gaps were corrected: nested package modules, the deployment-proof script and Compose CLI command now follow the selected identity, and bootstrap tests recognize a legitimate post-bootstrap repository. No optional pack, external integration, deployment, or source-template GitHub target was changed. Cleanup of the harness-owned temporary copies remains the final local step.

## Context and Orientation

`GETTING_STARTED.md` is the operator entry point. It requires WSL2, Docker Desktop integration, and a WSL-filesystem checkout, and prescribes `docker compose build`, a locked `uv` sync, `scripts/verify.py`, and three safe CLI commands. `scripts/verify.py` checks Ruff lint/format, pytest, and Markdown links.

`scripts/bootstrap_template.py` is the future-project boundary. It accepts explicit `--project-name`, `--package-name`, and `--github-repository` values, rejects invalid names, writes an ignored `.template-bootstrap-state.json`, and refuses conflicting re-bootstrap. It changes the source package directory and selected template-owned markers, so its real proof must use a disposable copy.

`compose.yaml`, `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, and `.github/workflows/ci.yml` define the local/CI development envelope. The template deliberately does not enable a deployed service, live agent runtime, credentials, or optional pack. `docs/template/OPTIONAL_PACKS.md` requires a separate ExecPlan for any such adoption.

The current configured GitHub target is `successbycs/template`; it must remain unchanged in this source template. The user has not authorized bootstrap of this source repository or changes to GitHub identity. The current WSLg setting is an external, temporary host workaround and is not copied into template configuration.

## Plan of Work

### Milestone 1: establish the documented baseline

Run Docker availability checks and the exact documented build, locked sync, canonical verifier, health, self-test, and no-op demo. Capture concise command results. If Docker is unavailable, record the specific prerequisite rather than substituting a host dependency installation; the existing `.venv` may run only supporting checks.

### Milestone 2: prove copied-project bootstrap safety

Create a temporary copy outside the repository, excluding `.git`, virtual environments, ignored state, and generated output. Run bootstrap with synthetic valid values such as `future-template-check`, `future_template_check`, and `example/future-template-check`. Verify the source package has been renamed in the copy, `pyproject.toml` contains the chosen project and GitHub target, the state file is created, and a conflicting second bootstrap exits with its documented error. Remove only the harness-owned temporary directory after recording the outcome.

### Milestone 3: close discovered readiness gaps

If Milestones 1–2 expose a reproducible mismatch among setup documentation, scripts, Docker, Dev Container, CI, or focused tests, make the smallest generic correction. Update the relevant docs and tests together. Do not introduce optional services, credentials, product requirements, or external operations.

### Milestone 4: durable verification and handoff

Run focused tests for modified code plus `scripts/verify.py` in the supported environment. Check Markdown links and `git diff --check`. Update this ExecPlan with actual commands, output summaries, remaining limits, and recovery notes before reporting completion.

## Concrete Steps

From `/home/chris/template`:

```bash
docker --version
docker compose version
docker compose build
docker compose run --rm app uv sync --locked --group dev
docker compose run --rm app uv run python scripts/verify.py
docker compose run --rm app uv run app-template health
docker compose run --rm app uv run app-template self-test
docker compose run --rm app uv run app-template demo --no-op
```

Expected result: Docker commands complete, verification prints `Verification: passed`, and the three CLI commands use no external service.

The actual temporary-copy proof used `/tmp/template-readiness-20261004`, `/tmp/template-readiness-regression-20261004`, and `/tmp/template-readiness-final-20261004`. The first two exposed the nested-import and script-import gaps; the final copy passed after the fixes. Only these exact harness-owned paths may be removed.

## Validation and Acceptance

| Boundary | Evidence required | Status |
| --- | --- | --- |
| Docker development environment | `docker compose build` and locked sync complete; Buildx used approved host fallback | Passed |
| Canonical template checks | Source `scripts/verify.py`: 77 passed; Ruff and Markdown links passed | Passed |
| Safe operator commands | `health`, `self-test`, and `demo --no-op` exited successfully without an external call | Passed |
| Copied-template personalization | Synthetic bootstrap was idempotent, rejected conflicting reuse, and final copied verifier passed 73 tests with 4 expected skips | Passed |
| Source-template preservation | Source still targets `successbycs/template`; no source bootstrap state was created | Passed |
| CI/Dev Container alignment | Compose/Dev Container/CI setup inspected; Compose executable command now follows bootstrap identity | Passed for local Docker; GitHub Actions remains unobserved |

## Idempotence and Recovery

Docker build/sync/verification and safe CLI commands are repeatable. The bootstrap test operates only in an explicit temporary directory; a failed test directory can be inspected and then removed by exact path. Never run bootstrap in `/home/chris/template`. If a Docker prerequisite is unavailable, do not install or reconfigure Docker without separate authority; record it as blocked.

## Artifacts and Notes

Durable results belong in this ExecPlan and any changed setup documentation/tests. Do not store Docker credentials, host configuration content, or temporary bootstrap state in the repository. Preserve the unrelated `.playwright-cli/` item.

## Interfaces and Dependencies

No new public interface is planned. Existing interfaces under verification are the Docker Compose `app` service, `app-template` CLI commands, `scripts/verify.py`, and `scripts/bootstrap_template.py` arguments: `--project-name`, `--package-name`, `--github-repository`, `--root`, and `--dry-run`.
