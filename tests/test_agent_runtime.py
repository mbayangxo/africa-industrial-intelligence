import importlib.util, unittest
from pathlib import Path
SPEC=importlib.util.spec_from_file_location('runtime',Path(__file__).parents[1]/'agents/runtime.py')
runtime=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(runtime)
class RuntimeTest(unittest.TestCase):
 def test_packets(self):
  p=runtime.mission_packets('mission-002','Compare nuts/oilseeds.')
  self.assertEqual(set(runtime.SPECIALISTS),{x.role for x in p if x.phase=='specialist-research'})
  b=[x for x in p if x.phase=='blind-discovery']; self.assertEqual(3,len(b)); self.assertEqual(3,len({x.blind_group for x in b}))
 def test_empty_novelty_fails(self):
  p=runtime.mission_packets('mission-002','test')[0]; o={k:[] for k in runtime.REQUIRED_OUTPUT}; o['new_knowledge']=''
  self.assertTrue(any('new_knowledge' in e for e in runtime.validate_output(p,o)))
 def test_no_advance_without_coverage(self): self.assertEqual('specialist-research',runtime.next_phase('specialist-research',[]))
if __name__=='__main__': unittest.main()
