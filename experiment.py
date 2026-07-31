from dataclasses import dataclass

@dataclass(frozen=True)
class DatasetRecord:
    dataset_id: str
    license: str
    sha256: str
    examples: int

def validate(record: DatasetRecord) -> None:
    if not record.dataset_id or not record.license or len(record.sha256) != 64:
        raise ValueError("dataset_id, license and a SHA-256 checksum are required")
    if record.examples < 1:
        raise ValueError("dataset must contain at least one example")
