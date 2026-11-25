# RFCs

RFCs (Requests for Comments) are the project's mechanism for proposing, reviewing, accepting, and recording substantial design and process decisions.

This system is adapted from practices in [Kubernetes Enhancement Proposals](https://github.com/kubernetes/enhancements) and [Rust RFCs](https://rust-lang.github.io/rfcs/), sized for the **openxe** Python library.

## What an RFC is

An RFC answers: **What should we do and why?**

An RFC is a Markdown proposal that:

- States a problem and motivation.
- Defines goals and non-goals.
- Describes a design and alternatives.
- Records trade-offs, risks, and open questions.
- Has an explicit status controlled by human Maintainers.

Related document types (do not substitute for each other):

| Location | Question |
|----------|----------|
| **`RFCs/`** (this tree) | What should we do and why? |
| [`docs/research/`](../docs/research/README.md) | What have we learned and what should we consider? |
| Living docs | How do I use it / what is current contract? (`README.md`, later `docs/`) |

Prefer a research report under `docs/research/` when evidence and options are still open; promote a design choice into an RFC when Maintainers need a decision record.

> **Scope note:** openxe currently bootstraps **Research + RFCs** only. Full Agent Rules / `AGENTS.md` systems from sibling repos are **not** part of this tree unless a future Maintainer-accepted RFC adds them.

Routine bug fixes, small refactors, and documentation clarifications that do not change project meaning normally do **not** need an RFC.

## When an RFC is required

Propose an RFC when the change is substantial, including:

- Public API or entry-surface semantics (`OpenXE`, MCP, Capability).
- Architecture or layering changes (Runtime / Product / KnowledgeGraph contracts).
- Documentation governance or release policy changes.
- Breaking changes to documented behavior.
- Decisions that should remain as historical project record.

When unsure, ask a Maintainer. Prefer a short RFC over an undocumented irreversible decision.

## How to propose an RFC

1. Read [`process.md`](process.md).
2. Copy [`TEMPLATE.md`](TEMPLATE.md) to a new file in `RFCs/` using the naming pattern `RFC-<AREA>-<NNN>-short-title.md`.
3. Fill every applicable section. Leave unknowns marked as open questions.
4. Open a pull request (or equivalent review request) for Maintainer review.
5. Revise in response to feedback.

Do **not** assign `Accepted` status yourself. AI agents may draft and revise RFCs; only a human Maintainer may accept, reject, defer, or supersede them.

## How decisions are made

| Decision | Authority |
|----------|-----------|
| Draft, revise, analyze | Contributors and AI agents |
| Accept / Reject / Defer / Supersede | Human Maintainer only |
| Mark Implemented / Completed | Human Maintainer (after verifying implementation) |

A merged implementation PR does **not** by itself mean an RFC was accepted.

## Lifecycle overview

```text
Draft → In Review → Accepted → In Progress → Implemented
                 ↘ Rejected
                 ↘ Deferred
Accepted / Implemented → Superseded (via a newer RFC)
```

Details: [`process.md`](process.md).

## Directory layout

```text
RFCs/
├── README.md          # This file
├── TEMPLATE.md        # Authoring template
├── process.md         # Lifecycle and rules
├── accepted/          # Optional staging for accepted copies
├── rejected/
├── deferred/
├── superseded/
└── RFC-*.md           # Active and historical RFC documents
```

Until Maintainers adopt a filing convention, the **Status** field inside each RFC file is authoritative.

## Existing RFCs

| RFC | Title | Status |
|-----|-------|--------|
| [RFC-DOC-001](RFC-DOC-001-documentation-governance-bootstrap.md) | Documentation Governance Bootstrap (Research + RFCs) | Draft |
| [RFC-ARCH-001](RFC-ARCH-001-runtime-product-kg-layering.md) | Runtime / Product / KnowledgeGraph Layering | Draft |

Historical RFCs MUST NOT be silently rewritten to match newer templates. Amend via a new RFC or an explicit Maintainer-approved amendment note.
