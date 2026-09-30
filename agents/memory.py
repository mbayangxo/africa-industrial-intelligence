#!/usr/bin/env python3
from datetime import date
def reusable(l,g,today=None):
 today=today or date.today().isoformat(); rule=l['reuse_rule']; geos=l.get('geographies',[])
 if l.get('status') in {'rejected','superseded'}: return {'use_as':'lesson-only','requires_refresh':True}
 if rule=='portable-technical': return {'use_as':'technical-context','requires_refresh':False}
 if rule in {'context-only','field-reverify'}: return {'use_as':'hypothesis','requires_refresh':True}
 expired=bool(l.get('valid_through') and l['valid_through']<today); same=g in geos
 return {'use_as':'prior-evidence' if same and not expired else 'hypothesis','requires_refresh':expired or not same or rule=='must-refresh'}
def candidates(items,tags,geography):
 r=[]
 for x in items:
  n=len(tags.intersection(set(x.get('sector_tags',[]))))
  if n:r.append((n,x,reusable(x,geography)))
 return sorted(r,key=lambda z:z[0],reverse=True)
