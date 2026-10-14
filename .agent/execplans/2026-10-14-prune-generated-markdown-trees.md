# Prune generated Markdown trees safely

This ExecPlan is a living document and must be maintained under `.agent/PLANS.md`.

## Purpose / Big Picture

Make Template V1's Markdown checker inspect authored Markdown in a repository
that contains nested Node and runtime projects, without reporting broken links
from generated dependencies or caches. A Template consumer can populate
`node_modules` and `var` and still run `uv run python scripts/verify.py`; a
broken authored link remains a failing quality gate.

## Progress

- [x] (2026-10-14) Inspected the checker and test conventions at `v1.0.0`.
- [x] (2026-10-14) Replaced recursive glob traversal with pruned deterministic traversal.
- [x] (2026-10-14) Added focused unit and command-boundary tests.
- [x] (2026-10-14) Ran the Template suite and preserved the review patch.
- [ ] Publish the reviewed upstream branch and create a release that PostSales can consume.

## Surprises & Discoveries

- Observation: The current `Path.rglob` checker only excludes `.git` and
  `.venv`, and checks absolute path components.
  Evidence: `scripts/check_markdown_links.py` at `v1.0.0`.

## Decision Log

- Decision: Prune exact directory names below the supplied root with top-down
  `os.walk`; do not use Git tracking as the authored-document boundary.
  Rationale: It ignores generated trees without hiding untracked authored docs
  or repositories under a parent called `var`.
  Date/Author: 2026-10-14 / Codex with user authorization.

## Outcomes & Retrospective

The candidate passes 5 focused tests and the complete Template verifier with
41 tests. It also passes against a disposable nested PostSales application
tree containing intentionally broken generated Markdown. Upstream publication
and a reviewed release remain pending; this does not yet change the imported
PostSales baseline.

## Context and Orientation

`scripts/check_markdown_links.py` finds `*.md`, checks repository-relative
links, prints `Broken Markdown links:` on failure, and exits one. The generic
fix must continue to check `.agent`, `.codex`, `apps`, and `docs`; it may prune
only `.git`, `.venv`, `node_modules`, and `var` at any depth.

## Plan of Work

Add `iter_markdown_files(root)` using `os.walk(root, topdown=True,
followlinks=False)`. Sort and prune directory names in-place, sort filenames,
and yield Markdown files. Extract `check_markdown_links(root)` to retain the
current parser, diagnostics, and exit behavior. Add
`tests/unit/test_check_markdown_links.py` using temporary directories and the
repository's importlib convention. Prove ignored invalid UTF-8 content is not
opened, all authored boundaries remain checked, exact-name matching is used,
and command behavior is deterministic. Run the full verifier.

## Concrete Steps

From this checkout:

    uv run pytest tests/unit/test_check_markdown_links.py
    uv run python scripts/verify.py
    git diff --check
    git diff -- scripts/check_markdown_links.py tests/unit/test_check_markdown_links.py

Completed result: all commands passed; `uv run python scripts/verify.py`
reported `Verification: passed`.

## Validation and Acceptance

Generated-only broken links exit zero. An authored broken link exits one and
identifies its repository-relative source. Valid, fragment, and external links
retain current behavior. The full Template verifier must pass.

## Idempotence and Recovery

The patch and tests are repeatable. `git restore --source=v1.0.0 --` limited to
the two changed files restores the candidate. No remote operation is included.

## Artifacts and Notes

The final diff and test output are copied to the PostSales ignored remediation
artifact directory for review.

## Interfaces and Dependencies

`iter_markdown_files(root: Path)` yields authored Markdown paths and
`check_markdown_links(root: Path)` returns unresolved links. They use Python
standard library traversal only; no dependency change is required.
