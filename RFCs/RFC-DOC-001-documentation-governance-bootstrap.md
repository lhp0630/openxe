# RFC: Documentation Governance Bootstrap (Research + RFCs)

- **RFC ID:** RFC-DOC-001
- **Title:** Documentation Governance Bootstrap (Research + RFCs)
- **Status:** Draft
- **Type:** Process / Documentation
- **Authors:** AI coding agent (draft); requires human Maintainer decision
- **Created:** 2026-11-25
- **Updated:** 2026-11-25
- **Supersedes:** N/A
- **Superseded by:** N/A

---

## 1. Summary

Adopt a minimal documentation governance system for openxe: **Research reports** under `docs/research/` and **RFCs** under `RFCs/`, with clear role separation from the product `README.md`. Explicitly **do not** import sibling-project Agent Rules (`.agents/rules/`, `AGENTS.md`) in this bootstrap. Dispose root planning Markdown by role (keep README; promote architecture decisions into RFCs; keep ephemeral `work/` notes out of Git).

## 2. Context and problem statement

Today the repository mixes product overview, requirements, architecture decisions, entry planning, and file-layout notes at the repo root (`README.md`, `REQUIREMENTS.md`, `DESIGN.md`, `ENTRIES.md`, `FILE_LAYOUT.md`). Local scratch lives under `work/` and is gitignored (`work/.gitignore` = `*`).

Without a triad:

- Design intent and implementation progress blur (for example README claims skeleton status while root docs still read like frozen specs).
- Valuable evidence in `work/dspy_lfx_demo.md` cannot enter Git unless distilled.
- There is no Maintainer-controlled path to accept or reject substantial decisions.

Evidence inventory and disposition recommendations: [`docs/research/2026-11-25-root-docs-and-work-notes-disposition.md`](../docs/research/2026-11-25-root-docs-and-work-notes-disposition.md).

External reference (not copied into this repo): smtgit `AGENTS.md` documentation governance table — Research / RFC / maintenance-report roles.

## 3. Motivation

- Contributors and agents need a stable place for pre-decision evidence vs decision records.
- Root Markdown sprawl should shrink to a product README plus (later) living `docs/`, with history preserved in RFCs/research.
- Maintainers retain exclusive authority over acceptance.

## 4. Goals

- Establish `docs/research/` layout: primary dated reports, `supplementary/`, `archive/`, and an index README.
- Establish `RFCs/` with `README.md`, `process.md`, `TEMPLATE.md`, and status stub directories.
- Codify the decision-document split: Research ≠ RFC acceptance ≠ living product docs.
- Record disposition rules for current root Markdown and `work/` notes.
- Keep bootstrap **docs-only** (no application code change required to accept this RFC).

## 5. Non-goals

- Importing or authoring `.agents/rules/`, `AGENTS.md`, or Cursor-specific rule packs in this RFC.
- Accepting architecture decisions (see `RFC-ARCH-001`; separate vote).
- Rewriting or deleting root Markdown in the same change set as acceptance without an explicit Maintainer disposition choice (§15).
- Creating Diátaxis Tutorial/How-to/Reference directory trees.
- Claiming English-only or Chinese-only as the sole project language in this RFC.

## 6. Constraints and assumptions

- Human Maintainers have final authority on status transitions (`RFCs/process.md`).
- AI agents MAY draft/revise; MUST NOT set status to `Accepted`.
- `work/` remains a local scratch area unless Maintainers change `.gitignore`.
- Sibling smtgit governance is **advisory** only.

## 7. Proposed design

### 7.1 Directory contracts

```text
docs/research/
├── README.md
├── YYYY-MM-DD-<topic>.md      # primary conclusions (flat + dated)
├── supplementary/
└── archive/

RFCs/
├── README.md
├── process.md
├── TEMPLATE.md
├── accepted/ | rejected/ | deferred/ | superseded/
└── RFC-<AREA>-<NNN>-*.md
```

### 7.2 Role rules (normative)

| Artifact | MUST answer | MUST NOT |
|----------|-------------|----------|
| Research report | What we learned / should consider | Mark RFC Accepted; act as sole public quick start |
| RFC | What we should do and why | Silent rewrite after Accepted; agent self-approval |
| `README.md` | Product orientation / quick start | Full architecture decision history; dump of research |

