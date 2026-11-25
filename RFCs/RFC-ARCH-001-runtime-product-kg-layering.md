# RFC: Runtime / Product / KnowledgeGraph Layering

- **RFC ID:** RFC-ARCH-001
- **Title:** Runtime / Product / KnowledgeGraph Layering
- **Status:** Draft
- **Type:** Architecture
- **Authors:** AI coding agent (draft from root DESIGN/ENTRIES/FILE_LAYOUT/REQUIREMENTS); requires human Maintainer decision
- **Created:** 2026-11-25
- **Updated:** 2026-11-25
- **Supersedes:** N/A
- **Superseded by:** N/A

---

## 1. Summary

Freeze openxe’s product and package architecture as three layers — **Runtime** (pluggable DSPy Signature execution), **Product** (metadata-driven BI element extraction), and optional **KnowledgeGraph** (business-rule scoping of visible metadata) — exposed through three entries (library `OpenXE`, MCP, pydantic_ai Capability). This RFC records decisions previously scattered across root Markdown so Maintainers can accept or revise them as a single design.

## 2. Context and problem statement

Root documents already describe the same architecture from different angles:

| Source | Angle |
|--------|-------|
| `REQUIREMENTS.md` | Problem, F/N requirements, non-goals |
| `DESIGN.md` | Layer contracts |
| `ENTRIES.md` | Three entry surfaces |
| `FILE_LAYOUT.md` | Package tree and Excel sheet conventions |

Implementation under `src/openxe/` largely mirrors that layout, but the **Predict path is still a skeleton** (`pipeline/runner.py` raises `NotImplementedError` after Spec validation). Without an accepted RFC, “skeleton matches DESIGN” and “DESIGN is normative” remain ambiguous.

Supporting research:

- Disposition of root docs: [`docs/research/2026-11-25-root-docs-and-work-notes-disposition.md`](../docs/research/2026-11-25-root-docs-and-work-notes-disposition.md)
- Runtime evidence from LFX/DSPy demo: [`docs/research/supplementary/2026-11-25-dspy-lfx-runtime-reference.md`](../docs/research/supplementary/2026-11-25-dspy-lfx-runtime-reference.md)

## 3. Motivation

- One decision record for layering, entries, and file placement.
- Clear non-goals (no full NL2SQL product; Runtime must not encode BI slot names).
- Unblock completing Runner + normalize against an accepted contract.

Affected parties: library users, MCP/Capability integrators, contributors implementing Predict, Maintainers reviewing API surface.

## 4. Goals

1. **Product core:** natural language + BI metadata → structured BI elements (metrics / dimensions / filters; configurable key names, fixed semantic roles).
2. **Runtime mechanism:** pluggable `SignatureSpec` (code string primary, class secondary) → generic Predict → OutputField-only dict.
3. **Optional KnowledgeGraph:** file-backed business-rule graph scopes model-visible names via `apply_to_metadata`; does **not** replace full `BiMetadata`.
4. **Three entries** share one `OpenXE` / `BiExtractor` kernel; MCP and pydantic_ai remain optional extras.
5. Package layout under `src/openxe/` matches the layer split (`pipeline/`, `bi/`, `knowledge_graph/`, `mcp/`, `capability/`).

## 5. Non-goals

- Full NL2SQL generation, query execution, or GUI.
- Positioning the open-source product as an arbitrary NLP Signature runtime.
- Binding internal oneboard (or similar) Specs.
- KnowledgeGraph replacing `BiMetadata` full catalog; Note / BizGlossary entities inside KG.
- Dict/builder Signature sources in the first Accepted design (may be proposed later).
- Completing LM Predict wiring inside this RFC document (implementation follows acceptance).

## 6. Constraints and assumptions

- Stack: Python, uv, DSPy; KG tables via Polars (+ fastexcel as already depended).
- LM configuration is external / injectable.
- `CodeSignatureSpec` uses `exec` on caller-provided code — trust boundary is the caller.
- Skeleton code may already exist; acceptance legitimizes the **contract**, not a claim that Predict is done.

## 7. Proposed design

### 7.1 Layer diagram

