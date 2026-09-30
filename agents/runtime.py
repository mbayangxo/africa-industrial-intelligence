#!/usr/bin/env python3
"""Africa Industrial Intelligence multi-agent research-room runtime.

Dependency-free orchestration state machine. It does not call a model/provider itself:
adapters execute packets and return structured outputs. This keeps evidence/governance
portable across model vendors and allows human/field researchers to participate.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, asdict
from pathlib import Path

ROLES = [
"director","agriculture-value-chain","trade-market","consumer-intelligence",
"industrial-engineer","machinery-local-fabrication","economic-financial-modeler",
"circular-zero-waste","livestock-animal-nutrition","brand-packaging",
"infrastructure","standards-certification","independent-discovery","skeptic-red-team"
]
SPECIALISTS=[r for r in ROLES if r not in {"director","independent-discovery","skeptic-red-team"}]
PHASES=["frame","specialist-research","blind-discovery","cross-examination","synthesis","red-team","human-decision"]
REQUIRED_OUTPUT=["new_knowledge","claim_ids","source_ids","unknowns","contradictions","handoffs","candidate_ids","disproof_tests"]

def stable_id(prefix: str, *parts: str) -> str:
    digest=hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]
    return f"{prefix}-{digest}"

@dataclass(frozen=True)
class Packet:
    id:str; mission_id:str; phase:str; role:str; question:str
    acceptance_criteria:list[str]; allowed_context:list[str]; withheld_context:list[str]
    blind_group:str|None=None

def make_packet(mission_id, phase, role, question, acceptance, allowed=None, withheld=None, blind_group=None):
    return Packet(stable_id("pkt",mission_id,phase,role,question),mission_id,phase,role,question,
                  acceptance,allowed or [],withheld or [],blind_group)

def mission_packets(mission_id:str, question:str)->list[Packet]:
    common=["Return atomic claim/source IDs; separate FACT/ESTIMATE/ASSUMPTION/SCENARIO/HYPOTHESIS.",
            "State what is newly learned, what remains unknown, contradictions, handoffs and falsification tests.",
            "Do not manufacture numbers. Current decisions require latest available evidence plus historical context."]
    packets=[]
    role_questions={
      "agriculture-value-chain":"Map feedstock reality, seasons, geography, producers, aggregation, post-harvest losses and capturable supply.",
      "trade-market":"Reconcile current and historical trade, prices, competitors, channels, policy shocks and money/value leakage.",
      "consumer-intelligence":"Find observed buying/use behavior, segments, pack/price/channel choices, complaints and field tests still required.",
      "industrial-engineer":"Build process/material/energy balances and throughput cases; identify bottlenecks before proposing capacity.",
      "machinery-local-fabrication":"Decompose every machine into functions/components and test modify/fabricate/assemble/share before full import.",
      "economic-financial-modeler":"Build bottom-up capex, working capital, labor, utilization, unit economics, downside and scale triggers from evidenced inputs.",
      "circular-zero-waste":"Trace every material stream to safe evidenced uses/buyers; find cross-industry loops and reject fake waste-value claims.",
      "livestock-animal-nutrition":"Test feed/co-product uses by species/stage, nutrient specification, safety, formulation limits and delivered economics.",
      "brand-packaging":"Test product, pack, trust, retail execution, marketing channels, creator/merchant activation and repeat-demand evidence.",
      "infrastructure":"Find shared constraints/assets in power, heat, water, storage, logistics, labs and processing that unlock multiple businesses.",
      "standards-certification":"Map current food/feed/labor/environment/label/export requirements, testing and unresolved compliance questions."
    }
    for role,q in role_questions.items():
        packets.append(make_packet(mission_id,"specialist-research",role,q,common+[question]))
    # Three isolated discovery rooms; founder ideas/brand/candidate list are explicitly withheld.
    for i in range(1,4):
        packets.append(make_packet(mission_id,"blind-discovery","independent-discovery",
          "Independently discover high-value buildable businesses and enabling infrastructure from evidence; do not optimize for known founder ideas.",
          common+["At least one candidate must arise from observed evidence rather than a supplied product idea.",
                  "Include customer, pain, evidence, dependency, first test, why-not-build and kill criteria."],
          allowed=["mission geography","public evidence","validated claim/source records"],
          withheld=["founder candidate list","founder brands","other discovery-agent outputs","provisional opportunity rankings"],
          blind_group=f"blind-{i}"))
    return packets

def validate_output(packet:Packet, output:dict)->list[str]:
    errors=[]
    for key in REQUIRED_OUTPUT:
        if key not in output: errors.append(f"{packet.id}: missing {key}")
    if not str(output.get("new_knowledge","")).strip(): errors.append(f"{packet.id}: new_knowledge cannot be empty")
    if packet.phase=="blind-discovery" and output.get("founder_context_used"):
        errors.append(f"{packet.id}: blinded discovery used founder context")
    if packet.phase=="blind-discovery" and output.get("peer_discovery_used"):
        errors.append(f"{packet.id}: blinded discovery used peer discovery output")
    return errors

def coverage(outputs:list[dict])->dict:
    completed={o.get("role") for o in outputs if o.get("status")=="complete"}
    missing=[r for r in SPECIALISTS if r not in completed]
    novelty=[o for o in outputs if str(o.get("new_knowledge","")).strip()]
    contradictions=sum(len(o.get("contradictions",[])) for o in outputs)
    return {"specialists_complete":len(SPECIALISTS)-len(missing),"specialists_required":len(SPECIALISTS),
            "missing_specialists":missing,"outputs_with_new_knowledge":len(novelty),
            "contradictions_opened":contradictions}

def next_phase(current:str, outputs:list[dict])->str:
    if current=="specialist-research" and coverage(outputs)["missing_specialists"]: return current
    idx=PHASES.index(current)
    return PHASES[min(idx+1,len(PHASES)-1)]

def write_packets(root:Path, mission_id:str, question:str):
    out=root/"runs"/mission_id/"packets"; out.mkdir(parents=True,exist_ok=True)
    packets=mission_packets(mission_id,question)
    for p in packets: (out/f"{p.id}.json").write_text(json.dumps(asdict(p),indent=2)+"\n")
    manifest={"mission_id":mission_id,"phase":"specialist-research","packet_ids":[p.id for p in packets],
              "rule":"Outputs are evidence-bearing work products, not prose completion. Empty novelty fails."}
    (out.parent/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return packets
