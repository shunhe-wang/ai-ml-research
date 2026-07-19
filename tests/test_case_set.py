from pathlib import Path

from rule_carryover.case_set import freeze_case_set, load_case_set, write_case_set
from rule_carryover.domain import RuleSchema
from rule_carryover.generation import generate_balanced_cases


def test_case_set_round_trip_preserves_hash_and_solver_labels(tmp_path: Path) -> None:
    schema = RuleSchema.permit(schema_id="case-set-example", minimum_safety_score=7)
    cases = generate_balanced_cases(schema, per_label=4, seed=41)

    frozen = freeze_case_set(schema, reversed(cases))
    output = tmp_path / "cases.json"
    write_case_set(output, frozen)
    loaded = load_case_set(output)

    assert loaded == frozen
    assert loaded.case_set_hash == frozen.case_set_hash
    assert [item.case.case_id for item in loaded.items] == sorted(
        case.case_id for case in cases
    )
