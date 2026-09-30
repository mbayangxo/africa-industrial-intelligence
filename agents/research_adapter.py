#!/usr/bin/env python3
"""Research-capable adapter primitives: search plan, evidence ledger, freshness and provenance."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

def sid(prefix,*parts): return prefix+"-"+hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]

@dataclass(frozen=True)
class SearchRequest:
    id:str; packet_id:str; query:str; source_class:str; freshness:str; geography:str; reason:str

def request(packet_id,query,source_class="authoritative",freshness="latest",geography="Senegal",reason=""):
    return SearchRequest(sid("search",packet_id,query,source_class,freshness),packet_id,query,source_class,freshness,geography,reason)

def default_search_plan(packet)->list[SearchRequest]:
    role=packet.role
    q={
      "agriculture-value-chain":["Senegal groundnut sesame production 2025 2026 region yield campaign","Senegal groundnut commercialization collection 2025 2026 processors"],
      "trade-market":["Senegal groundnut sesame oils meal imports exports 2025 2026 ANSD customs","Senegal edible oil prices market 2025 2026"],
      "consumer-intelligence":["Senegal household edible oil consumption pack sizes retail 2025 2026","Senegal cooking oil brands prices boutiques markets"],
      "industrial-engineer":["groundnut sesame mechanical pressing mass balance extraction yield technical","Senegal oilseed processing capacity SONACOS COPEOL SSII"],
      "machinery-local-fabrication":["Senegal SISMAR groundnut cleaner tarare sheller oil press fabrication","ITA Senegal sesame press equipment"],
      "economic-financial-modeler":["Senegal industrial electricity tariff wages transport packaging 2025 2026","Senegal groundnut producer price sesame price 2025 2026"],
      "circular-zero-waste":["groundnut shells cake Senegal buyers biomass feed uses","sesame meal cake composition uses Senegal"],
      "livestock-animal-nutrition":["Senegal feed mills soybean meal groundnut cake sesame meal specification price","groundnut cake aflatoxin livestock feed limits Senegal ECOWAS"],
      "brand-packaging":["Senegal edible oil packaging 1L 5L sachet prices brands 2025 2026","Senegal social media food creators retail marketing"],
      "infrastructure":["Senegal groundnut storage warehouses electricity industrial zones labs 2025 2026","Senegal oilseed logistics collection points processing constraints"],
      "standards-certification":["Senegal ECOWAS groundnut aflatoxin edible oil standards labeling 2025 2026","Senegal food processing permits oil feed standards ASN ITA"]
    }.get(role,[packet.question])
    return [request(packet.id,x,reason=f"Evidence for {role}") for x in q]

def evidence_item(packet_id,url,title,published,retrieved,claim_supported,source_class,geography):
    return {"id":sid("ev",packet_id,url,claim_supported),"packet_id":packet_id,"url":url,"title":title,
      "published":published,"retrieved":retrieved,"claim_supported":claim_supported,
      "source_class":source_class,"geography":geography}

def freshness_flag(item,decision_year=2026):
    p=item.get("published") or ""
    try: year=int(p[:4])
    except Exception: return "unknown-date"
    if year>=decision_year: return "current"
    if year==decision_year-1: return "recent"
    return "historical-context"

def save_ledger(items,path:Path):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload={"retrieved_on":date.today().isoformat(),"items":[dict(x,freshness=freshness_flag(x)) for x in items]}
    path.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n")
