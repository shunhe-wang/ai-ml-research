from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

from rule_carryover.rendering import Boundary, Channel

type Streak = Literal["positive", "negative", "balanced", "neutral"]


@dataclass(frozen=True, order=True)
class ExperimentCell:
    target_id: str
    history_id: str
    channel: Channel
    boundary: Boundary
    streak: Streak
    horizon: int
    model_id: str

    def payload(self) -> dict[str, object]:
        return {
            "target_id": self.target_id,
            "history_id": self.history_id,
            "channel": self.channel.value,
            "boundary": self.boundary.value,
            "streak": self.streak,
            "horizon": self.horizon,
            "model_id": self.model_id,
        }


@dataclass(frozen=True)
class FrozenManifest:
    protocol_version: str
    seed: int
    cells: tuple[ExperimentCell, ...]
    manifest_hash: str

    def canonical_json(self) -> str:
        payload = {
            "protocol_version": self.protocol_version,
            "seed": self.seed,
            "cells": [cell.payload() for cell in self.cells],
            "manifest_hash": self.manifest_hash,
        }
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _hash_payload(protocol_version: str, seed: int, cells: tuple[ExperimentCell, ...]) -> str:
    payload = {
        "protocol_version": protocol_version,
        "seed": seed,
        "cells": [cell.payload() for cell in cells],
    }
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(encoded.encode()).hexdigest()


def freeze_manifest(
    *,
    protocol_version: str,
    seed: int,
    cells: Iterable[ExperimentCell],
) -> FrozenManifest:
    frozen_cells = tuple(sorted(cells))
    if not frozen_cells:
        raise ValueError("manifest requires at least one cell")
    if len(set(frozen_cells)) != len(frozen_cells):
        raise ValueError("manifest contains a duplicate experiment cell")
    for cell in frozen_cells:
        if cell.horizon <= 0:
            raise ValueError("horizon must be positive")
        if "latest" in cell.model_id.casefold():
            raise ValueError(f"mutable model alias is prohibited: {cell.model_id}")
    digest = _hash_payload(protocol_version, seed, frozen_cells)
    return FrozenManifest(
        protocol_version=protocol_version,
        seed=seed,
        cells=frozen_cells,
        manifest_hash=digest,
    )
