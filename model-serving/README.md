# LLMOps Model Serving

A minimal, reproducible reference deployment for serving a local language model behind an OpenAI-compatible API with Prometheus metrics.

## Scope

This repository demonstrates the serving and observability boundary. It is intentionally provider- and model-agnostic: operators supply their own compatible model artifact and adapt the runtime command to their hardware.

## Quick start

Review `docker-compose.yml`, set `MODEL_PATH` to a local model directory and
`GRAFANA_ADMIN_PASSWORD` to a value of your own in `.env`, then run:

```bash
docker compose up -d
curl http://127.0.0.1:8001/health
```

The API is bound to loopback by default. Prometheus is exposed on `127.0.0.1:9090`; Grafana is exposed on `127.0.0.1:3000` for local exploration only.

## Metrics

No dashboard ships with this repository. The intended one tracks time to first token, generation latency, throughput, queue depth, and error rate. The exact metric names depend on the selected server image.

## Production notes

The compose file is a local demo, not a production deployment. Images are pinned
by tag and digest, `llama.cpp` to a `server-b<build>` image whose entrypoint is
`llama-server`. The stack was brought up with a 1 MB GGUF test model: `/health`,
`/v1/chat/completions` and `/metrics` answered and Prometheus reported the target
up. Grafana starts empty: no datasource or dashboard is provisioned. Add authentication, TLS,
resource limits, non-default credentials, persistent dashboards, and network
policy before exposing it beyond a trusted host.

## Authorship

Human thought, machine hand. The author set the direction, took the decisions and reviewed the result; an AI assistant produced the drafting, the code and the prose in this file. Mistakes are the author's.

## License

MIT
