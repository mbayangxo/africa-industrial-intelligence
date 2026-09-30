#!/usr/bin/env python3
"""Dependency-free repository integrity checks; not a full JSON Schema engine."""
from __future__ import annotations
import json, re, sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {"FACT", "ESTIMATE", "ASSUMPTION", "SCENARIO", "HYPOTHESIS"}
RECORD_DIRS = {
    "sources": ROOT / "intelligence/sources",
    "claims": ROOT / "intelligence/claims",
    "relationships": ROOT / "intelligence/relationships",
    "opportunities": ROOT / "intelligence/opportunities",
    "discrepancies": ROOT / "evidence/discrepancies",
    "assumptions": ROOT / "evidence/assumption-register",
}
ID_PREFIX = {"sources":"src-", "claims":"clm-", "relationships":"rel-", "opportunities":"opp-", "discrepancies":"dsc-", "assumptions":"clm-"}

def display(path: Path) -> str:
    try: return str(path.relative_to(ROOT))
    except ValueError: return str(path)


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{display(path)}: invalid JSON: {exc}")
        return None


def valid_date(value: object) -> bool:
    if not isinstance(value, str): return False
    try: date.fromisoformat(value); return True
    except ValueError: return False


def resolve_pointer(document, pointer: str) -> bool:
    node = document
    if pointer == "#": return True
    if not pointer.startswith("#/"): return False
    try:
        for part in pointer[2:].split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
        return True
    except (KeyError, TypeError): return False


def validate_schema_refs(errors: list[str]):
    for path in sorted((ROOT / "schemas").glob("*.json")):
        doc = load_json(path, errors)
        if doc is None: continue
        def walk(node):
            if isinstance(node, dict):
                ref = node.get("$ref")
                if isinstance(ref, str):
                    if ref.startswith("#") and not resolve_pointer(doc, ref):
                        errors.append(f"{display(path)}: broken $ref {ref}")
                    elif not ref.startswith(("#", "https://", "http://")):
                        target = (path.parent / ref.split("#", 1)[0]).resolve()
                        if not target.is_file(): errors.append(f"{display(path)}: missing schema reference {ref}")
                for value in node.values(): walk(value)
            elif isinstance(node, list):
                for value in node: walk(value)
        walk(doc)


def load_records(errors: list[str]):
    records = {kind:{} for kind in RECORD_DIRS}
    for kind, directory in RECORD_DIRS.items():
        for path in sorted(directory.glob("*.json")):
            obj = load_json(path, errors)
            if not isinstance(obj, dict): continue
            rid = obj.get("id")
            if not isinstance(rid, str) or not rid.startswith(ID_PREFIX[kind]):
                errors.append(f"{display(path)}: missing/invalid id for {kind}"); continue
            if rid in records[kind] or (kind == "assumptions" and rid in records["claims"]):
                errors.append(f"{display(path)}: duplicate id {rid}")
            records[kind][rid] = (obj, path)
    return records


def validate_records(records, errors: list[str]):
    sources = records["sources"]
    claims = {**records["claims"], **records["assumptions"]}
    for cid, (claim, path) in claims.items():
        rel = display(path)
        classification = claim.get("classification")
        if classification not in CLASSES: errors.append(f"{rel}: invalid classification {classification!r}")
        if path.parent.name == "assumption-register" and classification != "ASSUMPTION": errors.append(f"{rel}: assumption register requires ASSUMPTION")
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list): errors.append(f"{rel}: source_ids must be an array"); source_ids=[]
        for sid in source_ids:
            if sid not in sources: errors.append(f"{rel}: unknown source id {sid}")
        if classification == "FACT" and not source_ids: errors.append(f"{rel}: FACT requires a source")
        if classification == "ESTIMATE":
            if not source_ids: errors.append(f"{rel}: ESTIMATE requires a source")
            if not str(claim.get("methodology", "")).strip(): errors.append(f"{rel}: ESTIMATE requires methodology")
        if claim.get("quantitative") is True and classification in {"FACT", "ESTIMATE"} and not source_ids:
            errors.append(f"{rel}: quantitative {classification} is unsupported")
        if classification in {"ASSUMPTION", "SCENARIO"} and claim.get("quantitative") is True and not str(claim.get("methodology", "")).strip():
            errors.append(f"{rel}: quantitative {classification} requires rationale/methodology")
        if not valid_date(claim.get("created_at")): errors.append(f"{rel}: created_at must be ISO date")
    for rid, (relrec, path) in records["relationships"].items():
        rel = display(path)
        if relrec.get("classification") not in CLASSES: errors.append(f"{rel}: invalid classification")
        sids = relrec.get("source_ids", [])
        for sid in sids:
            if sid not in sources: errors.append(f"{rel}: unknown source id {sid}")
        if relrec.get("classification") in {"FACT", "ESTIMATE"} and not sids: errors.append(f"{rel}: evidenced relationship requires source")
    for oid, (opp, path) in records["opportunities"].items():
        rel = display(path)
        for cid in opp.get("thesis_claim_ids", []):
            if cid not in claims: errors.append(f"{rel}: unknown claim id {cid}")
        if opp.get("stage") in {"validated"} and opp.get("red_team", {}).get("status") != "passed":
            errors.append(f"{rel}: validated opportunity requires passed red team")
    for did, (disc, path) in records["discrepancies"].items():
        for cid in disc.get("claim_ids", []):
            if cid not in claims: errors.append(f"{display(path)}: unknown claim id {cid}")


