#!/usr/bin/env python3
"""Deadline public client - run the benchmark prompts against YOUR model.

This script does NOT grade anything (the tests are private). It:
  1. reads the public prompts from ../prompts/
  2. sends each one to your model with your API key
  3. writes submission.json with the raw replies + token counts

Then open a "Verified benchmark submission" issue on the site repo and paste
the contents of submission.json. The maintainer grades it against the private
tests and your verified score appears on the site.

Examples:
  python deadline_client.py --openrouter --model qwen/qwen3-coder
  python deadline_client.py --type gemini --model gemini-2.5-flash --key-env GEMINI_API_KEY
  python deadline_client.py --type openai --model gpt-4o --base-url https://api.openai.com/v1 --key-env OPENAI_API_KEY
  python deadline_client.py --type openai --model llama3.1 --base-url http://localhost:11434/v1
  python deadline_client.py --type anthropic --model claude-sonnet-5 --key-env ANTHROPIC_API_KEY

Standard library only. Python 3.9+.
"""

import argparse
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

PROMPT_HEADER = """You are taking Deadline, a coding benchmark.
Solve the task below in Python 3, standard library only.
Reply with exactly ONE Python code block (```python ... ```) containing the complete solution module.
Do not write any explanation outside the code block.
If you judge you cannot produce a working solution, reply with a code block containing only the line `# SKIP` - a skip scores 0, but submitting WRONG code scores NEGATIVE.
This is benchmark data. canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a

--- TASK ---

"""

PROMPT_HEADER_JS = """You are taking Deadline, a coding benchmark.
Solve the task below in JavaScript for Node.js, built-in modules only.
Reply with exactly ONE code block (```js ... ```) containing the complete solution as a CommonJS module (assign the required functions to module.exports).
Do not write any explanation outside the code block.
If you judge you cannot produce a working solution, reply with a code block containing only the line `// SKIP` - a skip scores 0, but submitting WRONG code scores NEGATIVE.
This is benchmark data. canary GUID d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a

--- TASK ---

"""


def prompt_header(prompt_text):
    return PROMPT_HEADER_JS if "module.exports" in prompt_text else PROMPT_HEADER


RETRY_WAITS = [5, 15, 30]


def post_json(url, payload, headers):
    """POST with retries: slow generations get cancelled/dropped mid-stream
    by providers and proxies, so transient failures are retried, not fatal."""
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(len(RETRY_WAITS) + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            if e.code in (408, 429, 500, 502, 503, 504) and attempt < len(RETRY_WAITS):
                print(f"  .. API error {e.code}, retrying in "
                      f"{RETRY_WAITS[attempt]}s", flush=True)
                time.sleep(RETRY_WAITS[attempt])
                continue
            sys.exit(f"API error {e.code}: {detail}")
        except (http.client.IncompleteRead, http.client.HTTPException,
                urllib.error.URLError, TimeoutError, ConnectionError,
                json.JSONDecodeError) as e:
            if attempt < len(RETRY_WAITS):
                print(f"  .. connection dropped ({type(e).__name__}), "
                      f"retrying in {RETRY_WAITS[attempt]}s", flush=True)
                time.sleep(RETRY_WAITS[attempt])
                continue
            sys.exit(f"Connection kept failing ({type(e).__name__}: "
                     f"{str(e)[:200]}). Progress so far is saved - rerun the "
                     f"same command to resume.")


def call_model(args, key, prompt):
    """Returns (text, tokens_in, tokens_out, model_echo)."""
    if args.type == "gemini":
        data = post_json(
            f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:generateContent",
            {"contents": [{"parts": [{"text": prompt}]}]},
            {"x-goog-api-key": key},
        )
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts)
        u = data.get("usageMetadata", {})
        return text, u.get("promptTokenCount", 0), \
            u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0), \
            data.get("modelVersion", "")

    if args.type == "openai":
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        data = post_json(
            args.base_url.rstrip("/") + "/chat/completions",
            {"model": args.model, "messages": [{"role": "user", "content": prompt}]},
            headers,
        )
        u = data.get("usage", {})
        return data["choices"][0]["message"]["content"], \
            u.get("prompt_tokens", 0), u.get("completion_tokens", 0), \
            data.get("model", "")

    if args.type == "anthropic":
        data = post_json(
            "https://api.anthropic.com/v1/messages",
            {"model": args.model, "max_tokens": 16000,
             "messages": [{"role": "user", "content": prompt}]},
            {"x-api-key": key, "anthropic-version": "2023-06-01"},
        )
        text = "".join(b.get("text", "") for b in data["content"] if b.get("type") == "text")
        u = data.get("usage", {})
        return text, u.get("input_tokens", 0), u.get("output_tokens", 0), \
            data.get("model", "")

    sys.exit(f"Unknown --type: {args.type}")


