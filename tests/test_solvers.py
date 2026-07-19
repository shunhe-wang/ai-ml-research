from rule_carryover.domain import Case, RuleSchema
from rule_carryover.solvers import solve_declarative, solve_imperative


def test_benefit_exception_overrides_the_general_threshold() -> None:
    schema = RuleSchema.benefit(
        schema_id="benefit-worked-example",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )
    case = Case(
        case_id="benefit-exception",
        world="benefit",
        facts={
            "income": 2_200,
            "residency_months": 10,
            "has_sanction": False,
            "is_caregiver": True,
        },
    )

    expected = ("APPROVE", "caregiver_exception", 100)

    imperative = solve_imperative(schema, case)
    declarative = solve_declarative(schema, case)

    assert (imperative.label, imperative.rule_id, imperative.margin) == expected
    assert declarative == imperative


def test_permit_hard_block_has_priority_over_emergency_exception() -> None:
    schema = RuleSchema.permit(
        schema_id="permit-worked-example",
        minimum_safety_score=7,
    )
    case = Case(
        case_id="permit-hard-block",
        world="permit",
        facts={
            "safety_score": 10,
            "fee_paid": False,
            "has_insurance": True,
            "restricted_zone": True,
            "emergency_waiver": True,
            "fraud_flag": True,
        },
    )

    expected = ("DENY", "fraud_hard_block", -1)

    imperative = solve_imperative(schema, case)
    declarative = solve_declarative(schema, case)

    assert (imperative.label, imperative.rule_id, imperative.margin) == expected
    assert declarative == imperative
