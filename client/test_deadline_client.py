import contextlib
import http.client
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import deadline_client as client


def response(text, finish_reason="stop", tokens=20):
    return {"id": "response-123", "model": "test-model",
            "choices": [{"message": {"content": text}, "finish_reason": finish_reason}],
            "usage": {"prompt_tokens": 10, "completion_tokens": tokens}}


def http_response(data):
    return io.BytesIO(json.dumps(data).encode("utf8"))


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="deadline-client-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.prompts = self.root / "prompts"
        self.prompts.mkdir()
        self.names = ["01_one", "02_two", "03_three"]
        for name in self.names:
            (self.prompts / (name + ".md")).write_text(name, encoding="utf8")
        self.output = self.root / "submission.json"
        self.partial = self.root / "submission.json.partial"
        self.receipt = {"tokens_in": 11, "tokens_out": 23490,
                        "seconds": 1589.68, "model_echo": "test-model"}

    def saved(self, replies, target=None):
        data = {"client": 2, "model": "test-model", "replies": replies,
                "meta": {name: dict(self.receipt) for name in replies}}
        (target or self.partial).write_text(json.dumps(data), encoding="utf8")
        return data

    def run_client(self, responses, *, provider="openai", error=None):
        args = ["deadline_client.py", "--type", provider, "--model", "test-model",
                "--out", str(self.output)]
        log = io.StringIO()
        with patch.object(client, "PROMPTS_DIR", self.prompts), \
             patch.object(client.sys, "argv", args), \
             patch.object(client.urllib.request, "urlopen", side_effect=responses) as request, \
             patch.object(client.time, "sleep") as sleep, contextlib.redirect_stdout(log):
            if error:
                with self.assertRaisesRegex(SystemExit, error):
                    client.main()
            else:
                client.main()
        return request, sleep, log.getvalue()

    def read(self, path):
        return json.loads(path.read_text(encoding="utf8"))

    def test_blank_reply_stops_without_final_submission(self):
        for text in (None, "", " ", "\r\n\t", "```python\n \n```", "```js\n```"):
            with self.subTest(text=text):
                self.partial.unlink(missing_ok=True)
                request, sleep, _ = self.run_client(
                    [http_response(response(text, "length"))], error="Run INCOMPLETE")
                request.assert_called_once()
                sleep.assert_not_called()
                self.assertFalse(self.output.exists())
                saved = self.read(self.partial)
                self.assertEqual(saved["replies"], {"01_one": text})
                receipt = saved["meta"]["01_one"]
                self.assertEqual(receipt["response_status"], "unresolved_blank")
                self.assertEqual(receipt["finish_reason"], "length")
                self.assertEqual(receipt["response_id"], "response-123")
                self.assertEqual(receipt["tokens_out"], 20)

    def test_connection_drop_then_blank_does_not_complete_task(self):
        original = self.saved({"01_one": "# SKIP"})
        request, sleep, _ = self.run_client(
            [http.client.IncompleteRead(b"partial", 100), http_response(response(" "))],
            error="02_two.*INCOMPLETE")
        self.assertEqual(request.call_count, 2)
        self.assertEqual(request.call_args_list[0].args[0].data,
                         request.call_args_list[1].args[0].data)
        sleep.assert_called_once_with(5)
        saved = self.read(self.partial)
        self.assertEqual(saved["replies"], {"01_one": "# SKIP", "02_two": " "})
        self.assertEqual(saved["meta"]["01_one"], original["meta"]["01_one"])
        self.assertEqual(saved["meta"]["02_two"]["request_attempts"], 2)
        self.assertEqual(saved["meta"]["02_two"]["transport_errors"], [{"error": "IncompleteRead"}])
        self.assertFalse(self.output.exists())

    def test_transport_retry_budget_remains_bounded_and_progress_survives(self):
        self.saved({"01_one": "def solve(): return 1"})
        before = self.partial.read_bytes()
        request, sleep, _ = self.run_client(
            [http.client.IncompleteRead(b"", 100) for _ in range(4)],
            error="Connection kept failing")
        self.assertEqual(request.call_count, 4)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [5, 15, 30])
        self.assertEqual(len({c.args[0].data for c in request.call_args_list}), 1)
        self.assertEqual(self.partial.read_bytes(), before)
        self.assertFalse(self.output.exists())

    def test_resume_retries_blank_and_keeps_answers_and_skip(self):
        original = self.saved({"01_one": "def solve(): return 1", "02_two": " ",
                               "03_three": "```python\n# SKIP\n```"})
        reply = "\n```python\ndef solve(): return 2\n```\n"
        request, _, log = self.run_client([http_response(response(reply))])
        request.assert_called_once()
        self.assertIn("02_two", request.call_args.args[0].data.decode())
        self.assertIn("2/3 task(s) already answered", log)
        result = self.read(self.output)
        self.assertEqual(result["client"], 3)
        self.assertEqual(result["replies"], {**original["replies"], "02_two": reply})
        self.assertEqual(result["meta"]["02_two"]["previous_attempts"],
                         [{"reply": " ", "receipt": self.receipt}])
        self.assertEqual(result["meta"]["01_one"], original["meta"]["01_one"])
        self.assertEqual(result["tokens_out"], 23490 * 2 + 20)
        self.assertFalse(self.partial.exists())

    def test_repeated_blank_resumes_preserve_each_attempt(self):
        self.saved({"01_one": "# SKIP", "03_three": "// SKIP"})
        for text in (" ", "\n"):
            self.run_client([http_response(response(text))], error="Run INCOMPLETE")
        self.run_client([http_response(response("def solve(): return 2"))])
        history = self.read(self.output)["meta"]["02_two"]["previous_attempts"]
        self.assertEqual([a["reply"] for a in history], [" ", "\n"])
        self.assertTrue(all(a["receipt"]["response_status"] == "unresolved_blank" for a in history))

    def test_legacy_final_with_blank_can_resume_and_original_is_backed_up(self):
        self.saved({"01_one": "# SKIP", "02_two": " ", "03_three": "# SKIP"}, self.output)
        before = self.output.read_bytes()
        request, _, _ = self.run_client([http_response(response("def solve(): return 2"))])
        request.assert_called_once()
        backups = list(self.root.glob("submission.json.before-resume-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), before)
        self.assertEqual(self.read(self.output)["meta"]["02_two"]["previous_attempts"][0]["reply"], " ")

    def test_failed_repair_leaves_original_final_file_untouched(self):
        self.saved({"01_one": "# SKIP", "02_two": " ", "03_three": "# SKIP"}, self.output)
        before = self.output.read_bytes()
        self.run_client([http_response(response(None))], error="Run INCOMPLETE")
        self.assertEqual(self.output.read_bytes(), before)
        self.assertIsNone(self.read(self.partial)["replies"]["02_two"])

    def test_complete_final_makes_no_requests_and_is_not_rewritten(self):
        self.saved({name: "# SKIP" for name in self.names}, self.output)
        before = self.output.read_bytes()
        request, _, log = self.run_client([])
        request.assert_not_called()
        self.assertIn("already complete", log)
        self.assertEqual(self.output.read_bytes(), before)

    def test_partial_takes_precedence_over_older_final(self):
        self.saved({name: "# SKIP" for name in self.names}, self.output)
        self.saved({"01_one": "# SKIP", "02_two": " ", "03_three": "# SKIP"})
        request, _, _ = self.run_client([http_response(response("def solve(): return 2"))])
        request.assert_called_once()
        self.assertEqual(self.read(self.output)["replies"]["02_two"], "def solve(): return 2")

    def test_fresh_run_preserves_nonblank_wrong_answers_and_explicit_skips(self):
        replies = ["not valid code", "```python\n# SKIP\n```", "// SKIP"]
        self.run_client([http_response(response(text)) for text in replies])
        self.assertEqual(self.read(self.output)["replies"], dict(zip(self.names, replies)))

    def test_gemini_missing_answer_is_saved_with_completion_reason(self):
        data = {"candidates": [{"finishReason": "MAX_TOKENS"}],
                "usageMetadata": {"promptTokenCount": 10, "thoughtsTokenCount": 20},
                "modelVersion": "test-model", "responseId": "gemini-response"}
        self.run_client([http_response(data)], provider="gemini", error="Run INCOMPLETE")
        receipt = self.read(self.partial)["meta"]["01_one"]
        self.assertEqual(receipt["finish_reason"], "MAX_TOKENS")
        self.assertEqual(receipt["tokens_out"], 20)

    def test_anthropic_empty_answer_is_saved_with_completion_reason(self):
        data = {"content": [], "stop_reason": "max_tokens", "id": "anthropic-response",
                "model": "test-model", "usage": {"input_tokens": 10, "output_tokens": 20}}
        self.run_client([http_response(data)], provider="anthropic", error="Run INCOMPLETE")
        receipt = self.read(self.partial)["meta"]["01_one"]
        self.assertEqual(receipt["finish_reason"], "max_tokens")
        self.assertEqual(receipt["response_id"], "anthropic-response")


if __name__ == "__main__":
    unittest.main()
