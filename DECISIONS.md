# Design decisions

One entry per non-obvious choice: what was decided, why, and what was rejected.
`README.md` says what exists; this file says why it exists this way. Nothing here
is a plan, only decisions already in force.

## 1. A reference implementation, not a product

- **Decided by:** Human.
- **Choice:** the repository is a small, transparent starting point that an
  operator reads, copies and adapts.
- **Why:** the value of a reference implementation is that its behaviour can be
  checked by reading it. A product would need support surface, versioning
  promises and configuration for cases that do not exist yet.
- **Rejected:** shipping a framework with plugin discovery, config files and
  abstractions for retrieval strategies nobody has asked for.

## 2. Standard library only, no framework, no vector database

- **Decided by:** Joint.
- **Choice:** ingestion, chunking and retrieval are plain Python.
- **Why:** the baseline stays deterministic and reviewable, and the test suite
  runs anywhere without a service, a model download or a network call.
- **Rejected:** LangChain or LlamaIndex as the substrate; an embedded vector
  store in the baseline. Embedding-backed retrieval is a roadmap adapter, not a
  hidden requirement.

## 3. Ingestion has an explicit trust boundary

- **Decided by:** Human.
- **Choice:** `ingest_file()` reads one explicitly selected UTF-8 file below an
  operator-provided root. Traversal, symlink targets, non-files and oversized
  inputs are rejected.
- **Why:** a document loader is the point where untrusted input enters the
  pipeline. Validating there is cheaper than validating every consumer
  downstream, and it keeps the failure mode loud.
- **Rejected:** accepting a glob or a directory tree and filtering later.

## 4. A citation carries the retrieved text, not just a pointer

- **Decided by:** Human.
- **Choice:** `retrieve_with_citations()` returns the source, the chunk index
  and the exact retrieved text.
- **Why:** a citation that only names a document cannot be checked without
  trusting the generated prose. Returning the text makes verification a
  comparison instead of an act of faith.
- **Rejected:** storing chunk ids only and re-reading the corpus at display time.

## 5. Tests are the contract, and CI runs them

- **Decided by:** Joint.
- **Choice:** `python3 -m unittest discover -s tests -v` is the entry point, and
  CI runs it on Python 3.12 with a read-only token.
- **Why:** the examples are synthetic, so the tests are the only executable
  description of intended behaviour. A green run is the release condition.
- **Rejected:** example notebooks as the primary demonstration.

## 6. Roadmap items stay unchecked until they exist

- **Decided by:** Human.
- **Choice:** unimplemented capabilities are listed as open boxes in the README
  and named as planned adapters.
- **Why:** an unchecked box is honest and cheap. Prose that implies a capability
  without shipping it is the failure mode this repository is meant to avoid.
- **Rejected:** describing the full target architecture as if it were present.

## 7. No named identity, no machine paths, no credentials in the public tree

- **Decided by:** Human.
- **Choice:** examples are synthetic, environment variables appear as names only,
  and the only identity in the tree is the copyright holder's public handle.
- **Why:** the repository is meant to be readable by a stranger, and a stranger
  should not be able to learn who runs it or where. The contribution boundary is
  stated in `GOVERNANCE.md` and enforced by review.
- **Rejected:** committing a sample corpus from a real environment.
