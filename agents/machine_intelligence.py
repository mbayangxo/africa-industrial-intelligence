#!/usr/bin/env python3
"""Machine intelligence: localization, recurrence, and build/buy/modify/shared-service evidence."""
from collections import defaultdict,Counter
LOCAL={"fabricate-local-now","source-local-now"}
PARTIAL={"assemble-local-import-components","local-after-training"}
def components(machine):
    for a in machine.get("assemblies",[]):
        for c in a.get("components",[]): yield a,c
def localization_profile(machine):
    cs=[c for _,c in components(machine)]; counts=Counter(c["localization_status"] for c in cs)
    critical_imports=[c["name"] for c in cs if c["criticality"] in {"high","safety-critical"} and c["localization_status"]=="import-required"]
    unknown=[c["name"] for c in cs if c["localization_status"]=="unknown"]
    return {"component_count":len(cs),"status_counts":dict(counts),
      "local_now_count":sum(counts[x] for x in LOCAL),"localizable_with_development_count":sum(counts[x] for x in PARTIAL),
      "critical_imports":critical_imports,"unknown_components":unknown,
      "warning":"Component counts are not cost/value/local-content percentages."}
def recurring_components(machines,min_machines=2):
    idx=defaultdict(lambda:{"machines":set(),"criticalities":set(),"statuses":set()})
    for m in machines:
        seen=set()
        for _,c in components(m):
            key=(c["category"],c["name"].strip().lower())
            if key in seen: continue
            seen.add(key); idx[key]["machines"].add(m["id"]); idx[key]["criticalities"].add(c["criticality"]); idx[key]["statuses"].add(c["localization_status"])
    return [{"category":k[0],"component":k[1],"machine_ids":sorted(v["machines"]),"machine_count":len(v["machines"]),
      "criticalities":sorted(v["criticalities"]),"localization_statuses":sorted(v["statuses"]),
      "action":"investigate standardization, pooled procurement, repair, or local production"}
      for k,v in idx.items() if len(v["machines"])>=min_machines]
def pathway_requirements(machine):
    p=localization_profile(machine)
    return {
      "buy-new-imported":["supplier quote","landed cost","support/spares","warranty","lead time","throughput/quality verification"],
      "buy-used":["inspection","remaining life","retrofit cost","spares","safety/food-contact remediation","landed cost"],
      "modify-existing":["baseline machine","required modifications","engineering verification","downtime","parts","performance test"],
      "fabricate-local":["drawings/specification","materials","process/tolerance capability","critical purchased components","prototype test","safety/food-contact validation"],
      "shared-service":["utilization demand","routing/logistics","changeover/cleaning","service pricing","downtime redundancy"],
      "profile":p}
def capability_gaps(machine,fabricators):
    available=set()
    for f in fabricators:
        for c in f.get("capabilities",[]):
            if c.get("status") in {"observed","sample-verified","production-verified"}: available.add(c["process"])
    needed=set()
    mapping={"structure":{"cutting","welding"},"food-contact":{"stainless-food-grade","surface-finishing"},"control":{"electrical-panel"},"sensor":{"sensor-integration"}}
    for _,c in components(machine): needed |= mapping.get(c["category"],set())
    return {"needed":sorted(needed),"verified_available":sorted(needed&available),"gaps":sorted(needed-available)}
