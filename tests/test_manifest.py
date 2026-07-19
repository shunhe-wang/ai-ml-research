import pytest

from rule_carryover.manifest import ExperimentCell, freeze_manifest
from rule_carryover.rendering import Boundary, Channel


def _cells() -> tuple[ExperimentCell, ...]:
    return (
        ExperimentCell(
            target_id="target-b",
            history_id="history-negative",
            channel=Channel.GOLD_LABEL,
            boundary=Boundary.FULL,
            streak="negative",
            horizon=4,
            model_id="local/qwen3.5-4b@c7429d5",
        ),
        ExperimentCell(
            target_id="target-a",
            history_id="history-positive",
            channel=Channel.GOLD_LABEL,
            boundary=Boundary.FULL,
            streak="positive",
            horizon=4,
            model_id="local/qwen3.5-4b@c7429d5",
        ),
    )


def test_manifest_hash_is_canonical_and_order_independent() -> None:
    forward = freeze_manifest(protocol_version="f1-v0", seed=17, cells=_cells())
    reverse = freeze_manifest(protocol_version="f1-v0", seed=17, cells=reversed(_cells()))

    assert forward.manifest_hash == reverse.manifest_hash
    assert forward.canonical_json() == reverse.canonical_json()
    assert [cell.target_id for cell in forward.cells] == ["target-a", "target-b"]


def test_manifest_rejects_duplicate_cells_and_mutable_model_aliases() -> None:
    cell = _cells()[0]
    with pytest.raises(ValueError, match="duplicate"):
        freeze_manifest(protocol_version="f1-v0", seed=17, cells=(cell, cell))

    mutable = ExperimentCell(
        target_id="target-a",
        history_id="history-a",
        channel=Channel.NEUTRAL,
        boundary=Boundary.FULL,
        streak="balanced",
        horizon=1,
        model_id="provider/model-latest",
    )
    with pytest.raises(ValueError, match="mutable"):
        freeze_manifest(protocol_version="f1-v0", seed=17, cells=(mutable,))
