import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mb=load('mb',ROOT/'agents/material_balance.py');cl=load('cl',ROOT/'agents/cost_ledger.py');fc=load('fc',ROOT/'agents/factory_composer.py')
class FactoryTests(unittest.TestCase):
 def test_mass_balance_catches_missing_mass(self): self.assertFalse(mb.check_balance([{'mass_kg':1000}],[{'mass_kg':800}],[{'mass_kg':100}])['passes'])
 def test_unknown_cost_cannot_have_number(self): self.assertTrue(cl.validate_line({'name':'x','amount':10,'basis':'unknown','currency':'XOF'}))
 def test_bottleneck(self):
  f={'target_throughput':{'value':100},'process_steps':[{'name':'press','machine_ids':['mach-a']}]};m=[{'id':'mach-a','throughput':{'value':50}}]
  self.assertEqual('capacity',fc.bottlenecks(f,m)[0]['type'])
if __name__=='__main__':unittest.main()