def validate_research_markdown(errors: list[str]):
    # Production narrative lives here. Templates/scopes are instructions, not claims.
    numeric = re.compile(r"(?<![A-Za-z])(?:[$€£]?\d[\d,.]*\s*(?:%|tonnes?|kg|km|MW|kWh|USD|XOF|CFA)\b|[$€£]\d)", re.I)
    marker = re.compile(r"<!--\s*(?:evidence|classification):", re.I)
    for path in (ROOT / "intelligence").rglob("*.md"):
        if path.name == "README.md": continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if numeric.search(line) and not marker.search(line):
                errors.append(f"{path.relative_to(ROOT)}:{number}: quantitative narrative lacks inline evidence/classification marker")


def validate_research_journals(errors: list[str]):
    """Validate the operational journal subset needed for reproducible handoffs."""
    allowed = {"search", "source-considered", "source-rejected", "evidence-gap", "contradiction", "hypothesis-revision", "unanswered-question", "handoff", "stop"}
    paths = list((ROOT / "missions").glob("*/research/**/*journal*.json"))
    paths += list((ROOT / "missions").glob("*/research/**/*JOURNAL*.json"))
    for path in sorted(set(paths)):
        journal = load_json(path, errors)
        if not isinstance(journal, dict): continue
        rel = display(path)
        if journal.get("schema_version") != "1.0.0": errors.append(f"{rel}: unsupported journal schema_version")
        if not re.fullmatch(r"mission-\d{3}", str(journal.get("mission_id", ""))): errors.append(f"{rel}: invalid mission_id")
        entries = journal.get("entries")
        if not isinstance(entries, list): errors.append(f"{rel}: entries must be an array"); continue
        seen = set()
        for index, entry in enumerate(entries):
            where = f"{rel}:entries[{index}]"
            if not isinstance(entry, dict): errors.append(f"{where}: entry must be an object"); continue
            eid = entry.get("id")
            if not isinstance(eid, str) or not re.fullmatch(r"jrnl-[a-z0-9-]+", eid): errors.append(f"{where}: invalid journal id")
            elif eid in seen: errors.append(f"{where}: duplicate journal id {eid}")
            seen.add(eid)
            if entry.get("activity") not in allowed: errors.append(f"{where}: invalid activity")
            if not str(entry.get("agent_role", "")).strip(): errors.append(f"{where}: agent_role is required")
            if not str(entry.get("outcome", "")).strip(): errors.append(f"{where}: outcome is required")
            timestamp = entry.get("timestamp")
            try: datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            except ValueError: errors.append(f"{where}: timestamp must be ISO date-time")


def run() -> list[str]:
    errors: list[str] = []
    validate_schema_refs(errors)
    records = load_records(errors)
    validate_records(records, errors)
    validate_research_markdown(errors)
    validate_research_journals(errors)
    return errors


if __name__ == "__main__":
    failures = run()
    if failures:
        print("Validation failed:")
        for failure in failures: print(f"- {failure}")
        sys.exit(1)
    count = sum(1 for d in RECORD_DIRS.values() for _ in d.glob("*.json"))
    print(f"Validation passed: schemas readable, references intact, {count} production record(s) checked.")
