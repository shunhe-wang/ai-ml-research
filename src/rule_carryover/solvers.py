from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from rule_carryover.domain import Case, Decision, FactValue, RuleSchema


def _bool(case: Case, name: str) -> bool:
    value = case.facts[name]
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be bool")
    return value


def _int(case: Case, name: str) -> int:
    value = case.facts[name]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int")
    return value


def _decision(label: Literal["APPROVE", "DENY"], rule_id: str, margin: int) -> Decision:
    return Decision(label=label, rule_id=rule_id, margin=margin, trace=(rule_id,))


def solve_imperative(schema: RuleSchema, case: Case) -> Decision:
    """Solve through direct world-specific control flow."""
    if schema.world != case.world:
        raise ValueError("schema and case worlds differ")

    if case.world == "benefit":
        income = _int(case, "income")
        residency = _int(case, "residency_months")
        ceiling = schema.parameters["income_ceiling"]
        required_residency = schema.parameters["residency_months"]

        if _bool(case, "has_sanction"):
            return _decision("DENY", "sanction_hard_block", -1)

        exception_ceiling = ceiling + schema.parameters["caregiver_income_extension"]
        exception_residency = (
            required_residency - schema.parameters["caregiver_residency_reduction"]
        )
        if (
            _bool(case, "is_caregiver")
            and income <= exception_ceiling
            and residency >= exception_residency
        ):
            return _decision("APPROVE", "caregiver_exception", exception_ceiling - income)

        if income <= ceiling and residency >= required_residency:
            return _decision("APPROVE", "general_eligibility", ceiling - income)

        return _decision("DENY", "benefit_default_deny", ceiling - income)

    safety = _int(case, "safety_score")
    minimum = schema.parameters["minimum_safety_score"]
    if _bool(case, "fraud_flag"):
        return _decision("DENY", "fraud_hard_block", -1)

    if (
        _bool(case, "emergency_waiver")
        and safety >= minimum + 1
        and _bool(case, "has_insurance")
    ):
        return _decision("APPROVE", "emergency_exception", safety - (minimum + 1))

    if (
        safety >= minimum
        and _bool(case, "fee_paid")
        and _bool(case, "has_insurance")
        and not _bool(case, "restricted_zone")
    ):
        return _decision("APPROVE", "general_permit", safety - minimum)

    return _decision("DENY", "permit_default_deny", safety - minimum)


Operator = Literal["eq", "le", "ge"]


@dataclass(frozen=True)
class _Predicate:
    fact: str
    operator: Operator
    expected: FactValue

    def holds(self, case: Case) -> bool:
        actual = case.facts[self.fact]
        if self.operator == "eq":
            return actual == self.expected
        if isinstance(actual, bool) or isinstance(self.expected, bool):
            raise TypeError("ordered predicates require integers")
        if self.operator == "le":
            return actual <= self.expected
        return actual >= self.expected


@dataclass(frozen=True)
class _Clause:
    rule_id: str
    label: Literal["APPROVE", "DENY"]
    predicates: tuple[_Predicate, ...]
    margin_fact: str | None = None
    margin_boundary: int = 0
    margin_direction: Literal[-1, 1] = 1
    fixed_margin: int | None = None

    def applies(self, case: Case) -> bool:
        return all(predicate.holds(case) for predicate in self.predicates)

    def margin(self, case: Case) -> int:
        if self.fixed_margin is not None:
            return self.fixed_margin
        if self.margin_fact is None:
            return 0
        value = case.facts[self.margin_fact]
        if isinstance(value, bool):
            raise TypeError("margin fact must be an integer")
        return self.margin_direction * (value - self.margin_boundary)


def _clauses(schema: RuleSchema) -> tuple[_Clause, ...]:
    if schema.world == "benefit":
        ceiling = schema.parameters["income_ceiling"]
        residency = schema.parameters["residency_months"]
        exception_ceiling = ceiling + schema.parameters["caregiver_income_extension"]
        exception_residency = residency - schema.parameters["caregiver_residency_reduction"]
        return (
            _Clause(
                "sanction_hard_block",
                "DENY",
                (_Predicate("has_sanction", "eq", True),),
                fixed_margin=-1,
            ),
            _Clause(
                "caregiver_exception",
                "APPROVE",
                (
                    _Predicate("is_caregiver", "eq", True),
                    _Predicate("income", "le", exception_ceiling),
                    _Predicate("residency_months", "ge", exception_residency),
                ),
                margin_fact="income",
                margin_boundary=exception_ceiling,
                margin_direction=-1,
            ),
            _Clause(
                "general_eligibility",
                "APPROVE",
                (
                    _Predicate("income", "le", ceiling),
                    _Predicate("residency_months", "ge", residency),
                ),
                margin_fact="income",
                margin_boundary=ceiling,
                margin_direction=-1,
            ),
            _Clause(
                "benefit_default_deny",
                "DENY",
                (),
                margin_fact="income",
                margin_boundary=ceiling,
                margin_direction=-1,
            ),
        )

    minimum = schema.parameters["minimum_safety_score"]
    return (
        _Clause(
            "fraud_hard_block",
            "DENY",
            (_Predicate("fraud_flag", "eq", True),),
            fixed_margin=-1,
        ),
        _Clause(
            "emergency_exception",
            "APPROVE",
            (
                _Predicate("emergency_waiver", "eq", True),
                _Predicate("safety_score", "ge", minimum + 1),
                _Predicate("has_insurance", "eq", True),
            ),
            margin_fact="safety_score",
            margin_boundary=minimum + 1,
        ),
        _Clause(
            "general_permit",
            "APPROVE",
            (
                _Predicate("safety_score", "ge", minimum),
                _Predicate("fee_paid", "eq", True),
                _Predicate("has_insurance", "eq", True),
                _Predicate("restricted_zone", "eq", False),
            ),
            margin_fact="safety_score",
            margin_boundary=minimum,
        ),
        _Clause(
            "permit_default_deny",
            "DENY",
            (),
            margin_fact="safety_score",
            margin_boundary=minimum,
        ),
    )


def solve_declarative(schema: RuleSchema, case: Case) -> Decision:
    """Solve by evaluating an ordered declarative clause table."""
    if schema.world != case.world:
        raise ValueError("schema and case worlds differ")
    for clause in _clauses(schema):
        if clause.applies(case):
            return _decision(clause.label, clause.rule_id, clause.margin(case))
    raise AssertionError("every schema must end in a default clause")
