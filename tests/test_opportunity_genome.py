import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load('g',ROOT/'agents/opportunity_genome.py');q=load('q',ROOT/'agents/portfolio_sequence.py')
class GenomeTests(unittest.TestCase):
 def test_shared_asset(self):
  xs=[{'id':'a','capabilities':['drying'],'infrastructure':['lab']},{'id':'b','capabilities':['drying'],'infrastructure':['lab']}]
  self.assertTrue(g.shared_asset_hypotheses(xs))
 def test_coproduct_link_is_hypothesis(self):
  xs=[{'id':'a','outputs':[],'coproducts':['cake']},{'id':'b','inputs':['cake']}]
  self.assertIn('hypothesis',g.coproduct_links(xs)[0]['status'])
 def test_unlock_map(self):
  xs=[{'id':'a','capabilities':['testing']},{'id':'b','capabilities':['testing']}]
  self.assertEqual(2,q.unlock_map(xs)[0]['unlock_count'])
if __name__=='__main__':unittest.main()
