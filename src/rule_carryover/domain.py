from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

type World = Literal["benefit", "permit"]
type FactValue = int | bool


@dataclass(frozen=True)
class Case:
    case_id: str
    world: World
    facts: Mapping[str, FactValue]


@dataclass(frozen=True)
class Decision:
    label: Literal["APPROVE", "DENY"]
    rule_id: str
    margin: int
    trace: tuple[str, ...]


@dataclass(frozen=True)
class RuleSchema:
    schema_id: str
    world: World
    parameters: Mapping[str, int]

    @classmethod
    def benefit(
        cls,
        *,
        schema_id: str,
        income_ceiling: int,
        residency_months: int,
        caregiver_income_extension: int,
        caregiver_residency_reduction: int,
    ) -> RuleSchema:
        return cls(
            schema_id=schema_id,
            world="benefit",
            parameters={
                "income_ceiling": income_ceiling,
                "residency_months": residency_months,
                "caregiver_income_extension": caregiver_income_extension,
                "caregiver_residency_reduction": caregiver_residency_reduction,
            },
        )

    @classmethod
    def permit(
        cls,
        *,
        schema_id: str,
        minimum_safety_score: int,
    ) -> RuleSchema:
        return cls(
            schema_id=schema_id,
            world="permit",
            parameters={"minimum_safety_score": minimum_safety_score},
        )
