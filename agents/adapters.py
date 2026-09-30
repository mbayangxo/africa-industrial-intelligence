#!/usr/bin/env python3
"""Provider-neutral execution contracts for AII research packets."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Any
from runtime import Packet, validate_output

class ResearchAdapter(Protocol):
    name: str
    def execute(self, packet: Packet, context: dict[str, Any]) -> dict[str, Any]: ...

@dataclass
class ExecutionResult:
    adapter:str; packet_id:str; status:str; output_path:str|None; errors:list[str]

def build_context(packet:Packet, evidence:dict[str,Any], founder_context:dict[str,Any]|None=None,
                  peer_outputs:list[dict]|None=None)->dict[str,Any]:
    """Enforce information boundaries before a provider ever sees context."""
    context={"mission_id":packet.mission_id,"phase":packet.phase,"role":packet.role,
             "question":packet.question,"acceptance_criteria":packet.acceptance_criteria,
             "evidence":evidence}
    if packet.phase!="blind-discovery":
        context["founder_context"]=founder_context or {}
        context["peer_outputs"]=peer_outputs or []
    else:
        context["blind_group"]=packet.blind_group
        context["withheld"]=packet.withheld_context
    return context

def execute_packet(adapter:ResearchAdapter, packet:Packet, context:dict[str,Any], run_dir:Path)->ExecutionResult:
    raw=adapter.execute(packet,context)
    raw.setdefault("packet_id",packet.id); raw.setdefault("mission_id",packet.mission_id)
    raw.setdefault("phase",packet.phase); raw.setdefault("role",packet.role)
    errors=validate_output(packet,raw)
    if errors: return ExecutionResult(adapter.name,packet.id,"rejected",None,errors)
    out=run_dir/"outputs"; out.mkdir(parents=True,exist_ok=True)
    path=out/f"{packet.id}--{adapter.name}.json"
    path.write_text(json.dumps(raw,indent=2,ensure_ascii=False)+"\n")
    return ExecutionResult(adapter.name,packet.id,"accepted",str(path),[])

def compare_outputs(outputs:list[dict[str,Any]])->dict[str,Any]:
    """Do not majority-vote facts; expose convergence/divergence for adjudication."""
    return {
      "outputs":len(outputs),
      "new_knowledge":[o.get("new_knowledge","") for o in outputs],
      "contradictions":[c for o in outputs for c in o.get("contradictions",[])],
      "handoffs":[h for o in outputs for h in o.get("handoffs",[])],
      "candidate_ids":sorted({c for o in outputs for c in o.get("candidate_ids",[])}),
      "requires_adjudication":len(outputs)>1
    }
