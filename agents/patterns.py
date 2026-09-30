#!/usr/bin/env python3
from collections import defaultdict
def recurring_capabilities(learnings,min_missions=2):
 d=defaultdict(lambda:{'missions':set(),'learning_ids':[]})
 for l in learnings:
  if l.get('kind') not in {'recurring-constraint','reusable-capability','cross-mission-relationship'}: continue
  for tag in l.get('sector_tags',[]):
   d[tag]['missions'].update(l.get('origin_mission_ids',[])); d[tag]['learning_ids'].append(l['id'])
 return [{'capability':k,'mission_count':len(v['missions']),'mission_ids':sorted(v['missions']),'learning_ids':v['learning_ids'],'action':'send-to-infrastructure-and-independent-discovery'} for k,v in d.items() if len(v['missions'])>=min_missions]
