# Prove upstream Symphony execution and restart

This ExecPlan is a living document and must be maintained under `.agent/PLANS.md`.

## Purpose / Big Picture

Prove that the configured upstream Symphony reference runtime can select one
deliberately eligible GitHub Issue, supply its context to Codex, make a small
reviewable code change in an isolated workspace, and expose the task through
its own dashboard. Then stop and restart only the Symphony process to document
the upstream in-memory recovery behaviour. This replaces assertions about the
old template scheduler with evidence from the chosen upstream runtime.

## Progress

- [x] (2026-10-04 04:10Z) Verify #39 is open, its dashboard proof passed, and #40 is now dependency-eligible.
- [x] (2026-10-04 04:10Z) Create dedicated child Issue #42 with the useful installer change, exact offline acceptance command, and the sole `symphony:ready` eligibility label.
- [x] (2026-10-04 04:18Z) Start upstream Symphony, observe #42 in its dashboard, and collect its isolated workspace result.
- [x] (2026-10-04 04:20Z) Verify the child diff and tests; preserve its review handoff without pushing, merging, or closing it.
- [x] (2026-10-04 04:24Z) Remove #42's temporary `symphony:ready` label with explicit human approval; confirm no eligible Issue remains.
- [x] (2026-10-04 04:30Z) After the owning session stopped the old process, start a fresh instance against the preserved workspace, observe its empty state, and stop the newly owned process.
- [x] (2026-10-04 04:26Z) Record durable current evidence and the remaining restart limitation in #40; leave it open for human review.

## Surprises & Discoveries

- Observation: Upstream Symphony v0.0.3 makes a deliberate `symphony:ready` queue gate practical: the verified #39 dashboard reported no active, blocked, or retrying sessions while no Issue carried that label.
  Evidence: `GET /api/v1/state` during #39 returned zero for all counts; #39 evidence comment `5976416984`.
- Observation: The first #42 attempt proved upstream dispatch and workspace creation, but Codex CLI `0.159.3` refused the configured `approval_policy.reject` variant before any agent turn.
  Evidence: the preserved upstream log reports `Invalid request: unknown variant reject, expected one of untrusted, on-request, granular, never`; the dashboard reported GH-42 retries and zero tokens.
- Observation: The successful worker workspace intentionally has no ignored `var/tools/` binary, so its initial `--check` invocation correctly exercised the missing-executable failure path.
  Evidence: `missing executable: .../workspaces-granular/GH-42/var/tools/symphony-v0.0.3-linux_x86_64`; after copying the already SHA-verified host binary as a local test fixture, the exact command returned `verified: v0.0.3 symphony-v0.0.3-linux_x86_64`.
- Observation: The repository-enforced GitHub safety control rejected removal of the temporary `symphony:ready` label without a new explicit user authorization.
  Evidence: 2026-10-04 `gh issue edit 42 --remove-label symphony:ready` was rejected before execution; the tool cited the repository workflow's label-mutation prohibition.
- Observation: A foreground upstream BEAM process remained bound to port 8765 after bounded `SIGINT` and `SIGTERM` observations; it was not force-killed. The owning terminal subsequently stopped it, enabling the clean recovery observation.
  Evidence: process `73973` continued listening on port 8765 during the first attempt; after the owner stopped it, fresh PID `92503` served `GET /api/v1/state` with empty state and closed its listener after `SIGTERM`.

## Decision Log

- Decision: The sole demonstration child Issue will add an offline `--check` mode to `scripts/install_upstream_symphony.sh`.
  Rationale: It is a useful, reviewable code change to the new upstream integration. The check can prove platform, pinned release metadata, and an already-installed binary's SHA-256 without network access, task dispatch, or a new custom scheduler.
  Date/Author: 2026-10-04 / Codex and repository owner.
- Decision: Only that child carries `symphony:ready` during the demonstration.
  Rationale: This proves real upstream selection while preventing unrelated Issue dispatch.
  Date/Author: 2026-10-04 / Codex and repository owner.
- Decision: A controlled service stop/restart occurs after the child has reached a stable stopped or completed state, never by restarting WSL or the host.
  Rationale: Upstream keeps blocked state in memory; host restart is unnecessary and would violate the bounded proof.
  Date/Author: 2026-10-04 / Codex and repository owner.
- Decision: The upstream workspace hook clones the committed local checkout by default for this local proof.
  Rationale: #39's integration commits are intentionally unpushed. A local Git clone brings the exact committed baseline to the isolated workspace while excluding uncommitted changes; the GitHub tracker remains the task source.
  Date/Author: 2026-10-04 / Codex.
- Decision: Use Codex's supported granular approval policy with every approval category set to `false`.
  Rationale: This preserves the intended upstream non-interactive rejection behaviour while matching the installed app-server's current schema; it does not broaden permissions or silently accept approvals.
  Date/Author: 2026-10-04 / Codex.

## Outcomes & Retrospective

Pending. #40 is complete only with a durable real scheduler-to-Codex-to-code-to-test evidence chain and a truthful upstream restart observation.

## Context and Orientation

`WORKFLOW.md` configures the official `openai/symphony` v0.0.3 GitHub adapter
for `successbycs/template`, the `symphony:ready` eligibility label, one worker,
an isolated ignored workspace root, and `codex app-server`. The pinned binary is
installed by `scripts/install_upstream_symphony.sh`; the foreground launcher is
`scripts/run_upstream_symphony_dashboard.sh`. Both require an explicit upstream
preview acknowledgement, and the launcher receives `GITHUB_TOKEN` only from its
environment.

