#!/usr/bin/env python3
"""Opportunity Genome comparison and industrial-cluster discovery."""
from __future__ import annotations
FIELDS=("inputs","processes","capabilities","infrastructure","machinery","labor","distribution")
def overlap(a,b):
    shared={}; union=set()
    for f in FIELDS:
        x=set(a.get(f,[])); y=set(b.get(f,[])); z=x&y
        if z: shared[f]=sorted(z)
        union|={(f,v) for v in x|y}
    n=sum(len(v) for v in shared.values())
    return {"a":a["id"],"b":b["id"],"shared":shared,"shared_count":n,
            "similarity":round(n/max(1,len(union)),3)}
def coproduct_links(genomes):
    links=[]
    for a in genomes:
        produced=set(a.get("coproducts",[])+a.get("outputs",[]))
        for b in genomes:
            if a["id"]==b["id"]: continue
            common=produced & set(b.get("inputs",[]))
            if common: links.append({"from":a["id"],"to":b["id"],"materials":sorted(common),"status":"hypothesis-needs-quality-logistics-economics"})
    return links
def cluster_candidates(genomes,min_shared=2):
    pairs=[]
    for i,a in enumerate(genomes):
        for b in genomes[i+1:]:
            o=overlap(a,b)
            if o["shared_count"]>=min_shared: pairs.append(o)
    return sorted(pairs,key=lambda x:(x["shared_count"],x["similarity"]),reverse=True)
def shared_asset_hypotheses(genomes,min_opportunities=2):
    index={}
    for g in genomes:
        for f in ("capabilities","infrastructure","machinery","distribution"):
            for x in g.get(f,[]): index.setdefault((f,x),set()).add(g["id"])
    return [{"type":f,"asset_or_capability":x,"opportunity_ids":sorted(ids),"count":len(ids),
             "action":"test shared service/infrastructure economics"}
            for (f,x),ids in index.items() if len(ids)>=min_opportunities]
