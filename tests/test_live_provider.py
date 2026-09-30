import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('provider',ROOT/'agents/provider.py'); e=load('evidence',ROOT/'agents/evidence_portfolio.py')
class LiveBoundaryTests(unittest.TestCase):
 def test_rejects_unsourced_quantitative_claim(self):
  raw={'new_knowledge':'x','sources':[{'url':'https://a','publisher':'A'},{'url':'https://b','publisher':'B'}],'claims':[{'quantitative':True,'classification':'FACT','evidence_ids':[]}]}
  self.assertTrue(any('quantitative' in x for x in p.quality_gate(raw)))
 def test_market_portfolio_needs_official_and_commercial(self):
  s=[{'source_class':'official-statistical','publisher':'A','url':'https://a'}]
  self.assertFalse(e.portfolio(s,'market')['passes'])
 def test_independence_warns_single_domain(self):
  s=[{'publisher':'A','url':'https://a.example/x'},{'publisher':'A','url':'https://a.example/y'}]
  self.assertTrue(e.independence_warning(s))
if __name__=='__main__': unittest.main()
