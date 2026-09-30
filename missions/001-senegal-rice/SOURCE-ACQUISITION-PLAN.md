# Mission 001 source-acquisition plan

**Status:** PLAN ONLY — no sources have been collected.

## Acquisition sequence

1. **Definitions and authoritative baseline:** identify Senegalese statistical, agricultural, trade/customs, water/irrigation, standards, port, and regulatory authorities; establish product/variety, paddy/milled, geography, crop/marketing-year, trade-code, unit, and conversion definitions.
2. **Independent international datasets:** identify relevant FAO, UN Comtrade, World Bank, regional, peer-reviewed, and other primary/authoritative series; preserve provider revisions and query parameters.
3. **Subnational and system records:** seek basin/region production, irrigation, processors, storage, transport, market price, loss, quality, and infrastructure evidence.
4. **Commercial and technical evidence:** only after outreach approval, request supplier specifications/quotations, machinery duty points, logistics tariffs, packaging data, laboratory requirements, and processor operating evidence.
5. **Field evidence:** only after fieldwork approval, collect interviews, observations, prices, photographs, samples, and tests under the approved protocol.
6. **Contradiction fill:** acquire sources specifically capable of resolving—or explaining—important disagreements and geographic/time gaps.

This sequence is prioritization, not a source list or a claim that any named institution holds a particular dataset.

## Source register requirements

Every acquired item receives an intake record before claim extraction: creator/publisher, title, version, publication and data dates, exact geography, commodity/product definition, language, source type and primary status, URL or protected locator, access date, rights, checksum, reliability notes, extraction method, precise page/table/cell/API-query/image locator, and claims supported. Machine downloads retain query, taxonomy/version, retrieval timestamp, and raw-to-normalized transformations.

## Evidence priorities

Prefer original administrative/statistical records, laws/standards, customs/trade data, transparent surveys, peer-reviewed primary research, original company filings, and original supplier specifications. Secondary analysis may locate or interpret primary evidence but does not inherit its authority. Material commercial conclusions seek independent triangulation and an authoritative source for important quantities when available. Scarce unique evidence is retained, clearly lowered in confidence, and assigned a verification task.

## Time and geography controls

Acquire the latest reliable baseline and seek at least ten years of comparable history where possible. Do not splice changed definitions without a documented bridge. Tag observations by subnational unit/basin/corridor/market and reference geography version. Date older contextual evidence prominently. Record missing years and coverage; never interpolate silently.

## Currency and price controls

Preserve stated XOF and every other original currency. A converted value links the original, FX source, applicable date/period and convention, calculation, and rounding. Label spot/period-average choice. Preserve nominal history; inflation-adjusted analysis records index source, base period, method, and labels results as real. Never overwrite nominal observations.

## Secure external-artifact strategy

Git stores public metadata, redacted provenance, checksums, permitted excerpts, and stable protected-artifact IDs—not restricted bytes.

* Use an approved encrypted object/document store with encryption in transit and at rest, role-based least privilege, MFA/SSO, access logs, backup/retention, and regional/legal review.
* Separate `public`, `internal`, `confidential-commercial`, and `restricted-personal-data` collections. Keep credentials in an approved secrets manager, never files or metadata.
* Name artifacts with opaque IDs; record checksum, owner, classification, rights, retention/deletion date, and access group in a restricted catalog. Git source records refer to opaque IDs and safe locators only.
* Store interview identity keys and consent forms separately from pseudonymized transcripts. Restrict recordings more tightly; publish no personal data without lawful basis and consent.
* Quotations and licensed documents retain use restrictions and expiration. Derived claims disclose the allowed level of detail and must not reconstruct protected content.
* Incident response, revocation, subject withdrawal, legal hold, and secure deletion procedures must be approved before field collection.

The platform/vendor, data controller, retention periods, and access-role assignments remain unresolved and block confidential collection.

## Acquisition acceptance check

A source is eligible for reviewed claims only when readable, in scope, provenance-linked, rights-reviewed, precisely locatable, and sufficiently understood to avoid definition/unit/date errors. OCR or automated extraction remains unverified until checked. Failure is logged; no weak source is silently upgraded.
