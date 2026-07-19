from rule_carryover.domain import RuleSchema
from rule_carryover.histories import (
    build_directional_history_bank,
    history_bank_hash,
    pair_is_naturally_token_matched,
)
from rule_carryover.pairs import generate_counterfactual_pairs
from rule_carryover.rendering import Channel, whitespace_tokens


def test_directional_history_twins_use_the_same_counterfactual_pairs() -> None:
    schema = RuleSchema.benefit(
        schema_id="benefit-histories",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )
    pairs = generate_counterfactual_pairs(schema, count=20, seed=2)

    bank = build_directional_history_bank(schema, pairs, sets=4, horizon=6, seed=9)
    rebuilt = build_directional_history_bank(schema, pairs, sets=4, horizon=6, seed=9)

    assert len(bank) == 8
    assert len(history_bank_hash(bank)) == 64
    assert history_bank_hash(bank) == history_bank_hash(rebuilt)
    assert all(
        pair_is_naturally_token_matched(schema, pair, whitespace_tokens)
        for pair in pairs
    )
    by_set: dict[str, dict[str, object]] = {}
    for sequence in bank:
        by_set.setdefault(sequence.set_id, {})[sequence.streak] = sequence
    assert len(by_set) == 4
    for variants in by_set.values():
        positive = variants["positive"]
        negative = variants["negative"]
        assert positive.source_pair_ids == negative.source_pair_ids
        assert all(record.decision.label == "APPROVE" for record in positive.records)
        assert all(record.decision.label == "DENY" for record in negative.records)
        for positive_record, negative_record in zip(
            positive.records, negative.records, strict=True
        ):
            differing = {
                key
                for key in positive_record.case.facts
                if positive_record.case.facts[key] != negative_record.case.facts[key]
            }
            assert len(differing) == 1


def test_outcome_code_channel_removes_literal_label_length_imbalance() -> None:
    schema = RuleSchema.benefit(
        schema_id="coded-history",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )
    pair = generate_counterfactual_pairs(schema, count=1, seed=31)[0]

    assert not pair_is_naturally_token_matched(
        schema,
        pair,
        len,
        channel=Channel.GOLD_LABEL,
    )
    assert pair_is_naturally_token_matched(
        schema,
        pair,
        len,
        channel=Channel.OUTCOME_CODE,
    )
