#!/usr/bin/env python3
"""Mission intelligence scorecard. Measures learning quality, not prose volume."""
def score(outputs:list[dict], tasks:list[dict])->dict:
    complete=[o for o in outputs if o.get("status")=="complete"]
    novelty=[o for o in complete if str(o.get("new_knowledge","")).strip()]
    blind=[o for o in complete if o.get("phase")=="blind-discovery"]
    independent=[o for o in blind if not o.get("founder_context_used") and not o.get("peer_discovery_used")]
    contradictions=sum(len(o.get("contradictions",[])) for o in outputs)
    disproof=sum(len(o.get("disproof_tests",[])) for o in outputs)
    return {
      "outputs_complete":len(complete),
      "novelty_rate":round(len(novelty)/len(complete),3) if complete else 0,
      "blind_outputs":len(blind),
      "blind_isolation_rate":round(len(independent)/len(blind),3) if blind else None,
      "contradictions_opened":contradictions,
      "disproof_tests":disproof,
      "evidence_gap_tasks":sum(t.get("kind")=="evidence-gap" for t in tasks),
      "fieldwork_tasks":sum(t.get("kind")=="fieldwork" for t in tasks),
      "supplier_quote_tasks":sum(t.get("kind")=="supplier-quote" for t in tasks),
      "handoff_tasks":sum(t.get("kind")=="handoff" for t in tasks),
      "warning":"This scorecard measures research-process health; it does not rank political choices or substitute for human investment decisions."
    }
