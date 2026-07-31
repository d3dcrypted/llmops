# LLMOps LoRA Fine-tuning

A provider-neutral scaffold for documenting and benchmarking parameter-efficient fine-tuning experiments. It starts with the contracts that make experiments reproducible before adding GPU-heavy training dependencies.

## Roadmap

- [x] dataset manifest and validation contract
- [x] experiment configuration example
- [ ] Transformers + PEFT training adapter
- [ ] quantized inference benchmark
- [ ] loss and resource report
- [ ] dataset licensing and contamination checks

## Design

Training data is external to the repository by default. Commit manifests, checksums, licenses, and synthetic fixtures—not private datasets or model weights.

## Run

```bash
python3 -m unittest discover -s tests -v
```