The dedicated child will have one code packet, `scripts/install_upstream_symphony.sh`, and must run:

    scripts/install_upstream_symphony.sh --check

The intended `--check` output identifies v0.0.3 and the named asset after
validating Linux x86_64, prerequisite tools, the installed executable, and its
pinned SHA-256. It must fail non-zero if installation has not occurred or the
asset is modified. The child does not push, merge, deploy, create credentials,
or close an Issue.

The created child is [#42](https://github.com/successbycs/template/issues/42),
“Add offline verification mode to the upstream Symphony installer.” Its body
contains the exact code packet, acceptance command, and no-push/no-close
boundary. A GitHub queue inspection immediately before creation found no other
open `symphony:ready` Issue.

## Plan of Work

Create the child Issue with its scope, non-goals, exact code packet, acceptance
command, and `symphony:ready` label. Confirm no other open Issue has that label.
Run the upstream dashboard on a distinct loopback port, inspect both its HTML
and JSON state while the child is active, and allow only the configured one
worker to operate.

After Codex reaches a stable outcome, inspect the isolated workspace, diff, and
test output. The source checkout must remain unchanged by the worker. Record
the child review handoff and stop its scheduler. Restart the same pinned binary
against the same workflow and capture its state. Compare the preserved
workspace and tracker eligibility with the fact that blocked-session maps are
in memory. Do not claim exact session continuation.

The first attempt used `var/symphony-upstream/workspaces/GH-42` and is preserved
for diagnosis. The corrected retry will set `SYMPHONY_WORKSPACE_ROOT` to a new
ignored workspace directory rather than removing or overwriting that evidence.

The corrected run used
`var/symphony-upstream/workspaces-granular/GH-42`. The upstream dashboard on
port 8767 showed one and only one running task, `GH-42`, with an app-server PID,
real session IDs, GitHub tool calls, a 48-line diff, and completed turns. The
foreground service was stopped after the stable change, preserving both
workspaces. The task's first completed turn used 383,294 tokens; because the
GitHub Issue remained open, upstream began additional turns up to the configured
`max_turns`, so the service was stopped rather than allowed to repeat work.

The #42 eligibility label was removed with explicit human authorization before
the restart exercise, so no work could be selected again. The owning terminal
then stopped the pre-existing foreground listener on port 8765. A fresh process
against the same preserved workspace returned an empty upstream dashboard state
with no eligible Issue; it did not redispatch #42. The new process was stopped
and its listener closed. This evidences upstream's persisted workspace and
tracker-reconstructed state model without claiming exact session continuation.
Deferred #43 captures a future supervised host-service option, outside this
milestone, to provide explicit operator-owned status, restart, and logs without
creating a replacement scheduler.

## Concrete Steps

From `/home/chris/template`:

    gh issue create --repo successbycs/template ...
    gh issue edit <child> --repo successbycs/template --add-label symphony:ready
    SYMPHONY_DASHBOARD_PORT=8766 SYMPHONY_UNSAFE_PREVIEW_ACK="I understand" GITHUB_TOKEN="$(gh auth token)" scripts/run_upstream_symphony_dashboard.sh
    scripts/install_upstream_symphony.sh --check

Actual runtime logs, dashboard response, workspace path, revision, and test
transcript will be recorded here during execution.

## Validation and Acceptance

| Capability | Real proof | Result |
| --- | --- | --- |
| One deliberate task selection | Exactly one open child carries `symphony:ready`; upstream dashboard identifies only that task | Passed: GH-42 only |
| GitHub Issue context reaches Codex | Child workspace contains a worker-authored implementation tied to the child scope | Passed: 48-line installer diff |
| Code and test result | Child diff plus `scripts/install_upstream_symphony.sh --check` output | Passed: syntax, diff check, missing-path refusal, and fixture-backed success |
| Review handoff | Child Issue comment records diff, command, and no-push/no-close state | Passed; worker comments retained |
| Restart behaviour | Stop/restart transcript and state/workspace comparison | Passed: old process stopped by its owner; fresh process yielded empty state, preserved workspace, no redispatch, then clean listener closure |
| Scope audit | No unrelated issue session, label mutation, push, merge, deploy, or host restart | Passed: #42 eligibility removed with explicit user approval; no other scope expansion |

## Idempotence and Recovery

The child Issue is the one deliberate external write. Do not create a second
child if the first blocks. Stop the foreground service with `Ctrl-C` or its exact
PID. Preserve `var/symphony-upstream/` logs and workspace; do not delete them to
force recovery. If Codex requests an approval, fails, or an upstream restart
does not safely demonstrate behaviour, record that fact and leave #40 and the
child open for human review.

## Artifacts and Notes

Durable evidence belongs in this plan, the child Issue, and parent #40. No
credential, full transcript, downloaded binary, or ignored runtime log is
committed. The final source changes remain only in the isolated workspace until
a human chooses how to review or integrate them.

## Interfaces and Dependencies

- `scripts/install_upstream_symphony.sh --check`: proposed child-owned
  non-network validation command. It must return zero only for the exact pinned
  installed binary on supported Linux x86_64.
- GitHub child Issue: only temporary dispatch candidate, selected through
  upstream `tracker.required_labels`.
- Upstream `openai/symphony` v0.0.3: GitHub adapter, workspace manager, Codex
  app-server protocol, dashboard, and in-memory restart semantics.
