#!/usr/bin/env python3
"""Research-room scheduler: packet queues, handoffs, contradiction and fieldwork tasks."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def _id(prefix,*parts):
    return prefix+"-"+hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]

def derive_tasks(output:dict)->list[dict]:
    tasks=[]
    for h in output.get("handoffs",[]):
        q=h["question"]; tasks.append({"id":_id("task","handoff",output["packet_id"],h["to_role"],q),
          "kind":"handoff","to_role":h["to_role"],"question":q,"parent_packet_id":output["packet_id"],"status":"queued"})
    for c in output.get("contradictions",[]):
        tasks.append({"id":_id("task","contradiction",output["packet_id"],c),"kind":"contradiction",
          "to_role":"director","question":"Adjudicate with counterevidence: "+c,"parent_packet_id":output["packet_id"],"status":"queued"})
    for u in output.get("unknowns",[]):
        tasks.append({"id":_id("task","unknown",output["packet_id"],u),"kind":"evidence-gap",
          "to_role":"director","question":"Acquire evidence for: "+u,"parent_packet_id":output["packet_id"],"status":"queued"})
    return tasks

def fieldwork_task(question:str, geography:str, method:str, evidence_needed:str)->dict:
    return {"id":_id("field",question,geography,method),"kind":"fieldwork","question":question,
      "geography":geography,"method":method,"evidence_needed":evidence_needed,"status":"queued"}

def quote_task(item:str, specification:str, geography:str, quantity:str)->dict:
    return {"id":_id("quote",item,specification,geography,quantity),"kind":"supplier-quote",
      "item":item,"specification":specification,"geography":geography,"quantity":quantity,
      "required":["supplier identity","date","currency","tax","freight","lead time","warranty","payment terms"],"status":"queued"}

def save_queue(tasks:list[dict],path:Path):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(tasks,indent=2,ensure_ascii=False)+"\n")
