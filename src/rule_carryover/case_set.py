from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from rule_carryover.domain import Case, Decision, FactValue, RuleSchema, World
from rule_carryover.solvers import solve_declarative, solve_imperative


@dataclass(frozen=True)
class FrozenCase:
    case: Case
    decision: Decision

    def payload(self) -> dict[str, object]:
        return {
            "case": {
                "case_id": self.case.case_id,
                "world": self.case.world,
                "facts": dict(self.case.facts),
            },
            "decision": {
                "label": self.decision.label,
                "rule_id": self.decision.rule_id,
                "margin": self.decision.margin,
                "trace": list(self.decision.trace),
            },
        }


@dataclass(frozen=True)
class FrozenCaseSet:
    schema: RuleSchema
    items: tuple[FrozenCase, ...]
    case_set_hash: str

    def payload_without_hash(self) -> dict[str, object]:
        return {
            "schema": {
                "schema_id": self.schema.schema_id,
                "world": self.schema.world,
                "parameters": dict(self.schema.parameters),
            },
            "items": [item.payload() for item in self.items],
        }

    def canonical_json(self) -> str:
        payload = self.payload_without_hash() | {"case_set_hash": self.case_set_hash}
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def select_label_stratified(
    case_set: FrozenCaseSet, limit: int | None
) -> tuple[FrozenCase, ...]:
    """Select a deterministic, alternating label-balanced prefix when bounded."""
    if limit is None or limit >= len(case_set.items):
        return case_set.items
    if limit <= 0:
        raise ValueError("case selection limit must be positive")
    buckets = {
        label: [item for item in case_set.items if item.decision.label == label]
        for label in ("APPROVE", "DENY")
    }
    selected: list[FrozenCase] = []
    index = 0
    while len(selected) < limit:
        added = False
        for label in ("APPROVE", "DENY"):
            if index < len(buckets[label]) and len(selected) < limit:
                selected.append(buckets[label][index])
                added = True
        if not added:
            break
        index += 1
    if len(selected) != limit:
        raise ValueError("case selection limit exceeds available targets")
    return tuple(selected)


def _canonical_digest(payload: dict[str, object]) -> str:
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()


def freeze_case_set(schema: RuleSchema, cases: Iterable[Case]) -> FrozenCaseSet:
    ordered = tuple(sorted(cases, key=lambda case: case.case_id))
    if not ordered:
        raise ValueError("case set cannot be empty")
    if len({case.case_id for case in ordered}) != len(ordered):
        raise ValueError("case set contains duplicate case IDs")

    items = []
    for case in ordered:
        imperative = solve_imperative(schema, case)
        declarative = solve_declarative(schema, case)
        if imperative != declarative:
            raise ValueError(f"solver disagreement for {case.case_id}")
        items.append(FrozenCase(case=case, decision=imperative))

    placeholder = FrozenCaseSet(schema=schema, items=tuple(items), case_set_hash="")
    digest = _canonical_digest(placeholder.payload_without_hash())
    return FrozenCaseSet(schema=schema, items=tuple(items), case_set_hash=digest)


def write_case_set(path: Path, case_set: FrozenCaseSet) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(case_set.canonical_json(), encoding="utf-8")


def _parse_case(raw: dict[str, Any]) -> Case:
    facts_raw = cast(dict[str, Any], raw["facts"])
    facts: dict[str, FactValue] = {}
    for key, value in facts_raw.items():
        if not isinstance(value, (bool, int)):
            raise ValueError(f"invalid fact value for {key}")
        facts[key] = value
    return Case(
        case_id=str(raw["case_id"]),
        world=cast(World, raw["world"]),
        facts=facts,
    )


def _parse_decision(raw: dict[str, Any]) -> Decision:
    label = raw["label"]
    if label not in {"APPROVE", "DENY"}:
        raise ValueError("invalid decision label")
    trace_raw = cast(list[Any], raw["trace"])
    if not all(isinstance(item, str) for item in trace_raw):
        raise ValueError("invalid decision trace")
    return Decision(
        label=cast(Any, label),
        rule_id=str(raw["rule_id"]),
        margin=int(raw["margin"]),
        trace=tuple(trace_raw),
    )


def load_case_set(path: Path) -> FrozenCaseSet:
    raw = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    schema_raw = cast(dict[str, Any], raw["schema"])
    parameters_raw = cast(dict[str, Any], schema_raw["parameters"])
    schema = RuleSchema(
        schema_id=str(schema_raw["schema_id"]),
        world=cast(World, schema_raw["world"]),
        parameters={key: int(value) for key, value in parameters_raw.items()},
    )
    items_raw = cast(list[dict[str, Any]], raw["items"])
    cases = [_parse_case(cast(dict[str, Any], item["case"])) for item in items_raw]
    frozen = freeze_case_set(schema, cases)
    stored_hash = str(raw["case_set_hash"])
    if frozen.case_set_hash != stored_hash:
        raise ValueError("case set hash mismatch")
    stored_decisions = [
        _parse_decision(cast(dict[str, Any], item["decision"])) for item in items_raw
    ]
    if [item.decision for item in frozen.items] != stored_decisions:
        raise ValueError("stored decisions do not match both solvers")
    return frozen