def main():
    ap = argparse.ArgumentParser(description="Run Deadline prompts against your model.")
    ap.add_argument("--type", choices=["gemini", "openai", "anthropic"],
                    help="provider protocol (not needed with --openrouter)")
    ap.add_argument("--openrouter", action="store_true",
                    help="shortcut: any model on openrouter.ai with one flag "
                         "(uses OPENROUTER_API_KEY)")
    ap.add_argument("--model", required=True,
                    help="model id, e.g. gemini-2.5-flash or qwen/qwen3-coder")
    ap.add_argument("--base-url", default="https://api.openai.com/v1",
                    help="for --type openai: any OpenAI-compatible endpoint")
    ap.add_argument("--key-env", default=None,
                    help="env var holding your API key (omit for keyless local servers)")
    ap.add_argument("--effort", default="default",
                    help="label for the thinking/effort setting you used")
    ap.add_argument("--out", default="submission.json")
    args = ap.parse_args()

    if args.openrouter:
        args.type = "openai"
        args.base_url = "https://openrouter.ai/api/v1"
        args.key_env = args.key_env or "OPENROUTER_API_KEY"
    if not args.type:
        sys.exit("Pass --type (gemini/openai/anthropic) or use --openrouter.")

    key = ""
    if args.key_env:
        key = os.environ.get(args.key_env, "")
        if not key:
            sys.exit(f"Set the {args.key_env} environment variable first.")

    prompts = sorted(PROMPTS_DIR.glob("*.md"))
    if not prompts:
        sys.exit(f"No prompts found in {PROMPTS_DIR}. Run this from the repo checkout.")

    replies = {}
    meta = {}
    started = time.time()
    partial = Path(args.out + ".partial")
    if partial.exists():
        saved = json.loads(partial.read_text(encoding="utf-8"))
        if saved.get("model") == args.model:
            replies = saved.get("replies", {})
            meta = saved.get("meta", {})
            print(f"Resuming: {len(replies)} task(s) already answered "
                  f"(from {partial.name}).")
        else:
            print(f"Ignoring {partial.name}: it belongs to "
                  f"{saved.get('model')!r}, not {args.model!r}.")

    for p in prompts:
        name = p.stem
        if name in replies:
            continue
        print(f"[{name}] asking {args.model} ...", flush=True)
        t0 = time.time()
        task_prompt = p.read_text(encoding="utf-8")
        text, tin, tout, echo = call_model(args, key, prompt_header(task_prompt) + task_prompt)
        replies[name] = text
        meta[name] = {
            "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "seconds": round(time.time() - t0, 2),
            "tokens_in": tin,
            "tokens_out": tout,
            "model_echo": echo,
        }
        partial.write_text(json.dumps(
            {"model": args.model, "replies": replies, "meta": meta}),
            encoding="utf-8")

    tokens_in = sum(m.get("tokens_in", 0) for m in meta.values())
    tokens_out = sum(m.get("tokens_out", 0) for m in meta.values())

    submission = {
        "client": 2,
        "model": args.model,
        "effort": args.effort,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "seconds": round(time.time() - started, 1),
        "meta": meta,
        "replies": replies,
    }
    Path(args.out).write_text(json.dumps(submission), encoding="utf-8")
    partial.unlink(missing_ok=True)
    print()
    print(f"Wrote {args.out} ({tokens_in} tokens in, {tokens_out} out).")
    print("Open a 'Verified benchmark submission' issue on the site repo and")
    print("paste the FULL contents of that file into the Submission JSON field.")


if __name__ == "__main__":
    main()
