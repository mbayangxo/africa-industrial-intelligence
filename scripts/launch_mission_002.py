#!/usr/bin/env python3
"""Materialize a mission research room into executable packets and initial queues."""
from pathlib import Path
import sys
ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/"agents"))
from runtime import write_packets
from scheduler import fieldwork_task, quote_task, save_queue

MISSION="mission-002"
QUESTION=("Across Senegal's nuts, oilseeds, edible oils and connected co-products, "
          "what businesses, infrastructure and locally buildable capabilities should be tested, "
          "using current 2024-2026 evidence, whole-system economics and independent discovery?")

def launch(root:Path=ROOT):
    packets=write_packets(root,MISSION,QUESTION)
    tasks=[
      quote_task("groundnut cleaner/screen","throughput, motor, screen area, materials, local-content BOM","Senegal","1 unit"),
      quote_task("tarares/aspirator","throughput, fan/motor, screens, dust handling, materials","Senegal","1 unit"),
      quote_task("small screw oil press","food-grade, continuous throughput, motor, wear parts","Senegal","1 unit"),
      quote_task("sesame press","food-grade, throughput, yield basis, motor, wear parts","Senegal","1 unit"),
      fieldwork_task("What margins, case sizes, credit and reorder cadence do neighborhood oil sellers require?","Senegal","merchant interviews + invoice observation","merchant economics by channel"),
      fieldwork_task("What oils and pack sizes do households actually buy and why?","Senegal","shop-along + receipt/purchase observation + interviews","observed behavior, not stated preference alone"),
      fieldwork_task("What prevents processors from using more installed groundnut capacity?","Senegal","processor/collector interviews + operating records","cause decomposition: finance, procurement, quality, maintenance, demand, utilities"),
      fieldwork_task("What specifications and delivered prices do feed mills require for protein meals?","Senegal","feed-mill buyer interviews + specification documents","nutrient/safety/volume/price requirements")
    ]
    save_queue(tasks,root/"runs"/MISSION/"initial-acquisition-queue.json")
    return len(packets),len(tasks)
if __name__=="__main__":
    p,t=launch(); print(f"materialized {p} packets and {t} acquisition tasks")
