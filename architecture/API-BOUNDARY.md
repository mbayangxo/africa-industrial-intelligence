# Future Kebu API boundary

Africa Industrial Intelligence remains an independent system of record. Kebu, OpportunityOS, Foundry, entrepreneurs, investors, universities/training systems, industrial planners, Jokko, Askaan, IAWIC, Maagal Cayor, and other authorized clients consume a versioned, read-oriented contract; they do not write directly to the intelligence database.

## Proposed boundary

`/v1/countries`, `/sectors`, `/commodities`, `/opportunities`, `/relationships`, `/infrastructure-gaps`, `/scenarios`, `/sources`, `/claims`, and `/discrepancies`. List endpoints support stable cursor pagination, filters, `as_of`, geography/taxonomy versions, and sparse fields. Responses include `id`, `schema_version`, `status`, `classification`, evidence links, freshness, and access/license flags. Opportunity responses expose red-team state and never hide unresolved disputes.

Writes use a separate authenticated contribution API (`/v1/submissions`) that creates intake items, not published records. Webhooks or an event feed announce reviewed revisions and retractions. Bulk, licensed exports support research use.

## Controls

OpenAPI is generated from approved schemas; OAuth/OIDC scopes, tenant/purpose controls, rate limits, audit logs, field-level redaction, signed artifact links, and explicit licensing apply. Public/internal/confidential tiers are enforced server-side. Idempotency keys protect submissions. Errors use machine-readable codes. Contract tests and deprecation windows protect clients.

## Non-goals now

No Kebu modification, endpoint implementation, authentication system, frontend, or production database is part of this foundation.
