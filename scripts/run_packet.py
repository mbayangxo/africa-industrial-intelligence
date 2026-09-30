#!/usr/bin/env python3
"""Execute one research-room packet with a supplied provider and persist governed results."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).parents[1]; sys.path.insert(0,str(ROOT/"agents"))
from runtime import Packet
from adapters import build_context
from provider import provider_prompt,quality_gate
from scheduler import derive_tasks,save_queue
from run_ledger import append

def run(provider, packet:Packet, evidence:dict, run_id:str, founder_context=None, peer_outputs=None):
    run_dir=ROOT/"runs"/packet.mission_id/run_id
    ledger=run_dir/"events.jsonl"
    context=build_context(packet,evidence,founder_context,peer_outputs)
    append(ledger,run_id,"packet-started",packet.id,{"role":packet.role,"phase":packet.phase,"provider":provider.name})
    request=provider_prompt(packet.__dict__,context)
    raw=provider.complete(packet.__dict__,request)
    errors=quality_gate(raw)
    if errors:
        append(ledger,run_id,"output-rejected",packet.id,{"errors":errors})
        return {"status":"rejected","errors":errors}
    # normalize governed fields used by scheduler/runtime
    output={"packet_id":packet.id,"mission_id":packet.mission_id,"phase":packet.phase,"role":packet.role,
      "status":"complete","new_knowledge":raw["new_knowledge"],
      "claim_ids":[c.get("id") for c in raw.get("claims",[]) if c.get("id")],
      "source_ids":[s.get("id") for s in raw.get("sources",[]) if s.get("id")],
      "unknowns":raw.get("unknowns",[]),"contradictions":raw.get("contradictions",[]),
      "handoffs":raw.get("handoffs",[]),"candidate_ids":[c.get("id") for c in raw.get("candidates",[]) if c.get("id")],
      "disproof_tests":raw.get("disproof_tests",[]),
      "founder_context_used":packet.phase!="blind-discovery" and bool(founder_context),
      "peer_discovery_used":False}
    out=run_dir/"outputs"; out.mkdir(parents=True,exist_ok=True)
    (out/f"{packet.id}.json").write_text(json.dumps({"governed":output,"raw":raw},indent=2,ensure_ascii=False)+"\n")
    tasks=derive_tasks(output); save_queue(tasks,run_dir/"queues"/f"{packet.id}.json")
    append(ledger,run_id,"output-accepted",packet.id,{"new_knowledge":raw["new_knowledge"],"spawned_tasks":len(tasks)})
    return {"status":"accepted","output":output,"tasks":tasks}
