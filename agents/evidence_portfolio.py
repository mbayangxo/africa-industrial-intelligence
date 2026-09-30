#!/usr/bin/env python3
"""Evidence portfolio checks: independence, source class, recency, and counter-search."""
from collections import Counter
REQUIRED_BY_DECISION={
 "market":["official-statistical","commercial-market"],
 "process":["technical-primary"],
 "safety":["regulator-standard","technical-primary"],
 "buildability":["commercial-quote","field-observation"],
}
def portfolio(sources:list[dict],decision_type:str)->dict:
    classes=Counter(s.get("source_class","unknown") for s in sources)
    publishers={s.get("publisher") for s in sources if s.get("publisher")}
    required=REQUIRED_BY_DECISION.get(decision_type,[])
    missing=[x for x in required if not classes[x]]
    return {"source_count":len(sources),"publisher_count":len(publishers),"classes":dict(classes),
            "missing_required_classes":missing,"passes":not missing and len(publishers)>=2}
def counter_search_query(thesis:str)->str:
    return f'Find credible evidence that contradicts, limits, or makes uneconomic this thesis: {thesis}'
def independence_warning(sources:list[dict])->list[str]:
    warnings=[]
    urls=[s.get("url","") for s in sources]
    domains=[u.split("/")[2].lower() if u.startswith("http") and len(u.split("/"))>2 else "" for u in urls]
    if domains and len(set(d for d in domains if d))==1: warnings.append("all web evidence comes from one domain")
    if len({s.get("publisher") for s in sources if s.get("publisher")})<2: warnings.append("fewer than two independent publishers")
    return warnings
