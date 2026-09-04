# Deadline

*Every model meets its Deadline.*

A closed coding benchmark for AI models. 27 MACHINE-GENERATED Python, JavaScript, and SQL tasks (nearly half pure inference from observed behavior) —
hidden cipher pipelines, randomized state machines and formats, scrambled
precedence tables, performance gates, and a generated-semantics interpreter —
graded by hidden, fuzz-tested oracles with partial credit per test group.
No judge model, no self-reported scores. Every task carries a TOKEN BUDGET
(its deadline); the headline DL Score is correctness times timeliness, so
correct-but-bloated loses to correct-and-lean. Official runs also report a
strict all-attempts-must-pass score.

**Scope, honestly:** Deadline measures exact Python 3, JavaScript (Node), and SQLite SQL with
standard libraries only, across 27 machine-generated tasks — most reverse-engineered
from the observed behavior of hidden systems — in one blind attempt against
token deadlines. Two tasks are whole-project bug
hunts across dozens of generated files. It does not measure dependency
wrangling or long agentic sessions. Skill areas (algorithms,
parsing, state, bugfix, refactoring, integration, ...) are tagged per task
in [`data/tasks.json`](data/tasks.json).

**Leaderboard:** https://deadline.nnx.fyi/

## Why the tests are private

Public benchmark answers leak into training data and inflate scores.
Deadline keeps the tests and reference solutions private. Only the prompts
are public (in [`prompts/`](prompts/)), so anyone can run their model against
them - but only the maintainer can grade.

## Submit a verified result

1. Clone this repo.
2. Run the client against your model (your key, your machine, standard library only):

```
python client/deadline_client.py --type gemini --model gemini-2.5-flash --key-env GEMINI_API_KEY
```

   `--type openai` works for any OpenAI-compatible endpoint (OpenAI, OpenRouter,
   Groq, and local servers like Ollama with `--base-url http://localhost:11434/v1`
   and no `--key-env`). `--type anthropic` for Claude. Use `--effort` to label a
   thinking/effort setting.

3. The script writes `submission.json` (raw replies + token counts).
4. [Open a submission issue](../../issues/new?template=submission.yml) and paste
   the full file contents.
5. The maintainer grades your replies against the private tests and posts your
   verified score on the issue. It then appears on the site, marked "community".

Rules: one blind attempt per task, no test peeking (you can't - they're private),
no hand-editing replies. Obviously hand-written "replies" get rejected.

### Interrupted runs and blank replies

Client version 3 stops with **INCOMPLETE** if a provider returns no text,
whitespace, or an empty code block. It saves the reply and receipt in
`submission.json.partial` and does not write a final submission. Connection
failures still use the existing three retries; a returned blank answer requires
an explicit resume instead of silently generating additional answers.

Rerun the same command to resume. Valid saved responses, including explicit
`# SKIP` / `// SKIP` answers, are kept. Missing and blank tasks are requested again.
The client reads the partial checkpoint first, or an existing `--out` file if
there is no checkpoint. This also repairs blank entries saved by older clients.
An already complete output file makes no new requests; use a different `--out`
filename for a new run.

When repairing an existing output file, the client makes a byte-for-byte backup
before replacing it. Earlier blank replies and receipts remain in each task's
`previous_attempts`; new receipts also retain completion reasons, response IDs
when supplied, and transport retry details. A replacement is a new generation,
not recovery of the original answer, and its history must be retained for review.
Top-level token totals describe the retained responses; previous-attempt usage is
recorded separately, and usage from dropped connections may be unknown.

Client regression checks (no API calls):

```powershell
python -m unittest discover -s client -p 'test_*.py' -v
```

## Scores explained

Scores are out of **100**, weighted by task difficulty and depth. The
**DL Score** additionally applies each task's token budget: points decay by
budget÷tokens past the deadline. Runs without per-task token data
(subscriptions, agent mode) get a raw score only.

- **Official**: runs executed end to end by the maintainer, averaged over
  3 attempts per task and shown with an error bar (±).
- **Community**: replies submitted by users, graded by the maintainer
  (single attempt each). The site shows only the AVERAGE of all verified
  submissions per model — individual submissions and usernames are never
  displayed. Scores are verified; token counts, cost, and time are averages
  of client-reported numbers.

Costs are computed from token counts using [`prices.json`](prices.json)
(USD per million tokens). Corrections to prices are welcome as PRs.

## Contamination canary

Every prompt carries the canary GUID `d34d1in3-7f3d-4c2e-a8b5-9d213c5b8e4a`.
If this string ever shows up in a model's unprompted output or a training
corpus, the task set has leaked and will be rotated. Please do not train
on this repository.
