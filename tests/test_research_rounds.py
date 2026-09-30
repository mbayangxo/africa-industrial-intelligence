import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=load('rounds',ROOT/'agents/rounds.py'); ra=load('research',ROOT/'agents/research_adapter.py')
class RoundTests(unittest.TestCase):
 def test_no_round1_without_outputs(self): self.assertFalse(r.advance(1,[],[])['advance'])
 def test_round2_blocks_unresolved(self): self.assertFalse(r.advance(2,[{'contradictions':['x'],'unknowns':[]}],[])['advance'])
 def test_buildability_requires_field_and_quote(self): self.assertFalse(r.advance(3,[{}],[{'kind':'fieldwork'}])['advance'])
 def test_freshness(self): self.assertEqual('current',ra.freshness_flag({'published':'2026-05-01'})); self.assertEqual('historical-context',ra.freshness_flag({'published':'2024-01-01'}))
if __name__=='__main__': unittest.main()
