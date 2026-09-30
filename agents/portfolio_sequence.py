#!/usr/bin/env python3
"""Dependency-aware portfolio sequencing. Produces evidence, not an automatic investment ranking."""
from collections import defaultdict
def dependency_map(genomes):
    providers=defaultdict(set); needs=defaultdict(set)
    for g in genomes:
        for x in g.get("outputs",[])+g.get("coproducts",[]): providers[x].add(g["id"])
        for x in g.get("inputs",[]): needs[x].add(g["id"])
    edges=[]
    for material in providers.keys() & needs.keys():
        for a in providers[material]:
            for b in needs[material]:
                if a!=b: edges.append({"from":a,"to":b,"dependency":material,"kind":"material"})
    return edges
def unlock_map(genomes):
    index=defaultdict(set)
    for g in genomes:
        for x in g.get("capabilities",[])+g.get("infrastructure",[])+g.get("machinery",[])+g.get("distribution",[]):
            index[x].add(g["id"])
    return [{"capability":x,"dependent_opportunities":sorted(ids),"unlock_count":len(ids)}
            for x,ids in index.items() if len(ids)>1]
def sequencing_facts(genomes):
    """Descriptive portfolio facts only; human decides priorities."""
    unlocks=unlock_map(genomes)
    return {"shared_unlocks":sorted(unlocks,key=lambda x:x["unlock_count"],reverse=True),
            "material_dependencies":dependency_map(genomes),
            "note":"These are dependency facts, not a recommendation or investment ranking."}
