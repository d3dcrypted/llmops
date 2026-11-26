# LLMOps Evaluation Suite

A lightweight starting point for repeatable evaluation of prompts, models, and retrieval systems. It defines a provider-neutral case format and produces machine-readable results suitable for CI.

## Run

```bash
python3 -m unittest discover -s tests -v
```

The baseline scorer is deliberately simple and deterministic. Model-graded metrics, lm-evaluation-harness, Promptfoo, and experiment tracking are planned adapters, not hidden requirements.

## Roadmap

- [x] evaluation case schema
- [x] deterministic exact-match and token-overlap scores
- [ ] provider adapters
- [ ] cached responses
- [x] regression thresholds
- [ ] CI artifact
- [ ] RAG faithfulness/context metrics

`evaluate_cases()` produces deterministic per-case and aggregate metrics. `regression_passes()` evaluates explicit minimum thresholds. No model, provider, or network call is required.

## Authorship

Human thought, machine hand. The author set the direction, took the decisions and reviewed the result; an AI assistant produced the drafting, the code and the prose in this file. Mistakes are the author's.
