# spaCy Docs Review

Reviewed sources:

- https://spacy.io/usage
- https://spacy.io/usage/models
- https://github.com/explosion/spaCy

Observed points:

- spaCy installation docs say spaCy is compatible with 64-bit CPython `3.7+` and available via `pip` and `conda`.
- The GitHub README narrows the current published support window to Python `>=3.7, <3.13` and recommends using a virtual environment to avoid modifying system state.
- The install docs recommend upgrading `pip`, `setuptools`, and `wheel` before install when using `pip`.
- The install docs recommend running `python -m spacy validate` to verify installed pipeline compatibility.
- The models docs state that trained pipelines are installed separately as Python packages.
- The models docs show `python -m spacy download en_core_web_sm` followed by `spacy.load("en_core_web_sm")` as the standard quickstart path.
- The models docs state that a blank pipeline is typically just a tokenizer and has no pretrained components.
- The models docs state that if lemmatization rules are available for the language, `spacy-lookups-data` or the `lookups` extra may be needed when using blank pipelines or languages without pretrained models.

Local implications for `dom0`:

- Host default Python `3.14.3` is outside the published `<3.13` README support window.
- A localized virtual environment was created at `/home/_404/src/dom0/.venv` using Python `3.12.12`.
- `spacy==3.8.11` is installed inside that localized environment.
- `python -m spacy validate` reports no installed pipeline packages in the current environment.

Boundaries for next analysis pass:

- Keep all inputs and outputs under `/home/_404/src/dom0`.
- Do not mutate `/home/_404/src/dom0/glossary.json`.
- Emit derived spaCy artifacts separately.
- Decide explicitly whether the analysis requires a trained English pipeline, a blank pipeline, or `spacy-lookups-data`.
