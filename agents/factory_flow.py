#!/usr/bin/env python3
"""Factory flow adjacency checks. Not a CAD/layout engine."""
def flow_issues(steps,zones):
    zone_names={z["name"] for z in zones}; issues=[]
    for s in steps:
        z=s.get("zone")
        if z and z not in zone_names: issues.append(f"unknown zone {z} for {s['name']}")
    seq=[s.get("zone") for s in steps if s.get("zone")]
    revisits=[z for i,z in enumerate(seq) if z in seq[:i] and (i==0 or seq[i-1]!=z)]
    if revisits: issues.append("process flow revisits zones; inspect cross-traffic/hygiene risk: "+", ".join(sorted(set(revisits))))
    return issues
