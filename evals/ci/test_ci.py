"""Regression tests for the validation, without API calls."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate


class NegativeCaseTests(unittest.TestCase):
    def check_data(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "negative-cases.json"
            path.write_text(json.dumps(data))
            report = validate.Report()
            with patch.object(validate, "ROOT", Path(directory)), \
                    patch.object(validate, "NEGATIVE_CASES_PATH", path):
                validate.check_negative_cases(["kpitree-basics"], report)
            return report.errors

    def test_valid_case_loads(self):
        self.assertEqual(self.check_data({"version": "1", "cases": [
            {"id": "n1", "question": "Write a poem."}
        ]}), [])

    def test_missing_or_invalid_id_is_rejected(self):
        for fields in ({}, {"id": None}, {"id": ""}, {"id": " "}, {"id": []}):
            with self.subTest(fields=fields):
                errors = self.check_data({"version": "1", "cases": [
                    {"question": "Write a poem.", **fields}
                ]})
                self.assertTrue(any("`id`" in error for error in errors))

    def test_non_object_case_is_reported(self):
        for case in (None, [], "text", 1):
            with self.subTest(case=case):
                self.assertTrue(self.check_data({"version": "1", "cases": [case]}))

    def test_duplicate_ids_are_rejected(self):
        errors = self.check_data({"version": "1", "cases": [
            {"id": "n1", "question": "Write a poem."},
            {"id": "n1", "question": "Write a story."},
        ]})
        self.assertTrue(any("duplicate case id" in error for error in errors))

    def test_a_case_that_names_a_skill_is_not_out_of_scope(self):
        errors = self.check_data({"version": "1", "cases": [
            {"id": "n1", "question": "Use kpitree-basics to answer this."},
        ]})
        self.assertTrue(any("not out-of-scope" in error for error in errors))


class ToolNameTests(unittest.TestCase):
    def test_backticked_snake_case_names_are_extracted(self):
        text = "Call `analyze_metric` then `get_metric_drivers`; the `kpitree-basics` skill, `status`."
        self.assertEqual(
            set(validate.BACKTICKED.findall(text)),
            {"analyze_metric", "get_metric_drivers", "status"},
        )

    def test_an_unknown_tool_name_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "demo"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: demo\ndescription: d\n---\nCall `made_up_tool`.\n")
            report = validate.Report()
            with patch.object(validate, "ROOT", root), \
                    patch.object(validate, "SKILLS_DIR", root / "skills"), \
                    patch.object(validate, "AGENTS_DIR", root / "agents"), \
                    patch.object(validate, "COMMANDS_DIR", root / "commands"):
                validate.check_tool_names({"analyze_metric"}, report)
            self.assertEqual(len(report.errors), 1)
            self.assertIn("made_up_tool", report.errors[0])

if __name__ == "__main__":
    unittest.main()
