# LLMOps LoRA Fine-tuning

A provider-neutral scaffold for documenting and benchmarking parameter-efficient fine-tuning experiments. It starts with the contracts that make experiments reproducible before adding GPU-heavy training dependencies.

## Roadmap

- [x] dataset manifest and validation contract
- [x] experiment configuration example
- [x] LoRA/QLoRA parameter accounting (trainable parameters, scaling, adapter share)
- [ ] Transformers + PEFT training adapter
- [ ] quantized inference benchmark
- [ ] loss and resource report
- [ ] dataset licensing and contamination checks

## Design

Training data is external to the repository by default. Commit manifests, checksums, licenses and synthetic fixtures, never private datasets or model weights.

## Run

```bash
python3 -m unittest discover -s tests -v
```

## Authorship

Human thought, machine hand. The author set the direction, took the decisions and reviewed the result; an AI assistant produced the drafting, the code and the prose in this file. Mistakes are the author's.
