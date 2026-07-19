import pytest

from rule_carryover.domain import Case, RuleSchema
from rule_carryover.rendering import (
    Boundary,
    Channel,
    HistoryRecord,
    render_request,
    whitespace_tokens,
    with_exact_token_count,
)
from rule_carryover.solvers import solve_imperative


def _fixture() -> tuple[RuleSchema, Case, tuple[HistoryRecord, ...]]:
    schema = RuleSchema.benefit(
        schema_id="rendering-example",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )
    target = Case(
        case_id="target-1",
        world="benefit",
        facts={
            "income": 1_900,
            "residency_months": 12,
            "has_sanction": False,
            "is_caregiver": False,
        },
    )
    prior = Case(
        case_id="prior-1",
        world="benefit",
        facts={
            "income": 2_100,
            "residency_months": 12,
            "has_sanction": False,
            "is_caregiver": False,
        },
    )
    record = HistoryRecord(case=prior, decision=solve_imperative(schema, prior))
    return schema, target, (record,)


def test_target_and_rule_bytes_are_invariant_across_boundaries() -> None:
    schema, target, records = _fixture()

    requests = [
        render_request(
            schema,
            target,
            records,
            channel=Channel.GOLD_RATIONALE,
            boundary=boundary,
        )
        for boundary in Boundary
    ]

    assert len({request.system_block for request in requests}) == 1
    assert len({request.target_block for request in requests}) == 1
    assert all(request.messages[-1].content == request.target_block for request in requests)


def test_system_block_contains_complete_ordered_rules_and_literal_output_contract() -> None:
    schema, target, records = _fixture()
    request = render_request(
        schema,
        target,
        records,
        channel=Channel.GOLD_LABEL,
        boundary=Boundary.FULL,
    )

    assert "sanction_hard_block" in request.system_block
    assert "caregiver_exception" in request.system_block
    assert "general_eligibility" in request.system_block
    assert '"decision":"APPROVE or DENY"' in request.system_block
    assert "Return exactly one JSON object and no other text" in request.system_block


def test_outcome_code_channel_is_truthful_fixed_width_and_explicitly_mapped() -> None:
    schema, target, negative_records = _fixture()
    positive_case = Case(
        case_id="prior-2",
        world="benefit",
        facts={
            "income": 1_900,
            "residency_months": 12,
            "has_sanction": False,
            "is_caregiver": False,
        },
    )
    positive_records = (
        HistoryRecord(
            case=positive_case,
            decision=solve_imperative(schema, positive_case),
        ),
    )

    positive = render_request(
        schema,
        target,
        positive_records,
        channel=Channel.OUTCOME_CODE,
        boundary=Boundary.FULL,
    )
    negative = render_request(
        schema,
        target,
        negative_records,
        channel=Channel.OUTCOME_CODE,
        boundary=Boundary.FULL,
    )

    assert positive.messages[1].content == "OUTCOME_CODE=1"
    assert negative.messages[1].content == "OUTCOME_CODE=0"
    assert len(positive.messages[1].content) == len(negative.messages[1].content)
    assert "OUTCOME_CODE=1 means APPROVE" in positive.system_block
    assert "OUTCOME_CODE=0 means DENY" in positive.system_block
    assert '"decision":"APPROVE or DENY"' in positive.system_block


def test_permit_system_block_uses_the_frozen_fact_and_parameter_names() -> None:
    schema = RuleSchema.permit(schema_id="permit-rendering-example", minimum_safety_score=7)
    target = Case(
        case_id="permit-target-1",
        world="permit",
        facts={
            "safety_score": 8,
            "fraud_flag": False,
            "emergency_waiver": False,
            "fee_paid": True,
            "has_insurance": True,
            "restricted_zone": False,
        },
    )

    request = render_request(
        schema,
        target,
        (),
        channel=Channel.NEUTRAL,
        boundary=Boundary.FRESH,
    )

    for name in (
        "fraud_flag",
        "emergency_waiver",
        "safety_score",
        "fee_paid",
        "has_insurance",
        "restricted_zone",
        "PARAMETERS.minimum_safety_score",
    ):
        assert name in request.system_block
    assert "has_fraud" not in request.system_block
    assert "has_emergency_waiver" not in request.system_block
    assert "is_restricted" not in request.system_block


def test_assistant_deletion_and_fresh_context_have_literal_semantics() -> None:
    schema, target, records = _fixture()

    deleted = render_request(
        schema,
        target,
        records,
        channel=Channel.GOLD_RATIONALE,
        boundary=Boundary.ASSISTANT_DELETED,
    )
    fresh = render_request(
        schema,
        target,
        records,
        channel=Channel.GOLD_RATIONALE,
        boundary=Boundary.FRESH,
    )

    assert [message.role for message in deleted.messages] == ["user", "user"]
    assert [message.role for message in fresh.messages] == ["user"]


def test_inert_text_can_be_padded_to_a_provider_token_budget() -> None:
    padded = with_exact_token_count(
        "archived neutral record",
        target_tokens=7,
        token_counter=whitespace_tokens,
    )

    assert whitespace_tokens(padded) == 7
    assert padded.startswith("archived neutral record")

    with pytest.raises(ValueError, match="already exceeds"):
        with_exact_token_count(
            "four tokens live here",
            target_tokens=3,
            token_counter=whitespace_tokens,
        )
