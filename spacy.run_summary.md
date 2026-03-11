# spaCy run summary

## Input substrate
- Source glossary: `glossary.json`
- Input kind: `glossary.raw.v1`
- Source entries: `13`
- Raw strings: `4453`

## Scope
- Source paths are inherited from `glossary.raw.v1` and remain source-local.
- Existing glossary excludes were preserved from the raw glossary contract.

## Pipeline
- Mode: `blank_lookup`
- Pipes: `lemmatizer`
- Tokens/lemmas are derived from `sources[].raw_strings`, not from whitespace-splitting full files.
- KWIC targets the top non-stop lemmas by frequency.
- Collocations are adjacent non-stop alpha lemmas within a single raw glossary string.

## Limitations
- If `en_core_web_sm` is unavailable, the fallback pipeline has no POS tagger.
- Session-log transport fields remain part of the corpus when present in the raw glossary.
- This pass preserves duplicate raw strings because the input glossary preserves them.

## Artifacts
- `glossary.json`
- `glossary.spacy.tokens.json`
- `glossary.spacy.lemmas.json`
- `glossary.spacy.kwic.json`
- `glossary.spacy.collocations.json`
- `spacy.run_summary.md`
