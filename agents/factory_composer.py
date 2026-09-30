#!/usr/bin/env python3
"""Factory Composer: assemble process, machines, utilities, QC and evidence gaps."""
from __future__ import annotations
CONFIGS=("minimum-viable-industrial","locally-optimized-scale-up","larger-industrial")
def compose(product,geography,target,process_template,machines,config):
    if config not in CONFIGS: raise ValueError("invalid configuration")
    byid={m["id"]:m for m in machines}; unknown=[]; steps=[]
    for i,s in enumerate(process_template,1):
        mids=s.get("machine_ids",[])
        for mid in mids:
            if mid not in byid: unknown.append(f"machine genome missing: {mid}")
            elif byid[mid].get("throughput",{}).get("value") is None: unknown.append(f"throughput unverified: {mid}")
        steps.append(dict(s,sequence=i))
    return {"product":product,"geography":geography,"configuration":config,"target_throughput":target,
      "process_steps":steps,"unknowns":sorted(set(unknown))}
def bottlenecks(factory,machines):
    byid={m["id"]:m for m in machines}; target=factory["target_throughput"].get("value"); out=[]
    if target is None:return [{"type":"unknown-target","severity":"blocking"}]
    for s in factory["process_steps"]:
        for mid in s.get("machine_ids",[]):
            m=byid.get(mid); cap=(m or {}).get("throughput",{}).get("value")
            if cap is None: out.append({"type":"unknown-capacity","machine_id":mid,"step":s["name"]})
            elif cap<target: out.append({"type":"capacity","machine_id":mid,"step":s["name"],"capacity":cap,"target":target})
    return out
def acquisition_tasks(factory):
    tasks=[]
    for u in factory.get("unknowns",[]):
        kind="engineering-verification" if "throughput" in u else "evidence-acquisition"
        tasks.append({"kind":kind,"question":u,"status":"queued"})
    cm=factory.get("cost_model",{})
    for x in ("capex","preopening","working_capital","cash_buffer"):
        if cm.get(x) is None: tasks.append({"kind":"cost-build","question":f"derive {x} bottom-up; do not insert benchmark lump sum","status":"queued"})
    return tasks
