# Cloud Worker Handoff: spaCy Analysis

## Status

No `cloud_worker` executor is available in the current session. This file is the bounded handoff packet for external execution.

## Objective

Run a localized spaCy-based linguistic analysis over the `dom0` corpus and emit derived artifacts without mutating the raw glossary substrate.

## Trust Boundary

- Trust only `/home/_404/src/dom0`
- Do not read from sibling repos or external working trees
- Do not write outside `/home/_404/src/dom0`

## Inputs

- Raw glossary: `/home/_404/src/dom0/glossary.json`
- Corpus root: `/home/_404/src/dom0`
- Excludes:
  - `/home/_404/src/dom0/.git/**`
  - `/home/_404/src/dom0/artifacts/PLAN/**`
- Source roots:
  - `/home/_404/src/dom0/homeostasis`
  - `/home/_404/src/dom0/asset-control-model`

## Observed Local Environment

- Virtual environment: `/home/_404/src/dom0/.venv`
- Python: `3.12.12`
- spaCy: `3.8.11`
- Installed pipeline packages: none observed

Evidence:

- `/home/_404/src/dom0/artifacts/PLAN/evidence/spacy_installation_summary.txt`
- `/home/_404/src/dom0/artifacts/PLAN/evidence/spacy_runtime_info.txt`
- `/home/_404/src/dom0/artifacts/PLAN/evidence/spacy_validate.txt`
- `/home/_404/src/dom0/artifacts/PLAN/evidence/spacy_docs_review.md`

## Official Documentation Findings

- spaCy install guidance recommends a virtual environment.
- The GitHub README publishes Python support as `>=3.7, <3.13`.
- Trained pipelines are installed separately as Python packages.
- Blank pipelines are typically tokenizers only.
- Lemmatization support may require `spacy-lookups-data` or a trained pipeline, depending on the chosen path.

## Requested Analysis

1. Token layer
2. Lemma layer
3. KWIC layer
4. Collocation layer

## Required Output Boundary

Keep the raw glossary unchanged:

- `/home/_404/src/dom0/glossary.json`

Emit derived artifacts separately, preferably under:

- `/home/_404/src/dom0/SPACY_ANALYSIS/`

Suggested outputs:

- `tokens.json`
- `lemmas.json`
- `kwic.json`
- `collocations.json`
- `run_summary.md`

## Open Decisions

- Whether to install `en_core_web_sm`
- Whether to install `spacy-lookups-data`
- Whether a blank-pipeline path is sufficient for the target analysis quality

## Success Criteria

- Analysis runs entirely from the localized `dom0` environment
- Derived artifacts are separated from the raw glossary
- Pipeline choice and limitations are recorded explicitly
- All outputs remain inside `/home/_404/src/dom0`
