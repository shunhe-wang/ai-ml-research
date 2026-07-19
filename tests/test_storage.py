import json
from pathlib import Path

import pytest

from rule_carryover.domain import Case, RuleSchema
from rule_carryover.providers import ScriptedProvider
from rule_carryover.rendering import Boundary, Channel, render_request
from rule_carryover.runner import execute_once
from rule_carryover.solvers import solve_imperative
from rule_carryover.storage import StoredExecution, append_execution


def test_append_execution_preserves_complete_request_response_and_score(tmp_path: Path) -> None:
    schema = RuleSchema.permit(schema_id="storage-example", minimum_safety_score=7)
    target = Case(
        case_id="storage-target",
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
    gold = solve_imperative(schema, target)
    request = render_request(
        schema,
        target,
        (),
        channel=Channel.NEUTRAL,
        boundary=Boundary.FRESH,
    )
    record = execute_once(
        provider=ScriptedProvider(
            ['{"decision":"APPROVE","rule_id":"general_permit","margin":1}']
        ),
        provider_name="scripted",
        model_id="scripted/model@v1",
        request=request,
        gold=gold,
        decoding={"temperature": 0},
    )
    execution = StoredExecution(
        run_id="run-1",
        cell_id="cell-1",
        attempt_id="attempt-1",
        parent_attempt_id=None,
        request=request,
        gold=gold,
        record=record,
    )
    output = tmp_path / "executions.jsonl"

    append_execution(output, execution)

    payload = json.loads(output.read_text().strip())
    assert payload["request"]["system"] == request.system_block
    assert payload["record"]["raw_response"] == record.raw_response
    assert payload["record"]["score"]["decision_correct"] is True
    assert payload["record"]["request_hash"] == record.request_hash
    assert "provider_prompt_hash" in payload["record"]
    assert "provider_prompt" in payload["record"]

    with pytest.raises(ValueError, match="duplicate attempt"):
        append_execution(output, execution)