```text
┌──────────────────────────────────────────────────────────┐
│ Product · BI element extraction (default public story)   │
│  OpenXE(metadata, knowledge_graph?=None, lm, …)          │
│  text → BiResult JSON {metrics, dimensions, filters, …}  │
│  BiMetadata = full catalog                               │
│  KnowledgeGraph? → effective_metadata = apply_to_metadata│
└────────────────────────────┬─────────────────────────────┘
                             │ assemble InputField kwargs
                             │ consume OutputField dict → normalize
┌────────────────────────────▼─────────────────────────────┐
│ Runtime · pluggable Signature runtime (domain-agnostic)  │
│  SignatureSpec.resolve() → type[dspy.Signature]          │
│  Runner(lm, state?) · Predict · OutputField-only dict    │
│  Optimize → state (optional extension)                   │
└──────────────────────────────────────────────────────────┘
```

### 7.2 Runtime contracts

**`SignatureSpec`** exposes `resolve()` / field maps; validation requires ≥1 InputField and ≥1 OutputField.

| Adapter | Ingress | Notes |
|---------|---------|-------|
| `CodeSignatureSpec` | Signature source as Python string | Primary; last public `dspy.Signature` subclass wins (demo-aligned) |
| `ClassSignatureSpec` | Concrete subclass | Secondary; avoid string round-trip |

**Runner:** `dspy.Predict(spec.resolve())`; pass InputField kwargs; optional `load_state`; return **only** OutputField keys. Runtime MUST NOT hard-code BI slot names or industry vocabulary.

**Optimize:** optional path producing state for Runner restore (may remain unimplemented after this RFC’s acceptance).

### 7.3 Product contracts

Default semantic slots (key names configurable via metadata):

| Role | Meaning | Typical shape |
|------|---------|---------------|
| metrics | what to measure | `list[str]` |
| dimensions | slice-by | `list[str]` (may be empty) |
| filters | constraints | `dict[str, str \| list[str]]` |

**Init sequence:**

1. Load full `BiMetadata`.
2. Optionally load `FileKnowledgeGraph`.
3. `effective = kg.apply_to_metadata(full) if kg else full`.
4. `BiExtractor` sees only effective catalog for prompting and normalize enums.

Default Signature is a BI-oriented template loaded via `CodeSignatureSpec`; advanced users may swap Spec if they still satisfy BI normalize (or own post-processing).

Facade: `OpenXE.extract(text) -> BiResult`.

### 7.4 KnowledgeGraph Excel (English sheets)

Entity sheets — columns `vid`, `name`, `description`:

`topics`, `vocabularies`, `measures`, `dimensions`

Relation sheets — columns `src_vid`, `dst_vid`:

`synonyms`, `hyponyms`, `represents`, `topic_measures`, `topic_dimensions`, `subtopics`

No Chinese sheet titles; no Note / BizGlossary.

### 7.5 Entry surfaces

| Entry | Package path | Dependency |
|-------|--------------|------------|
| Library | `openxe.api.OpenXE` (re-exported at package root) | default |
| MCP | `openxe.mcp` / `openxe-mcp` | extra `mcp` |
| pydantic_ai Capability | `openxe.capability` | extra `pydantic-ai` |

All construct or wrap the same kernel. MCP tool sketch: `extract_bi_elements(query) -> JSON`. Capability injects equivalent tools into an Agent.

### 7.6 Package layout (normative intent)

```text
src/openxe/
├── api.py                      # OpenXE facade
├── lm.py · exceptions.py
├── pipeline/                   # Runtime
│   ├── signature_spec.py · runner.py · optimize.py
│   └── adapters/code.py · klass.py
├── bi/                         # Product
│   ├── extractor.py · metadata.py · result.py
│   ├── normalize.py · default_signature.py
├── knowledge_graph/            # Optional scoping
│   ├── models.py · base.py · file_graph.py
├── mcp/                        # Entry #2
└── capability/                 # Entry #3
```

`main.py` at repo root remains transitional scaffolding; examples under `examples/` are the preferred demos.

### 7.7 Requirement traceability (from REQUIREMENTS)

