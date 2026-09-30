# Evidence and research standard

## Claim classes

| Class | Meaning | Source requirement |
|---|---|---|
| `FACT` | Externally verifiable observation | One or more traceable sources; triangulate material claims |
| `ESTIMATE` | Derived or reported approximation | Sources plus method, inputs, range/uncertainty |
| `ASSUMPTION` | Explicit input accepted for analysis | Owner, rationale, review date; cite if externally informed |
| `SCENARIO` | Deliberately chosen what-if case | Parameters and purpose; never present as forecast |
| `HYPOTHESIS` | Testable proposition | Test and falsification criteria; evidence optional until tested |

Founder statements enter as `HYPOTHESIS` or `ASSUMPTION`, with `origin.kind = founder`, never as facts merely because of authorship.

## Atomic evidence workflow

1. Define the question, geography, period, units, and terms before collection.
2. Prefer original statistical agencies, ministries, customs/trade systems, FAO, World Bank, UN Comtrade, ECOWAS/AfCFTA bodies, standards bodies, peer-reviewed work, company filings, and original supplier specifications.
3. Register source identity, publisher, dates, geography, industries/commodities, source type, primary status, access path, reliability, licensing, and exact locator.
4. Create one independently assessable claim per claim record. Preserve reported units and currency; put transformations in methodology.
5. Use source locators (page, table, sheet/cell, API query/version, image ID). A URL alone is insufficient when a precise locator exists.
6. Record contradictions as discrepancy records linking all claim IDs. Do not average or select silently.
7. Separate collection, interpretation, modeling, red-team review, and decision.

## Quantitative claims

Every quantitative `FACT` or `ESTIMATE` requires at least one source ID. Estimates additionally require a method. Record observation year separately from publication/access dates, currency and price year, units and conversion steps, geographic scope, definitions, and uncertainty. Tables must trace each row or clearly declare a shared source and scope.

## Reliability

Reliability is structured judgment, not truth: `high`, `medium`, `low`, or `unrated`, with notes. Consider authority, method transparency, independence, coverage, recency, reproducibility, and incentives. Secondary summaries do not inherit the authority of sources they mention.

## Conflicts and corrections

Create a discrepancy record describing definition, period, method, or unknown cause. Retain competing claims. Resolutions require rationale and reviewer. Corrections supersede rather than erase records, leaving an audit trail.

## Ethical and legal handling

Capture consent and permitted use for interviews/images; minimize personal data; restrict confidential quotations and commercial material; record licenses; never commit inbox originals, secrets, or personal data without authorization.

