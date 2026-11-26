# LLMOps Reference Stack

Five small reference projects for the LLMOps lifecycle, in one tree. They were
published as separate repositories and are merged here, history included, so the
pieces can be read together, tested by one pipeline and versioned as a set.

Nothing in this repository needs a GPU, an API key or a network call to run its
tests. Every project is deliberately dependency-light, deterministic and
provider-neutral: interfaces first, adapters later.

## Needs and gains

| Project | Need it addresses | What you get |
| --- | --- | --- |
| [`rag-pipeline/`](rag-pipeline) | Answers over your own documents with no way to check where they came from | Deterministic ingestion, chunking and retrieval that return citations: source, chunk index and the exact retrieved text. Ingest rejects traversal, symlink targets, non-files and oversized input |
| [`evaluation-suite/`](evaluation-suite) | A prompt, model or retrieval change ships with no repeatable way to know whether quality moved | A provider-neutral case format, deterministic exact-match and token-overlap scores, explicit regression thresholds, machine-readable results suitable for CI |
| [`model-serving/`](model-serving) | A local model served behind an opaque endpoint, with no metrics | An OpenAI-compatible endpoint with Prometheus metrics and Grafana wiring, bound to loopback by default, plus an explicit list of what production would still require |
| [`finetuning-lora/`](finetuning-lora) | Fine-tuning experiments that cannot be reproduced or compared | A dataset manifest and validation contract plus an experiment configuration example; training data stays external, only manifests, checksums and licences are committed |
| [`security-governance/`](security-governance) | LLM features that reach users with no input classification, policy, redaction or audit trail | Deterministic policy checks, a minimal PII redaction example and a structured decision record that never stores raw secrets |

## How the pieces fit

A document enters through `rag-pipeline`, which returns text with citations.
`finetuning-lora` holds the contracts for the data and the experiments behind
the model. `model-serving` exposes a model behind a compatible API and makes it
observable. `evaluation-suite` decides whether a change is an improvement or a
regression. `security-governance` sits across all of them: classify the input,
apply policy, redact, keep an auditable record.

Each directory stands alone. Use one project, or use the set.

## Run

```bash
# one project
cd rag-pipeline && python3 -m unittest discover -s tests -v

# everything
for d in */; do echo "== $d"; (cd "$d" && python3 -m unittest discover -s tests) || exit 1; done
```

## Layout

```text
.
├── evaluation-suite/
├── finetuning-lora/
├── model-serving/
├── rag-pipeline/
└── security-governance/
```

Each project directory carries its own `README.md`, `DECISIONS.md`, `VERSION`
and tests. Shared files live once at the root: `LICENSE`, `GOVERNANCE.md` and
the CI workflow.

## Design rules

- Synthetic examples only. No secrets, no private data, no credentials, no
  unlicensed datasets, no model weights.
- Tests pass without network access, credentials or a GPU.
- Interfaces stay provider-neutral. An adapter is optional and never required by
  the baseline.
- Trade-offs are documented next to the code that makes them, in `DECISIONS.md`.

## Continuous integration

One workflow, one job per project, each running from its own directory. No
project can break another one's build.

## Merged from

| Directory | Original repository |
| --- | --- |
| `evaluation-suite/` | `llmops-evaluation-suite` |
| `finetuning-lora/` | `llmops-finetuning-lora` |
| `model-serving/` | `llmops-model-serving` |
| `rag-pipeline/` | `llmops-rag-pipeline` |
| `security-governance/` | `llmops-security-governance` |

The original repositories are archived. They stay readable, and each README
points here.

## Authorship

Human thought, machine hand. The author set the direction, took the decisions
and reviewed the result; an AI assistant produced the drafting, the code and the
prose in these files. Mistakes are the author's.

## License

MIT. See [LICENSE](LICENSE).
