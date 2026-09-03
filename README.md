# Deadline

*Every model meets its Deadline.*

A closed coding benchmark for AI models. 37 original Python tasks — including
a brutal tier built to break frontier models — graded by hidden, fuzz-tested
oracles: no judge model, no self-reported scores. Brutal tasks award partial
credit per test group; official runs also report a strict all-attempts-must-pass
score.

**Leaderboard:** https://violetweather.github.io/deadline-site/

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

## Scores explained

Scores are out of **100**, weighted by task difficulty (easy 6, medium 13,
hard 18, brutal 30 points, normalized to 100). A perfect run scores 100.

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
