# Africa Industrial Intelligence

An evidence-led foundation for a living intelligence engine that identifies what should be built, processed, manufactured, financed, distributed, serviced, or improved across African economies. Senegal is the proving ground; West Africa and continental Africa follow. African demand is the base market, with exports as additional—not sole—demand.

## Current boundary

This repository contains **foundation only**: governance, schemas, templates, mission scopes, ingestion design, agent roles, validation, and future integration boundaries. It contains no completed mission findings, production observations, opportunity recommendations, frontend, or Kebu code. Mission folders may contain research plans, evidence-gap records, and blocked-attempt journals, but those are not substantive findings.

## Operating model

1. Place untrusted material in `intake/inbox/` (ignored by Git).
2. Register and triage it using `intake/intake-record.template.json` and `intake/WORKFLOW.md`.
3. Create immutable source metadata, then atomic claim records; preserve conflicts.
4. Build country, sector, commodity, process, infrastructure, and circular-economy views from those records.
5. Have the Skeptic challenge an opportunity before the Director promotes it.
6. Validate with `python3 scripts/validate.py`.

## Repository map

| Path | Purpose |
|---|---|
| `mission/` | North star, principles, success measures |
| `evidence/` | Research rules and governed registers |
| `schemas/` | Versioned JSON Schema contracts |
| `templates/` | Reusable research and decision documents |
| `agents/` | Specialist role contracts and orchestration |
| `intake/` | Quarantined intake design and triage template |
| `missions/` | Approved scopes for Missions 001–005; no findings |
| `architecture/` | Discovery, storage, database, and API proposals |
| `intelligence/` | Future validated source/claim/relationship records |
| `scripts/`, `tests/` | Dependency-free validation and tests |

## Status and next gate

Foundation and the Mission 001 public desk-research plan are approved. The first retrieval pass paused because public network access failed before evidence acquisition. External contact, quotations, paid data, and fieldwork remain unauthorized.
