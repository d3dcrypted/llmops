# LLMOps RAG Pipeline

A small, transparent retrieval-augmented generation reference implementation. The first milestone focuses on deterministic ingestion, chunking, retrieval, citations, and testable interfaces rather than framework abstraction.

## Roadmap

- [x] deterministic text chunking
- [x] source metadata and citation objects
- [x] dependency-free baseline retriever
- [ ] embedding-backed retrieval
- [ ] generation adapter
- [ ] faithfulness and context-precision evaluation
- [ ] REST API and container deployment

## Run

```bash
python3 -m unittest discover -s tests -v
```

The examples are synthetic. Do not place confidential documents, credentials, or production data in this repository.

## License

MIT
