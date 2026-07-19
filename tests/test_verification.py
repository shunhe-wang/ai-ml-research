from rule_carryover.domain import RuleSchema
from rule_carryover.verification import crosscheck_schema


def test_boundary_grid_crosscheck_covers_both_labels_without_disagreement() -> None:
    benefit = RuleSchema.benefit(
        schema_id="benefit-crosscheck",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )
    permit = RuleSchema.permit(schema_id="permit-crosscheck", minimum_safety_score=7)

    reports = (crosscheck_schema(benefit), crosscheck_schema(permit))

    assert all(report.checked >= 100 for report in reports)
    assert all(report.disagreements == () for report in reports)
    assert all(set(report.label_counts) == {"APPROVE", "DENY"} for report in reports)
