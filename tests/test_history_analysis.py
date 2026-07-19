import json
from pathlib import Path

from rule_carryover.history_analysis import analyze_history_log


def _record(target: str, streak: str, decision: str | None, correct: bool) -> dict[str, object]:
    score = None
    if decision is not None:
        score = {
            "schema_valid": True,
            "parsed_decision": decision,
            "decision_correct": correct,
        }
    return {
        "cell_id": f"{target}|history|{streak}|model",
        "attempt_id": f"{target}-{streak}",
        "record": {"score": score, "transport_error": None},
    }


def test_history_analysis_reports_paired_exact_and_missingness_statistics(
    tmp_path: Path,
) -> None:
    records = [
        _record("t1", "positive", "APPROVE", True),
        _record("t1", "negative", "DENY", True),
        _record("t2", "positive", "APPROVE", True),
        _record("t2", "negative", "APPROVE", True),
        _record("t3", "positive", "DENY", True),
        _record("t3", "negative", "APPROVE", False),
        _record("t4", "positive", None, False),
        _record("t4", "negative", "DENY", True),
    ]
    path = tmp_path / "executions.jsonl"
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n")

    result = analyze_history_log(path, bootstrap_replications=200, seed=31)

    assert result.targets == 4
    assert result.paired_valid == 3
    assert result.positive_only_approve == 1
    assert result.negative_only_approve == 1
    assert result.risk_difference_complete_case == 0.0
    assert result.risk_difference_lower_bound == 0.0
    assert result.risk_difference_upper_bound == 0.25
    assert result.exact_one_sided_p == 0.75
    assert result.exact_two_sided_p == 1.0
    assert result.positive_schema_valid == 3
    assert result.negative_schema_valid == 4
