# Future database proposal

## Approach

Begin with versioned JSON records in Git. Move validated records to PostgreSQL when collaboration/query volume requires it; use relational integrity and recursive queries before adding a graph database. Store large licensed artifacts in object storage by checksum, not in relational rows or Git. Maintain schema versions and immutable audit events.

## Logical entities

`source`, `source_locator`, `claim`, `claim_source`, `discrepancy`, `geography`, `organization`, `sector`, `commodity`, `product`, `process`, `facility`, `infrastructure_asset`, `machine`, `supplier`, `standard`, `trade_flow`, `observation`, `relationship`, `opportunity`, `opportunity_claim`, `scenario`, `scenario_input`, `mission`, `agent_run`, `review`, `decision`, and `audit_event`.

Critical relations are many-to-many and effective-dated. Quantities use value/range, unit, period, geography, method, source, currency, and price year. Ownership is effective-dated and supports beneficial-ownership uncertainty. Taxonomies retain external codes (ISO, HS, CPC, ISIC) and versions alongside internal stable IDs.

## Integrity and lifecycle

* Immutable source/claim IDs; corrections create revisions/supersession links.
* Foreign keys for every citation and graph endpoint; uniqueness on versioned external identifiers.
* Classification constraints; factual/estimated quantitative claims require citations, and estimates require methodology.
* Opportunity promotion requires completed red-team review.
* Row-level access for confidential material and separate personal-data store.
* Raw → normalized → reviewed → published layers; reproducible transformations and lineage.
* Backups, retention/licensing controls, observability, migrations, and exportable open formats prevent lock-in.

## Query layer

Materialized views can serve country/sector/commodity profiles, trade leakage, unresolved discrepancies, shared infrastructure, circular paths/loops, scenario inputs, and evidence coverage. Full-text/vector search may aid discovery but never replace source links or authorization filters.
