# Design decisions

One entry per non-obvious choice: what was decided, why, and what was rejected.
`README.md` says what exists; this file says why it exists this way. Nothing here
is a plan, only decisions already in force.

## 1. A provider-neutral case format, not a harness fork

- **Decided by:** Human.
- **Choice:** a case is `Case(case_id, expected, actual)`; the suite scores cases,
  it does not run models.
- **Why:** keeping generation outside the scorer means the same case set can score
  any provider, any prompt version and any cached response, and the suite stays
  usable when the provider changes.
- **Rejected:** binding the format to one provider's response objects.

## 2. The baseline scorer is deterministic and offline

- **Decided by:** Joint.
- **Choice:** exact match plus token overlap, no model call, no network call.
- **Why:** a metric that changes between runs cannot gate a regression. The
  baseline has to be reproducible on a laptop and in CI.
- **Rejected:** an LLM judge as the default scorer.

## 3. Thresholds are explicit, and a regression fails

- **Decided by:** Human.
- **Choice:** `regression_passes()` takes minimum thresholds per metric.
- **Why:** a score that is only printed gets eyeballed and then ignored. A named
  threshold turns "the numbers look fine" into a pass or a failure.
- **Rejected:** storing a baseline and comparing deltas, which hides the absolute
  quality level.

## 4. Known ceiling: token overlap is a weak proxy

- **Decided by:** Joint.
- **Choice:** token overlap ships as a baseline metric with its weakness stated.
- **Why:** it is useful for detecting gross regressions and useless for judging
  paraphrase or correctness. Saying so is cheaper than being trusted and wrong.
- **Upgrade path:** model-graded metrics and RAG faithfulness/context metrics, as
  the roadmap lists them.

## 5. Evaluators stay out of the dependency graph

- **Decided by:** Human.
- **Choice:** lm-evaluation-harness, Promptfoo and experiment tracking are planned
  adapters, not required dependencies.
- **Why:** a reference suite that cannot run without installing a framework is a
  framework. `python3 -m unittest discover -s tests -v` has to be the whole
  entry point.
- **Rejected:** vendoring a harness or pinning a tracking service.

## 6. Results are machine-readable on purpose

- **Decided by:** Human.
- **Choice:** `evaluate_cases()` returns per-case and aggregate metrics as data.
- **Why:** CI and later adapters consume the result; a human-readable table is a
  rendering of it, not the interface.
- **Rejected:** printing a report as the only output.

## 7. No named identity, no machine paths, no credentials in the public tree

- **Decided by:** Human.
- **Choice:** cases are synthetic, and the only identity in the tree is the
  copyright holder's public handle.
- **Why:** the suite is meant to be read and reused by strangers. The
  contribution boundary is stated in `GOVERNANCE.md` and enforced by review.
- **Rejected:** committing a case set extracted from production traffic.

## 8. Precision and recall, not token presence

- **Decided by:** Human, after an external review.
- **Choice:** `token_scores()` reports precision, recall and F1 over token sets;
  `mean_token_f1` is the aggregate and the regression gate.
- **Why:** the old `token_overlap` was recall in disguise: the expected word
  appearing anywhere scored 1.0, so "No, it is not Paris, it is Lyon" passed a
  `min_token_overlap=1.0` gate. A metric that gives full marks to a wrong answer
  is worse than no metric, because it gets trusted.
- **Rejected:** keeping the name and raising the threshold. The number was
  saturated, not mis-tuned.
- **Still out of scope:** negation and paraphrase. A lexical metric cannot see
  them. `exact_match` stays the honest signal for short factual answers, and the
  semantic layer is on the roadmap.

