from rule_carryover.domain import RuleSchema
from rule_carryover.pairs import fact_signature, generate_counterfactual_pairs
from rule_carryover.solvers import solve_imperative


def test_counterfactual_history_pairs_flip_one_decisive_fact() -> None:
    schemas = (
        RuleSchema.benefit(
            schema_id="benefit-pairs",
            income_ceiling=2_000,
            residency_months=12,
            caregiver_income_extension=300,
            caregiver_residency_reduction=2,
        ),
        RuleSchema.permit(schema_id="permit-pairs", minimum_safety_score=7),
    )

    for schema in schemas:
        pairs = generate_counterfactual_pairs(schema, count=12, seed=73)
        assert len(pairs) == 12
        assert len({pair.pair_id for pair in pairs}) == 12
        assert len({fact_signature(pair.negative) for pair in pairs}) == 12
        for pair in pairs:
            differing = {
                key
                for key in pair.positive.facts
                if pair.positive.facts[key] != pair.negative.facts[key]
            }
            assert differing == {pair.changed_fact}
            assert solve_imperative(schema, pair.positive).label == "APPROVE"
            positive = solve_imperative(schema, pair.positive)
            negative = solve_imperative(schema, pair.negative)
            assert negative.label == "DENY"
            assert abs(positive.margin) == abs(negative.margin)


def test_counterfactual_pair_generation_is_seeded() -> None:
    schema = RuleSchema.permit(schema_id="permit-seeded-pairs", minimum_safety_score=7)

    assert generate_counterfactual_pairs(schema, count=5, seed=1) == generate_counterfactual_pairs(
        schema, count=5, seed=1
    )
    assert generate_counterfactual_pairs(schema, count=5, seed=1) != generate_counterfactual_pairs(
        schema, count=5, seed=2
    )


def test_counterfactual_pair_generation_excludes_frozen_target_facts() -> None:
    schema = RuleSchema.permit(schema_id="permit-disjoint-pairs", minimum_safety_score=7)
    initial = generate_counterfactual_pairs(schema, count=2, seed=41)
    excluded = {
        fact_signature(initial[0].positive),
        fact_signature(initial[0].negative),
    }

    regenerated = generate_counterfactual_pairs(
        schema,
        count=2,
        seed=41,
        excluded_fact_signatures=excluded,
    )

    assert all(
        fact_signature(case) not in excluded
        for pair in regenerated
        for case in (pair.positive, pair.negative)
    )


def test_counterfactual_pair_generation_applies_preoutcome_acceptance_filter() -> None:
    schema = RuleSchema.permit(schema_id="permit-filtered-pairs", minimum_safety_score=500)
    initial = generate_counterfactual_pairs(schema, count=1, seed=51)
    rejected = fact_signature(initial[0].positive)

    filtered = generate_counterfactual_pairs(
        schema,
        count=2,
        seed=51,
        pair_filter=lambda pair: fact_signature(pair.positive) != rejected,
    )

    assert all(fact_signature(pair.positive) != rejected for pair in filtered)
