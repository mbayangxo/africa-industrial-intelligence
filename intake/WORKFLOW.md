# Intake and ingestion workflow

`inbox/` is a local quarantine and is ignored except for its README. Nothing in it is evidence merely because it was received.

1. **Receive safely:** malware-sensitive handling, checksum, original filename, timestamp, confidentiality, rights/consent; never overwrite the original.
2. **Identify:** what it is, creator/publisher, creation/publication/data dates, media type/version/language.
3. **Scope:** geography, sector, commodity, entities, units, and periods.
4. **Triage:** duplicate, legibility, personal/confidential data, permitted use, likely primary/secondary status, reliability notes.
5. **Extract reproducibly:** retain exact page/table/cell/image/API-query locators and transformations; OCR is unverified until checked.
6. **Register:** mint source record only after catalog review; extract atomic claims separately.
7. **Conflict check:** compare definitions/periods with existing claims and open a discrepancy rather than overwriting.
8. **Route:** approved archive, restricted store, review queue, or documented rejection. Git contains metadata only unless rights and policy allow otherwise.
9. **Review:** a second role checks material extraction before use in a promoted opportunity.

Adapters may later parse PDF, spreadsheet/CSV, API data, images/packaging, surveys, regulatory text, supplier documents, or founder strategy. All emit the same intake → source → claim contracts; automated extraction never upgrades reliability by itself.
