"""Regression tests for validation and paired routing, without API calls."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import routing_eval as routing
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


class PairedRoutingTests(unittest.TestCase):
    def setUp(self):
        self.base = routing.Catalog("base", ["a", "b"], [{"text": "old"}], ["a", "b", "none"])
        self.head = routing.Catalog("head", ["a", "b"], [{"text": "new"}], ["a", "b", "none"])
        self.cases = [routing.Case("a", "1", "request", "a")]
        self.usage = SimpleNamespace(input_tokens=1, output_tokens=1, cache_read_input_tokens=2)
        self.args = SimpleNamespace(model="stub", samples=3)

    def run_votes(self, votes):
        with patch.object(routing, "classify", side_effect=[(v, self.usage) for v in votes]) as mock, \
                contextlib.redirect_stdout(io.StringIO()):
            results, confirmation = routing.run_paired(
                None, "stub", self.base, self.head, self.cases, 3, 1)
            code, summary = routing.report_paired(results, self.args, "base", "head", confirmation)
        return results, confirmation, code, summary, mock.call_count

    def test_identical_catalogs_share_votes_and_do_not_double_count_tokens(self):
        self.head.system = self.base.system
        results, confirmation, code, summary, calls = self.run_votes(["a", "b", "a"])
        self.assertEqual(calls, 3)
        self.assertEqual(code, 0)
        self.assertEqual(confirmation, [])
        self.assertEqual(results[0]["picks"], results[1]["picks"])
        self.assertEqual(results[1]["reused_from"], "base")
        self.assertEqual(sum(r["input_tokens"] for r in results), 3)
        self.assertEqual(sum(r["cached_input_tokens"] for r in results), 6)
        self.assertIn("Catalogues are identical", "\n".join(summary))

    def test_changed_choices_do_not_reuse_votes(self):
        self.head.system = self.base.system
        self.head.choices = ["a", "none"]
        _, confirmation, code, _, calls = self.run_votes(["a"] * 6)
        self.assertEqual(calls, 6)
        self.assertEqual(confirmation, [])
        self.assertEqual(code, 0)

    def test_transient_head_failure_does_not_gate(self):
        initial = ["a", "a", "b", "b", "b", "a"]
        results, confirmation, code, summary, calls = self.run_votes(initial + ["a"] * 18)
        self.assertEqual(code, 0)
        self.assertEqual(calls, 24)
        self.assertFalse(results[1]["passed"])
        self.assertTrue(confirmation[1]["passed"])
        self.assertIn("Unconfirmed regressions", "\n".join(summary))
        self.assertEqual(sum(r["input_tokens"] for r in results + confirmation), calls)

    def test_unstable_base_does_not_gate(self):
        _, _, code, _, _ = self.run_votes(["a"] * 3 + ["b"] * 21)
        self.assertEqual(code, 0)

    def test_repeatable_regression_gates(self):
        _, confirmation, code, summary, calls = self.run_votes(
            ["a"] * 3 + ["b"] * 3 + ["a"] * 9 + ["b"] * 9)
        self.assertEqual(code, 1)
        self.assertEqual(calls, 24)
        self.assertEqual([len(r["picks"]) for r in confirmation], [9, 9])
        self.assertIn("Confirmed regressions", "\n".join(summary))

    def test_observed_fix_needs_no_confirmation(self):
        _, confirmation, code, _, calls = self.run_votes(["b"] * 3 + ["a"] * 3)
        self.assertEqual(code, 0)
        self.assertEqual(confirmation, [])
        self.assertEqual(calls, 6)

    def test_confirmation_api_error_is_not_a_pass(self):
        responses = [(v, self.usage) for v in ["a"] * 3 + ["b"] * 3]
        with patch.object(routing, "classify", side_effect=responses + [RuntimeError("API failed")]), \
                contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "API failed"):
                routing.run_paired(None, "stub", self.base, self.head, self.cases, 3, 1)


if __name__ == "__main__":
    unittest.main()
