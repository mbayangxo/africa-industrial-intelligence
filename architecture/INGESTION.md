# Ingestion architecture

## Layers

1. **Quarantine:** bytes plus checksum and restricted metadata; no trust.
2. **Catalog:** completed intake record, rights/privacy review, deduplication.
3. **Extraction:** reproducible text/table/image observations with exact locators; retain raw values.
4. **Normalization:** taxonomies, units, currencies, dates, geography and entity resolution while preserving originals.
5. **Evidence:** reviewed source and atomic claim records; discrepancies linked.
6. **Publication:** approved views/API payloads, access policy, revision/retraction feed.

Each adapter emits a common manifest rather than domain conclusions. PDF/OCR, tabular, API, image, survey, supplier, regulatory, and founder-strategy adapters record software/version and transformations. Human review is mandatory for consequential extraction and classification.

Founder material is stored in its own intake category; extracted propositions use origin `founder` and `HYPOTHESIS`/`ASSUMPTION`. It cannot corroborate itself or satisfy external evidence gates.
