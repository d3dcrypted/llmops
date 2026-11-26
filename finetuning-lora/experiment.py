from dataclasses import dataclass
import json
from pathlib import Path
import re

SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
SLUG = re.compile(r"\A[a-z0-9][a-z0-9._-]*\Z")
SPDX_ID = re.compile(r"\A[A-Za-z0-9.+-]+\Z")

@dataclass(frozen=True)
class DatasetRecord:
    dataset_id: str
    license: str
    sha256: str
    examples: int

def validate(record: DatasetRecord) -> None:
    """Validate a dataset manifest. The checksum must be real hex, not just 64 characters."""
    if not SLUG.match(record.dataset_id):
        raise ValueError("dataset_id must be a lowercase slug")
    if not SPDX_ID.match(record.license):
        raise ValueError("license must be an SPDX identifier")
    if not SHA256.match(record.sha256):
        raise ValueError("sha256 must be 64 lowercase hexadecimal characters")
    if record.examples < 1:
        raise ValueError("dataset must contain at least one example")

def load_manifest(path: str | Path) -> DatasetRecord:
    record = DatasetRecord(**json.loads(Path(path).read_text(encoding="utf-8")))
    validate(record)
    return record

@dataclass(frozen=True)
class LoraPlan:
    """An experiment configuration: what is trained, how much of it, at what scale."""
    base_model: str
    rank: int = 16
    alpha: int = 32
    dropout: float = 0.05
    target_modules: tuple[str, ...] = ("q_proj", "k_proj", "v_proj", "o_proj")
    quantize_4bit: bool = False

    def scaling(self) -> float:
        """LoRA scaling factor alpha / r applied to the adapter output."""
        return self.alpha / self.rank

    def validate(self) -> None:
        if not self.base_model:
            raise ValueError("base_model is required")
        if type(self.rank) is not int or self.rank < 1 or self.alpha < 1:
            raise ValueError("rank must be an integer >= 1 and alpha >= 1")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("dropout must be in [0, 1)")
        if not self.target_modules:
            raise ValueError("at least one target module is required")
        if any(not SLUG.match(module) for module in self.target_modules):
            raise ValueError("target modules must be lowercase slugs")

def adapter_parameters(plan: LoraPlan, layers: tuple[tuple[str, int, int], ...]) -> int:
    """Trainable parameters: rank * (in_features + out_features) per targeted linear layer."""
    plan.validate()
    targeted = [layer for layer in layers if layer[0] in plan.target_modules]
    if any(plan.rank > min(i, o) for _, i, o in targeted):
        # Above min(in, out) the adapter is no longer low-rank: it has more parameters than the layer.
        raise ValueError("rank exceeds the smallest dimension of a targeted layer")
    return sum(plan.rank * (i + o) for _, i, o in targeted)

def plan_summary(plan: LoraPlan, layers: tuple[tuple[str, int, int], ...]) -> dict:
    """The numbers an experiment record needs before anyone books GPU hours."""
    plan.validate()
    base = sum(in_features * out_features for _, in_features, out_features in layers)
    adapter = adapter_parameters(plan, layers)
    return {"base_model": plan.base_model, "rank": plan.rank, "alpha": plan.alpha,
            "scaling": round(plan.scaling(), 4), "quantize_4bit": plan.quantize_4bit,
            "target_modules": list(plan.target_modules),
            "base_parameters": base, "adapter_parameters": adapter,
            "adapter_share": round(adapter / base, 6) if base else 0.0}

def load_plan(path: str | Path) -> LoraPlan:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    plan = LoraPlan(**{**data, "target_modules": tuple(data.get("target_modules", LoraPlan.target_modules))})
    plan.validate()
    return plan
