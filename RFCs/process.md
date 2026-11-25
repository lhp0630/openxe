# RFC Process

This document defines the RFC lifecycle for **openxe**.

Normative language: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**.

Adapted from the smtgit RFC process; sized for a small Python library. Agent Rules systems are **out of scope** unless a future RFC introduces them.

## 1. Purpose

Provide a lightweight, auditable path for substantial project decisions without introducing unnecessary bureaucracy.

## 2. Roles

| Role | Responsibilities |
|------|------------------|
| Author | Drafts and revises the RFC |
| Reviewer | Provides technical and editorial feedback |
| Maintainer | Accepts, rejects, defers, supersedes; owns final governance decisions |
| AI agent | MAY draft, analyze, and revise; MUST NOT independently accept or claim approval |

## 3. Statuses

| Status | Meaning |
|--------|---------|
| `Draft` | Work in progress; not ready for decision |
| `Proposed` / `In Review` | Submitted for Maintainer and community review |
| `Accepted` | Design approved; implementation may proceed |
| `Rejected` | Will not be pursued as proposed |
| `Deferred` | Not rejected; postponed until conditions change |
| `In Progress` | Accepted and actively being implemented |
| `Implemented` | Accepted design has been delivered and verified |
| `Superseded` | Replaced by a later RFC |

Notes:

- Early proposals MAY use `Proposed` as equivalent to `In Review`.
- Only a human Maintainer MAY change status to `Accepted`, `Rejected`, `Deferred`, `Implemented`, or `Superseded`.

## 4. Lifecycle

```text
Draft
  │
  ▼
In Review (Proposed)
  │
  ├──► Rejected
  │
  ├──► Deferred
  │
  ▼
Accepted
  │
  ▼
In Progress
  │
  ▼
Implemented
  │
  └──► Superseded (by a newer RFC)
```

### 4.1 Proposal

1. Author copies [`TEMPLATE.md`](TEMPLATE.md).
2. Author fills required sections with evidence-based claims.
3. Author sets status to `Draft`, then `Proposed` / `In Review` when ready.

### 4.2 Review

1. Reviewers comment on the proposal.
2. Author revises the RFC in place (prefer additive clarification).
3. Material design changes during review MUST be summarized in the PR or discussion thread.

### 4.3 Decision

A Maintainer records one of:

- **Accept** — status `Accepted`; optionally note implementation owners.
- **Reject** — status `Rejected`; record rationale.
- **Defer** — status `Deferred`; record conditions for revisit.

AI agents MUST NOT invent reviewers, consensus, or approval.

### 4.4 Implementation

1. After acceptance, implementation work MAY begin.
2. Status SHOULD move to `In Progress` when work starts.
3. Status becomes `Implemented` only after Maintainer verification that deliverables match the accepted design (or documented deviations are approved).

### 4.5 Supersession

Significant changes to an accepted decision SHOULD use a new RFC that:

- References the prior RFC.
- Explains what changes and why.
- Leaves the prior RFC intact with status `Superseded`.

Do not silently rewrite historical accepted RFCs.

## 5. When an RFC is not required

An RFC is usually unnecessary for:

- Typo and wording fixes that preserve meaning.
- Narrow bug fixes with no semantic change.
- Internal refactors that do not change documented contracts.
- Adding tests or examples that confirm existing behavior.

## 6. Numbering and naming

Recommended pattern:

```text
RFC-<AREA>-<NNN>-kebab-title.md
```

| Area | Use |
|------|-----|
| `DOC` | Documentation and governance |
| `ARCH` | Internal architecture / package contracts |
| `API` | Public library / entry-surface semantics |
| `SEC` | Security and safety policy |
| `REL` | Release and packaging |

`<NNN>` is a three-digit sequence within the area (for example `001`). Maintainers MAY adjust numbering if collisions arise.

## 7. Filing locations

- New and in-review RFCs live directly under `RFCs/`.
- Status directories (`accepted/`, `rejected/`, `deferred/`, `superseded/`) MAY hold stubs or relocated copies once Maintainers choose a filing convention.
- Until a filing convention is adopted, the **Status** field inside the RFC file is authoritative.

## 8. Relationship to pull requests

| Event | Does it accept the RFC? |
|-------|-------------------------|
| Opening a PR that contains an RFC | No |
| Merging an RFC document PR while status is still Proposed | No (unless Maintainer explicitly accepts in the merge decision) |
| Merging an implementation PR | No |
| Maintainer sets Status to Accepted | Yes |

## 9. Relationship to research reports

Prefer a research report under [`docs/research/`](../docs/research/README.md) when evidence and options are still open; promote a design choice into an RFC when Maintainers need a decision record.

Research reports MUST NOT mark an RFC Accepted.

## 10. Safety constraints

- MUST NOT mark an RFC `Accepted` without Maintainer authorization.
- MUST NOT claim community consensus that was not recorded.
- MUST NOT delete historical RFCs to “clean up” disagreement.
- MUST preserve license and attribution when quoting external material.

## 11. Related documents

- [`README.md`](README.md)
- [`TEMPLATE.md`](TEMPLATE.md)
- [`../docs/research/README.md`](../docs/research/README.md)
