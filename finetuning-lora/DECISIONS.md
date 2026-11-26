# Design decisions

One entry per non-obvious choice: what was decided, why, and what was rejected.
`README.md` says what exists; this file says why it exists this way. Nothing here
is a plan, only decisions already in force.

## 1. Contracts before GPU hours

- **Decided by:** Human.
- **Choice:** the dataset manifest, its validation and an example experiment
  configuration ship first; the training adapter comes later.
- **Why:** the expensive and irreversible part of fine-tuning is the data and the
  configuration record. Writing the contract first makes a failed run
  reproducible instead of anecdotal.
- **Rejected:** starting from a training script and documenting it afterwards.

## 2. Training data lives outside the repository

- **Decided by:** Human.
- **Choice:** commit manifests, checksums, licenses and synthetic fixtures. Never
  datasets, never model weights.
- **Why:** datasets carry licensing and privacy obligations that a git history
  cannot honour or revoke, and weights are build outputs, not source.
- **Rejected:** a small sample dataset committed for convenience.

## 3. Validation is enforced in code, not in a checklist

- **Decided by:** Joint.
- **Choice:** `validate()` rejects a record without a `dataset_id`, a `license`, a
  64-character SHA-256 checksum, or at least one example.
- **Why:** a manifest that is not checked drifts from the data it describes. The
  checksum is the only way to notice that the file changed under the manifest.
- **Rejected:** a documented convention with no executable check.

## 4. Provider-neutral scaffold

- **Decided by:** Human.
- **Choice:** no trainer-specific dependency until the adapter exists.
- **Why:** Transformers, PEFT and quantization choices age quickly, and a
  scaffold pinned to one of them would date the whole repository. The manifest
  format is the part meant to survive.
- **Rejected:** committing a pinned training environment with no adapter to run.

## 5. Dataset licensing and contamination checks are an open item

- **Decided by:** Human.
- **Choice:** both are listed as unchecked roadmap items rather than assumed.
- **Why:** the framework currently records a license string; it does not verify
  that the data matches it, nor that evaluation sets were kept out of training.
  Both are real gaps and naming them is the honest position.
- **Rejected:** treating the license field as sufficient provenance.

## 6. Standard library only, tested in CI

- **Decided by:** Joint.
- **Choice:** `python3 -m unittest discover -s tests -v` runs on Python 3.12 in
  CI with a read-only token.
- **Why:** the parts that can be tested without hardware are exactly the contracts
  above, so the suite runs everywhere and stays fast.
- **Rejected:** gating CI on GPU availability.

## 7. No named identity, no machine paths, no credentials in the public tree

- **Decided by:** Human.
- **Choice:** fixtures are synthetic and the only identity in the tree is the
  copyright holder's public handle.
- **Why:** the scaffold is meant to be read and reused by strangers. The
  contribution boundary is stated in `GOVERNANCE.md` and enforced by review.
- **Rejected:** committing a manifest that names internal systems.

## 8. Parameter accounting is part of the contract

- **Decided by:** Human, after an external review.
- **Choice:** `LoraPlan` validates rank, alpha, dropout and target modules,
  `adapter_parameters()` computes `rank * (in_features + out_features)` per
  targeted linear layer, and `plan_summary()` reports base parameters, adapter
  parameters and the adapter's share of the total.
- **Why:** the manifest contract validated a checksum by length alone, so 64
  characters of anything passed, and the configuration existed only as prose. The
  number that decides whether an experiment is feasible is arithmetic: it belongs
  in a tested function, not in a sentence.
- **Rejected:** shipping a training adapter to prove the point. It needs GPU
  dependencies and is already on the roadmap; the contract has to be right first.

