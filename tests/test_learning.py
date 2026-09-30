import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mem=load('memory',ROOT/'agents/memory.py'); pat=load('patterns',ROOT/'agents/patterns.py')
class LearningTests(unittest.TestCase):
 def test_cross_geography_refresh(self):
  l={'reuse_rule':'must-refresh','status':'evidenced','geographies':['Senegal']}; self.assertTrue(mem.reusable(l,'Mali','2026-01-01')['requires_refresh'])
 def test_rejected_is_lesson_only(self):
  l={'reuse_rule':'context-only','status':'rejected','geographies':['Senegal']}; self.assertEqual('lesson-only',mem.reusable(l,'Senegal')['use_as'])
 def test_recurring_pattern_needs_multiple_missions(self):
  ls=[{'id':'lrn-a','kind':'recurring-constraint','sector_tags':['drying'],'origin_mission_ids':['mission-001']},{'id':'lrn-b','kind':'recurring-constraint','sector_tags':['drying'],'origin_mission_ids':['mission-002']}]
  self.assertEqual('drying',pat.recurring_capabilities(ls)[0]['capability'])
if __name__=='__main__':unittest.main()
