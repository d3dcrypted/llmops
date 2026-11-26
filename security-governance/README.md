# LLMOps Security and Governance

A small input filter for LLM applications, written as a baseline to measure against. It treats security as an application boundary: classify inputs, apply policy, redact sensitive values, and retain auditable decisions without storing raw secrets.

## Roadmap

- [x] deterministic baseline policy checks, English and Italian phrasings
- [x] PII redaction for email, IBAN, phone and key-shaped secrets
- [x] append-only decision log (input hash, never the input)
- [ ] prompt-injection evaluation corpus
- [ ] provider-independent guardrail adapters
- [ ] retention and access-control reference
- [ ] red-team CI checks

## Run

```bash
python3 -m unittest discover -s tests -v
```

## Limits

The injection check is a list of known phrasings in two languages. It catches the
common wording and misses paraphrase, misspelling and any other language;
`tests/test_controls.py::test_known_misses` keeps three of those misses on record.
Treat a match as a signal to log and review, and do not treat a pass as safe input.
Redaction covers email, checksum-valid IBANs, Italian-shaped phone numbers and a
few key formats. It over-redacts digit runs that look like phone numbers and does
not cover card numbers, tax codes or names.

This is not a security certification or a substitute for threat modeling and human review.

## Authorship

Human thought, machine hand. The author set the direction, took the decisions and reviewed the result; an AI assistant produced the drafting, the code and the prose in this file. Mistakes are the author's.
