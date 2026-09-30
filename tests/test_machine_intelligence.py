import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mi=load('mi',ROOT/'agents/machine_intelligence.py'); mt=load('mt',ROOT/'agents/maagal_training.py')
def m(i,status='fabricate-local-now'):
 return {'id':i,'assemblies':[{'components':[{'name':'frame','category':'structure','criticality':'medium','localization_status':status}]}]}
class MachineTests(unittest.TestCase):
 def test_localization_is_not_percentage(self): self.assertIn('not cost',mi.localization_profile(m('a'))['warning'])
 def test_recurrence(self): self.assertEqual(2,mi.recurring_components([m('a'),m('b')])[0]['machine_count'])
 def test_training_signal(self): self.assertEqual(1,mt.curriculum_hypotheses([m('a','local-after-training')])[0]['demand_signal'])
if __name__=='__main__':unittest.main()
