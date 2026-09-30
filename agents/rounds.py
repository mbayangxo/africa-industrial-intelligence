#!/usr/bin/env python3
"""Round controller for iterative multi-agent research."""
from __future__ import annotations
import hashlib
def rid(*p): return "rnd-"+hashlib.sha256("|".join(p).encode()).hexdigest()[:12]

ROUND_RULES={
  1:{"name":"parallel-evidence","goal":"Establish fresh evidence and independent findings without premature synthesis."},
  2:{"name":"cross-examination","goal":"Resolve contradictions, challenge weak claims, and execute specialist handoffs."},
  3:{"name":"buildability","goal":"Convert surviving candidates into engineering, cost, labor, distribution and marketing cases."},
  4:{"name":"red-team","goal":"Try to kill or materially revise candidates before human review."}
}
def unresolved(outputs):
    return [x for o in outputs for x in o.get("contradictions",[])+o.get("unknowns",[])]
def advance(round_no,outputs,tasks):
    if round_no==1 and not outputs: return {"advance":False,"reason":"no agent outputs"}
    if round_no==2 and unresolved(outputs): return {"advance":False,"reason":"unresolved contradictions/unknowns remain"}
    if round_no==3:
        needed={"supplier-quote","fieldwork"}
        present={t.get("kind") for t in tasks}
        if not needed.issubset(present): return {"advance":False,"reason":"buildability lacks fieldwork/quote acquisition"}
    return {"advance":round_no<4,"next_round":min(4,round_no+1)}
def cross_exam_questions(outputs):
    q=[]
    for o in outputs:
        for c in o.get("contradictions",[]): q.append({"target":"relevant-specialists","question":"Find counterevidence and reconcile: "+c})
        for u in o.get("unknowns",[]): q.append({"target":"relevant-specialists","question":"Can this be answered from evidence; if not generate field/quote task: "+u})
    return q
