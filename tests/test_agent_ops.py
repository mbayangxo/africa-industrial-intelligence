import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
sched=load('scheduler',ROOT/'agents/scheduler.py'); score=load('scorecard',ROOT/'agents/scorecard.py')
class OpsTest(unittest.TestCase):
 def test_handoffs_become_tasks(self):
  o={'packet_id':'pkt-x','handoffs':[{'to_role':'industrial-engineer','question':'test yield'}],'contradictions':['two sources disagree'],'unknowns':['local price']}
  self.assertEqual({'handoff','contradiction','evidence-gap'},{t['kind'] for t in sched.derive_tasks(o)})
 def test_quote_requires_commercial_terms(self):
  q=sched.quote_task('press','food grade','Senegal','1'); self.assertIn('freight',q['required']); self.assertIn('lead time',q['required'])
 def test_score_rewards_novelty_not_length(self):
  o=[{'status':'complete','new_knowledge':'x','phase':'specialist-research','contradictions':[],'disproof_tests':['kill']}]
  self.assertEqual(1,score.score(o,[])['novelty_rate'])
if __name__=='__main__': unittest.main()