| ID | Requirement | Design hook |
|----|-------------|-------------|
| F1–F3 | BI JSON extract; metadata-driven; swap catalog without Runtime change | Product + BiMetadata |
| F4 | Pluggable Signature + state/optimize extension points | Runtime Spec + Runner |
| F5–F7 | Default BI template; empty slots; minimal example | `default_signature` + examples |
| F8 | Optional KG scoping | `knowledge_graph` + OpenXE param |
| N1–N4 | uv/Polars; clear BI narrative; swappable LM; layered tests | Constraints §6 |

## 8. Alternatives considered

| Alternative | Summary | Why not chosen |
|-------------|---------|----------------|
| A. Runtime-as-product | Market as generic DSPy Signature host | Conflicts with BI-first open-source narrative |
| B. Single flat package | No pipeline/bi split | BI constants leak into Predict; harder testing |
| C. KG replaces BiMetadata | One graph for all catalog | Mixes full warehouse catalog with topic scoping |
| D. MCP-only distribution | Skip library facade | Weakens programmatic embedding; MCP stays optional |
| E. Three separate RFCs | DOC already separate; split ENTRIES/LAYOUT | Same decision surface; increases process overhead |

## 9. Trade-off analysis

- **Benefits:** Clear extension points; industry swap via metadata/KG; demo-proven code-string ingress.
- **Costs:** `exec` trust boundary; three optional surfaces to maintain; dual Spec adapters.
- **Harder:** Contributors must not “just add BI field names” inside `pipeline/`.

## 10. Compatibility and migration

- Public import `from openxe import OpenXE` remains the primary story.
- Optional extras stay optional.
- After acceptance: treat this RFC as decision SoT; update README wording if needed; root `DESIGN.md` / `ENTRIES.md` / `FILE_LAYOUT.md` follow `RFC-DOC-001` disposition.
- Rollback of *docs acceptance* does not require deleting skeleton code; code can diverge only with a superseding RFC.

## 11. Security and privacy

- `CodeSignatureSpec` executes caller-supplied Python — document as trusted-code ingress (same class of risk as demo).
- LM API keys stay in caller-provided LM config; library MUST NOT log secrets.
- Excel KG paths are local files; no remote fetch in the Accepted design.

## 12. Testing and validation

Existing / expected checks (do not invent missing harnesses):

- Unit tests under `tests/` for KG, API facade, MCP/Capability import guards, Spec adapters.
- After Predict lands: end-to-end example with real LM (manual or gated CI) — currently blocked by `NotImplementedError` in `run_predict`.
- Layering lint-by-review: no BI slot string constants under `pipeline/`.

## 13. Rollout and rollback

1. Maintainer Accepts this RFC (docs decision).
2. Implementors complete Runner Predict + normalize path against §7.
3. Mark `In Progress` / `Implemented` only after Maintainer verification.

Rollback of incomplete Predict work is independent of RFC status (feature simply remains skeleton).

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Accepting RFC while Predict unfinished | Readers assume product is complete | README + status honesty; §5 non-goal on wiring |
| Spec swap breaks BI normalize | Silent bad JSON | Document user responsibility; keep default template |
| Excel schema drift | Broken KG loads | Sheet/column table in §7.4 as contract |

## 15. Open questions

- [ ] Default Signature: multi-field outputs vs single JSON field then split in `normalize` — freeze which default?
- [ ] MCP/Capability: should KG path injection via env/CLI be required for `Implemented`, or follow-up API RFC?
- [ ] Confirm English identifier defaults (`metrics` / `dimensions` / `filters`) vs Chinese keys in examples — metadata-configurable either way; which README demo uses?

## 16. References

- Root transitional docs: `REQUIREMENTS.md`, `DESIGN.md`, `ENTRIES.md`, `FILE_LAYOUT.md`, `README.md`
- Code: `src/openxe/api.py`, `pipeline/`, `bi/`, `knowledge_graph/`, `mcp/`, `capability/`
- Research: disposition primary + DSPy/LFX supplementary (2026-11-25)
- Process: [`RFC-DOC-001`](RFC-DOC-001-documentation-governance-bootstrap.md), [`process.md`](process.md)