### 7.3 Root Markdown disposition (policy)

| File | Policy under this RFC |
|------|------------------------|
| `README.md` | Remains canonical product overview; Documentation links SHOULD point to `docs/research/` and `RFCs/` once this RFC is Accepted |
| `REQUIREMENTS.md` | Transitional living doc until Maintainer chooses archive or `docs/` summary; problem/goals already mirrored into `RFC-ARCH-001` |
| `DESIGN.md`, `ENTRIES.md`, `FILE_LAYOUT.md` | Decision content lives in `RFC-ARCH-001`; after that RFC is Accepted, Prefer single source of truth — do not dual-maintain conflicting trees |
| `work/*` | Not committed; distill into research/RFC only when information-valuable |

### 7.4 Initial seeded documents (already drafted with this proposal)

- Primary research: root docs + work disposition (2026-11-25)
- Supplementary: DSPy/LFX runtime reference (2026-11-25)
- `RFC-ARCH-001` Draft (architecture)

## 8. Alternatives considered

| Alternative | Summary | Why not chosen |
|-------------|---------|----------------|
| A. Full smtgit bootstrap (AGENTS + rules + maintenance reports) | Complete agent governance | User scope: Research + RFCs only; avoid unrelated Agent Rules |
| B. Keep only root Markdown forever | No process overhead | No acceptance authority; dual sources drift |
| C. Convert each root MD 1:1 into an RFC | Mechanical rename | Inflates RFC count; ENTRIES/FILE_LAYOUT are facets of one architecture decision |
| D. docs/ only, no RFCs | Living docs without decision log | Loses auditable accept/reject history |

## 9. Trade-off analysis

- **Benefits:** Clear places for evidence vs decisions; aligns with known open-source RFC practice; keeps scratch out of Git.
- **Costs:** Contributors must learn two new trees; temporary overlap with root planning docs until migration finishes.
- **Harder:** Casual “edit DESIGN.md only” without updating RFC after acceptance.

## 10. Compatibility and migration

- No Python API change.
- Documentation links in README SHOULD be updated when this RFC is Accepted.
- Rollback: remove or stop linking `docs/research/` and `RFCs/` if Rejected; root docs remain usable.

## 11. Security and privacy

- Docs-only; no new credential surfaces.
- Research MUST NOT paste secrets from local environments into Git.

## 12. Testing and validation

- Paths resolve: `docs/research/README.md`, `RFCs/README.md`, inventory tables list existing files.
- No RFC in-tree claims `Accepted` without Maintainer edit.
- `work/` still ignored by Git after bootstrap.

## 13. Rollout and rollback

- **Rollout:** Merge docs trees as Draft infrastructure; Maintainer sets this RFC to Accepted when process is approved.
- **Rollback:** Revert the docs commit(s); root Markdown unchanged in meaning.

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dual maintenance (root DESIGN vs RFC-ARCH) | Conflicting guidance | §7.3 + open question on post-accept disposition |
| Scope creep into Agent Rules | Unwanted process weight | Explicit non-goal |
| Research used as pseudo-acceptance | False authority | Index README forbids; process.md §9 |

## 15. Open questions

- [ ] After `RFC-ARCH-001` Accepted: delete, archive, or keep-as-non-normative the root `DESIGN.md` / `ENTRIES.md` / `FILE_LAYOUT.md` / `REQUIREMENTS.md`?
- [ ] Should a later RFC introduce `AGENTS.md` / agent rules, or permanently stay Research+RFC-only?
- [ ] Prefer Chinese, English, or bilingual for future RFCs? (Current drafts follow existing Chinese product docs + English RFC metadata.)

## 16. References

- [`docs/research/README.md`](../docs/research/README.md)
- [`docs/research/2026-11-25-root-docs-and-work-notes-disposition.md`](../docs/research/2026-11-25-root-docs-and-work-notes-disposition.md)
- [`RFC-ARCH-001`](RFC-ARCH-001-runtime-product-kg-layering.md)
- smtgit (external): documentation governance triad in `AGENTS.md`
