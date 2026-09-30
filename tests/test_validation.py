"""Tests use temporary, unmistakably synthetic records only."""
import importlib.util, json, tempfile, unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("validator", Path(__file__).parents[1] / "scripts/validate.py")
validator = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(validator)

class ValidationRulesTest(unittest.TestCase):
    def test_repository_foundation_validates(self):
        self.assertEqual([], validator.run())

    def test_unsupported_synthetic_quantitative_fact_is_rejected(self):
        synthetic = {"classification":"FACT", "quantitative":True, "source_ids":[], "created_at":"2026-01-01"}
        records = {name:{} for name in validator.RECORD_DIRS}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SYNTHETIC-DO-NOT-INGEST.json"
            records["claims"]["clm-synthetic-only"] = (synthetic, path)
            errors=[]; validator.validate_records(records, errors)
        self.assertTrue(any("requires a source" in error for error in errors))
        self.assertTrue(any("unsupported" in error for error in errors))

    def test_broken_synthetic_cross_reference_is_rejected(self):
        opportunity={"thesis_claim_ids":["clm-does-not-exist"],"stage":"candidate","red_team":{"status":"not-started"}}
        records = {name:{} for name in validator.RECORD_DIRS}
        with tempfile.TemporaryDirectory() as directory:
            records["opportunities"]["opp-synthetic-only"]=(opportunity, Path(directory)/"SYNTHETIC.json")
            errors=[]; validator.validate_records(records, errors)
        self.assertTrue(any("unknown claim id" in error for error in errors))

    def test_research_journals_are_validated(self):
        errors=[]; validator.validate_research_journals(errors)
        self.assertEqual([], errors)

if __name__ == "__main__": unittest.main()
