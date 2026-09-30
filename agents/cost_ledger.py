#!/usr/bin/env python3
"""Bottom-up factory cost ledger; unknowns stay unknown."""
ALLOWED_BASIS={"supplier-quote","field-observation","invoice","official-tariff","evidenced-estimate","engineering-estimate","unknown"}
def validate_line(x):
    errors=[]
    if x.get("basis") not in ALLOWED_BASIS: errors.append("invalid cost basis")
    if x.get("amount") is not None and x.get("basis")=="unknown": errors.append("amount cannot be known with unknown basis")
    if x.get("amount") is not None and not x.get("currency"): errors.append("known amount requires currency")
    if x.get("basis") in {"supplier-quote","field-observation","invoice","official-tariff","evidenced-estimate"} and not x.get("evidence_ids"): errors.append("evidenced cost basis requires evidence")
    return errors
def summarize(lines):
    errors=[]; totals={}; unknown=[]
    for x in lines:
        errors += [f"{x.get('name','line')}: {e}" for e in validate_line(x)]
        if x.get("amount") is None: unknown.append(x.get("name")); continue
        key=(x.get("category"),x.get("currency")); totals[key]=totals.get(key,0)+x["amount"]
    return {"totals":[{"category":k[0],"currency":k[1],"amount":v} for k,v in sorted(totals.items())],
            "unknown_lines":unknown,"errors":errors,"complete":not unknown and not errors}
