import importlib.util
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('edl_generator',Path(__file__).resolve().parents[1]/'scripts/generate-edl.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class GraphicTimingTests(unittest.TestCase):
    def test_collision_never_delays_spoken_cue(self):
        graphics=[{'type':'badge','startMs':1000,'endMs':4000},
                  {'type':'callout','startMs':2000,'endMs':5000},
                  {'type':'badge','startMs':3200,'endMs':5700}]
        out=module.dedup_overlap(graphics,10)
        self.assertEqual([g['startMs'] for g in out],[1000,3200])
        self.assertEqual(graphics[0]['endMs'],4000) # no input mutation
    def test_cta_does_not_push_visual_earlier(self):
        graphics=[{'type':'badge','startMs':8000,'endMs':12000},
                  {'type':'cta','startMs':9000,'endMs':10000}]
        out=module.dedup_overlap(graphics,10)
        self.assertEqual([g['type'] for g in out],['cta'])

if __name__=='__main__':unittest.main()
