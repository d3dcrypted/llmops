# Design decisions

One entry per non-obvious choice: what was decided, why, and what was rejected.
`README.md` says what exists; this file says why it exists this way. Nothing here
is a plan, only decisions already in force.

## 1. Loopback by default

- **Decided by:** Human.
- **Choice:** the OpenAI-compatible API binds to `127.0.0.1:8001`, Prometheus to
  `127.0.0.1:9090`, Grafana to `127.0.0.1:3000`.
- **Why:** an inference endpoint with no authentication must not be reachable by
  default. Publishing it becomes a deliberate operator action instead of an
  accident of the compose file.
- **Rejected:** binding `0.0.0.0` and documenting that it is unsafe.

## 2. A local demo is labelled a local demo

- **Decided by:** Human.
- **Choice:** the README names what is missing before this is exposed: authentication,
  TLS, resource limits, pinned image digests, non-default credentials, persistent
  dashboards, network policy.
- **Why:** the failure mode of a reference deployment is that it gets promoted to
  production because it started once. The list is the price of that promotion,
  stated up front.
- **Rejected:** shipping a "production-ready" compose file with placeholder secrets.

## 3. Provider- and model-agnostic

- **Decided by:** Human.
- **Choice:** the operator supplies the model artifact (`MODEL_PATH`) and adapts
  the runtime command to their own hardware.
- **Why:** the repository demonstrates the serving and observability boundary.
  Picking a model or a runtime for the reader would make the example useless on
  hardware that differs from the author's.
- **Rejected:** committing a specific model image and quantization preset.

## 4. CI checks the wiring, not running containers

- **Decided by:** Joint.
- **Choice:** `tests/test_layout.py` validates the compose and metrics
  configuration; CI runs `python3 -m unittest discover -s tests -v`.
- **Why:** pulling model images in CI would make the check slow, flaky and
  dependent on a registry. What can break silently here is the wiring between
  services, and that is testable in milliseconds.
- **Rejected:** a smoke test that starts the stack on every push.

## 5. Environment variables appear as names only

- **Decided by:** Human.
- **Choice:** `.env.example` carries variable names with placeholder values, and
  the compose file interpolates `${GRAFANA_ADMIN_PASSWORD:?…}` so a missing value
  stops the stack instead of falling back to a known credential.
- **Why:** a committed default password or token is the most common way a
  reference deployment leaks. The operator fills the values, and
  `tests/test_layout.py` fails if a credential line ever grows a value again.
- **Rejected:** a working `.env` with a demo credential.

## 6. No named identity, no machine paths, no credentials in the public tree

- **Decided by:** Human.
- **Choice:** the only identity in the tree is the copyright holder's public
  handle, and the compose file uses loopback addresses and relative paths.
- **Why:** the deployment is meant to be copied by strangers. The contribution
  boundary is stated in `GOVERNANCE.md` and enforced by review.
- **Rejected:** committing a compose file tuned to one host.

## 7. Images pinned by tag and digest

- **Decided by:** Human, after an external review.
- **Choice:** every image reference carries a tag and a digest. `llama.cpp` is
  pinned to `ghcr.io/ggml-org/llama.cpp:server-b<build>@sha256:...`.
- **Why:** the original reference, `ghcr.io/ggerganov/llama.cpp:server`, does not
  resolve: the images moved to the `ggml-org` namespace. A digest makes the demo
  reproducible and an upgrade a deliberate edit.
- **Correction:** the first fix pinned a `full-<sha>` image from the old namespace
  and stated that upstream publishes no `server` tag. Both were wrong and neither
  had been run: that image dates from March 2023, predates GGUF and has no
  `llama-server`. The current pin was chosen by starting the stack and querying it.
- **Rejected:** `:latest`, and a floating tag with a comment asking operators to
  pin it themselves.

