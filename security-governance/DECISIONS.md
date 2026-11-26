# Design decisions

One entry per non-obvious choice: what was decided, why, and what was rejected.
`README.md` says what exists; this file says why it exists this way. Nothing here
is a plan, only decisions already in force.

## 1. The baseline is deterministic, so it can be trusted and tested

- **Decided by:** Human.
- **Choice:** `inspect()` classifies input and redacts sensitive values with
  pattern matching, without a model call.
- **Why:** a guardrail whose verdict changes between runs cannot be reviewed,
  regression-tested or explained after an incident. The deterministic baseline is
  the floor other layers build on.
- **Rejected:** an LLM judge as the primary control.

## 2. Decisions are records, not logs of the input

- **Decided by:** Human.
- **Choice:** `inspect()` returns `Decision(allowed, redacted_text, reasons)`.
- **Why:** a control plane that stores the text it inspected becomes the data
  store it was supposed to protect. The record keeps the verdict and the reason
  codes; the redacted text is what callers may persist.
- **Rejected:** writing raw prompts to an audit table for later review.

## 3. Redaction and the verdict happen in one pass

- **Decided by:** Joint.
- **Choice:** the returned text is already redacted when the decision comes back.
- **Why:** redaction offered as a separate, optional step gets skipped by the
  first caller in a hurry, and then the raw value is in a log. Making it part of
  the return value removes the choice.
- **Rejected:** a `redact()` helper the caller has to remember to call.

## 4. Prompt-injection patterns are named, not scored

- **Decided by:** Joint.
- **Choice:** a detected injection pattern denies the request and adds a reason
  code, rather than producing a risk score.
- **Why:** a score invites a threshold debate. A named pattern is falsifiable,
  and the corpus that expands it is a roadmap item with a visible list.
- **Rejected:** a weighted confidence value with no published calibration.

## 5. Scope limits are stated, not implied

- **Decided by:** Human.
- **Choice:** the README says this is not a security certification and not a
  substitute for threat modeling and human review.
- **Why:** governance scaffolding is easy to mistake for governance. Naming the
  boundary keeps the repository useful without overselling what it enforces.
- **Rejected:** a compliance-mapping table with no control implementation.

## 6. Standard library only, tested in CI

- **Decided by:** Joint.
- **Choice:** `python3 -m unittest discover -s tests -v` on Python 3.12 with a
  read-only token.
- **Why:** the controls are pure functions over text, so they are fully testable
  offline and the suite doubles as the specification of each rule.
- **Rejected:** provider-specific guardrail adapters in the baseline.

## 7. No named identity, no machine paths, no credentials in the public tree

- **Decided by:** Human.
- **Choice:** examples are synthetic and the only identity in the tree is the
  copyright holder's public handle.
- **Why:** the repository is meant to be read and reused by strangers, and a
  security example must not itself leak who runs it. The contribution boundary is
  stated in `GOVERNANCE.md` and enforced by review.
- **Rejected:** sample inputs taken from a real mailbox or ticket queue.
