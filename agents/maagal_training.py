#!/usr/bin/env python3
"""Translate recurring machine gaps into Maagal training/tooling hypotheses."""
from collections import defaultdict
def curriculum_hypotheses(machines):
    gaps=defaultdict(set)
    for m in machines:
        for a in m.get("assemblies",[]):
            for c in a.get("components",[]):
                if c["localization_status"]=="local-after-training":
                    gaps[c["category"]].add(m["id"])
    return [{"skill_or_component_family":k,"machine_ids":sorted(v),"demand_signal":len(v),
      "next_step":"define competency, tooling, instructor, prototype and acceptance test"}
      for k,v in gaps.items()]
