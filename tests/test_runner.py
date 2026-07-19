from rule_carryover.domain import Case, RuleSchema
from rule_carryover.providers import ScriptedProvider, TransportError
from rule_carryover.rendering import Boundary, Channel, render_request
from rule_carryover.runner import execute_once
from rule_carryover.solvers import solve_imperative


def _request_fixture() -> tuple[object, object]:
    schema = RuleSchema.permit(
        schema_id="runner-example",
        minimum_safety_score=7,
    )
    target = Case(
        case_id="runner-target",
        world="permit",
        facts={
            "safety_score": 8,
            "fee_paid": True,
            "has_insurance": True,
            "restricted_zone": False,
            "emergency_waiver": False,
            "fraud_flag": False,
        },
    )
    request = render_request(
        schema,
        target,
        (),
        channel=Channel.NEUTRAL,
        boundary=Boundary.FRESH,
    )
    return request, solve_imperative(schema, target)


def test_runner_preserves_request_response_and_exact_score() -> None:
    request, gold = _request_fixture()
    provider = ScriptedProvider(
        ['{"decision":"APPROVE","rule_id":"general_permit","margin":1}']
    )

    record = execute_once(
        provider=provider,
        provider_name="scripted",
        model_id="scripted/model@v1",
        request=request,
        gold=gold,
        decoding={"temperature": 0},
    )

    assert record.request_hash
    assert record.response_hash
    assert record.raw_response is not None
    assert record.score is not None and record.score.decision_correct is True
    assert record.transport_error is None
    assert record.started_at <= record.completed_at
    assert record.latency_ms >= 0


def test_transport_failure_is_retained_and_not_scored() -> None:
    request, gold = _request_fixture()
    provider = ScriptedProvider([TransportError("temporary unavailable")])

    record = execute_once(
        provider=provider,
        provider_name="scripted",
        model_id="scripted/model@v1",
        request=request,
        gold=gold,
        decoding={"temperature": 0},
    )

    assert record.raw_response is None
    assert record.response_hash is None
    assert record.score is None
    assert record.transport_error == "temporary unavailable"
    assert record.started_at <= record.completed_at
    assert record.latency_ms >= 0
