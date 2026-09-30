#!/usr/bin/env python3
"""Append-only run ledger for reproducibility and audit."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path

def event_id(run_id,event_type,packet_id,sequence):
    return "evt-"+hashlib.sha256(f"{run_id}|{event_type}|{packet_id}|{sequence}".encode()).hexdigest()[:12]

def append(path:Path,run_id:str,event_type:str,packet_id:str,payload:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    seq=0
    if path.exists():
        with path.open() as f: seq=sum(1 for _ in f)
    event={"id":event_id(run_id,event_type,packet_id,seq),"run_id":run_id,"sequence":seq,
      "timestamp":datetime.now(timezone.utc).isoformat(),"event_type":event_type,"packet_id":packet_id,"payload":payload}
    with path.open("a") as f: f.write(json.dumps(event,ensure_ascii=False)+"\n")
    return event
