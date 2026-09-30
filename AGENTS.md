# Repository instructions

This repository contains evidence-led industrial intelligence, not promotional copy.

* Never invent a datum, citation, interview, quotation, supplier, or result.
* Keep founder knowledge separate from external evidence and classify it as `HYPOTHESIS` or `ASSUMPTION` until verified.
* Put atomic claims in machine-readable records conforming to `schemas/claim.schema.json` and sources in records conforming to `schemas/source.schema.json`.
* Every `FACT` and `ESTIMATE` must cite at least one source ID. Record disagreements; never silently reconcile them.
* Do not place raw or sensitive intake material in Git. Preserve provenance and licensing metadata.
* Run `python3 scripts/validate.py` before committing intelligence records or schema changes.
* Research missions require explicit founder approval before execution. Mission folders currently contain scopes only.

