#!/usr/bin/env python3
"""Material-balance checks for factory compositions."""
def check_balance(inputs,outputs,losses,tolerance_pct=0.5):
    total_in=sum(x["mass_kg"] for x in inputs); total_out=sum(x["mass_kg"] for x in outputs)+sum(x["mass_kg"] for x in losses)
    delta=total_in-total_out; pct=abs(delta)/total_in*100 if total_in else 0
    return {"input_kg":total_in,"accounted_kg":total_out,"unaccounted_kg":delta,"error_pct":round(pct,4),"passes":pct<=tolerance_pct}
def stream_value(streams):
    result=[]
    for s in streams:
        v=s.get("mass_kg"); p=s.get("price_per_kg")
        result.append(dict(s,gross_value=None if v is None or p is None else v*p,
                           value_status="unknown" if p is None else "requires-buyer-and-price-evidence"))
    return result
