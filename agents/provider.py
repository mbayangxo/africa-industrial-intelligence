#!/usr/bin/env python3
"""Provider boundary for live research execution.

Secrets never belong in Git. Concrete providers implement complete(packet, context)
outside the governed core and may use web/search/model APIs. The core validates
their structured return before persistence.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol,Any

class Provider(Protocol):
    name:str
    def complete(self, packet:dict[str,Any], context:dict[str,Any])->dict[str,Any]: ...

@dataclass
class ProviderPolicy:
    require_search:bool=True
    require_source_urls:bool=True
    min_sources:int=2
    max_unverified_quantitative_claims:int=0

def provider_prompt(packet,context):
    return {
      "system":("You are a bounded industrial-intelligence researcher. Search for evidence; "
                "do not invent facts, prices, yields, companies or citations. Distinguish fact, "
                "estimate, assumption, scenario and hypothesis. Prefer current authoritative/local "
                "sources for current conditions. State disagreement. Return structured output only."),
      "packet":packet,
      "context":context,
      "return_contract":{
        "new_knowledge":"specific findings not supplied in context",
        "claims":"atomic claims with classification, quantitative flag and evidence IDs",
        "sources":"title, publisher, URL, publication date, retrieval date, geography",
        "unknowns":"unresolved material questions",
        "contradictions":"source/agent disagreements",
        "handoffs":"role + precise question",
        "candidates":"opportunity hypotheses, if evidence created them",
        "disproof_tests":"what evidence would kill/revise the finding"
      }
    }

def quality_gate(raw:dict, policy=ProviderPolicy()):
    errors=[]
    sources=raw.get("sources",[])
    if policy.require_search and len(sources)<policy.min_sources: errors.append("insufficient source coverage")
    if policy.require_source_urls and any(not s.get("url") for s in sources): errors.append("source missing URL")
    for c in raw.get("claims",[]):
        if c.get("quantitative") and c.get("classification") in {"FACT","ESTIMATE"} and not c.get("evidence_ids"):
            errors.append("quantitative claim lacks evidence")
    if not str(raw.get("new_knowledge","")).strip(): errors.append("no new knowledge")
    return errors
