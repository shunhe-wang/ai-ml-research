from rule_carryover.domain import Decision
from rule_carryover.scoring import extract_decision_sensitivity, score_response


def test_strict_scorer_separates_correctness_from_schema_validity() -> None:
    gold = Decision(
        label="APPROVE",
        rule_id="general_eligibility",
        margin=100,
        trace=("general_eligibility",),
    )

    score = score_response(
        '{"decision":"APPROVE","rule_id":"general_eligibility","margin":100}',
        gold,
    )

    assert score.schema_valid is True
    assert score.decision_correct is True
    assert score.rule_correct is True
    assert score.margin_correct is True
    assert score.error_type is None


def test_schema_invalid_response_is_incorrect_but_can_have_sensitivity_extraction() -> None:
    gold = Decision(
        label="DENY",
        rule_id="benefit_default_deny",
        margin=-50,
        trace=("benefit_default_deny",),
    )
    raw = "I would DENY this case because the income is too high."

    score = score_response(raw, gold)

    assert score.schema_valid is False
    assert score.decision_correct is False
    assert score.error_type == "schema_invalid"
    assert extract_decision_sensitivity(raw) == "DENY"


def test_refusal_is_reported_separately() -> None:
    gold = Decision(
        label="DENY",
        rule_id="fraud_hard_block",
        margin=-1,
        trace=("fraud_hard_block",),
    )

    score = score_response("I cannot make this decision.", gold)

    assert score.refusal is True
    assert score.error_type == "refusal"
    assert score.decision_correct is False


def test_strict_scorer_rejects_extra_rationale_key() -> None:
    gold = Decision(
        label="APPROVE",
        rule_id="general_eligibility",
        margin=0,
        trace=("general_eligibility",),
    )

    score = score_response(
        '{"decision":"APPROVE","rule_id":"general_eligibility","margin":0,'
        '"rationale":["extra"]}',
        gold,
    )

    assert score.schema_valid is False
    assert score.error_type == "schema_invalid"
