#!/usr/bin/env python3
"""Factory utilization scenarios and evidence-based expansion triggers."""
def annual_capacity(rate_per_hour,hours_per_shift,shifts_per_day,operating_days,utilization):
    theoretical=rate_per_hour*hours_per_shift*shifts_per_day*operating_days
    return {"theoretical":theoretical,"utilization":utilization,"effective":theoretical*utilization}
def scenarios(rate_per_hour,hours_per_shift=8,shifts_per_day=1,operating_days=250):
    return {name:annual_capacity(rate_per_hour,hours_per_shift,shifts_per_day,operating_days,u)
            for name,u in [("downside",0.35),("base-case",0.60),("high-use",0.80)]}
def expansion_gate(actual):
    required=["utilization","procurement_coverage","quality_pass_rate","reorder_rate","cash_cycle_days","downtime_rate"]
    missing=[x for x in required if actual.get(x) is None]
    if missing:return {"status":"not-evaluable","missing":missing}
    return {"status":"evaluate-with-human","facts":{k:actual[k] for k in required},
            "note":"Thresholds must be defined for the specific business before launch; the engine does not invent them after seeing results."}
