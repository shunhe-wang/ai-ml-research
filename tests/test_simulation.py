from rule_carryover.simulation import (
    estimate_paired_risk_difference,
    evaluate_design,
    evaluate_discordance_design,
    evaluate_panel_design,
    simulate_paired_binary,
)


def test_paired_simulation_recovers_injected_directional_effect() -> None:
    outcomes = simulate_paired_binary(
        targets=10_000,
        negative_history_probability=0.20,
        directional_risk_difference=0.10,
        seed=20260717,
    )

    estimate = estimate_paired_risk_difference(outcomes)

    assert abs(estimate.risk_difference - 0.10) < 0.02
    assert estimate.ci_low < 0.10 < estimate.ci_high
    assert estimate.n_targets == 10_000


def test_zero_effect_uses_shared_paired_outcomes() -> None:
    outcomes = simulate_paired_binary(
        targets=100,
        negative_history_probability=0.50,
        directional_risk_difference=0.0,
        seed=3,
    )

    assert all(row.positive == row.negative for row in outcomes)
    assert estimate_paired_risk_difference(outcomes).risk_difference == 0.0


def test_design_evaluation_reports_type_one_error_power_and_coverage() -> None:
    null = evaluate_design(
        targets=400,
        negative_history_probability=0.50,
        directional_risk_difference=0.0,
        pair_coupling=0.50,
        replications=1_000,
        seed=7,
    )
    alternative = evaluate_design(
        targets=400,
        negative_history_probability=0.50,
        directional_risk_difference=0.10,
        pair_coupling=0.50,
        replications=1_000,
        seed=8,
    )

    assert null.rejection_rate < 0.10
    assert 0.90 < null.coverage < 1.0
    assert alternative.rejection_rate > 0.80
    assert 0.90 < alternative.coverage < 1.0


def test_discordance_calibrated_design_uses_exact_paired_test() -> None:
    null = evaluate_discordance_design(
        targets=240,
        discordance_probability=0.10,
        directional_risk_difference=0.0,
        replications=2_000,
        seed=81,
    )
    alternative = evaluate_discordance_design(
        targets=240,
        discordance_probability=0.10,
        directional_risk_difference=0.05,
        replications=2_000,
        seed=82,
    )

    assert null.rejection_rate <= 0.06
    assert alternative.rejection_rate > null.rejection_rate
    assert abs(alternative.mean_estimate - 0.05) < 0.01
    assert 0.08 < alternative.mean_discordance_rate < 0.12


def test_panel_design_exposes_pooled_power_without_sign_stability() -> None:
    homogeneous = evaluate_panel_design(
        targets_per_cell=400,
        discordance_probabilities=(0.10, 0.10, 0.10, 0.10),
        directional_risk_differences=(0.05, 0.05, 0.05, 0.05),
        replications=1_000,
        seed=91,
    )
    heterogeneous = evaluate_panel_design(
        targets_per_cell=400,
        discordance_probabilities=(0.15, 0.15, 0.15, 0.15),
        directional_risk_differences=(0.10, 0.10, 0.10, -0.10),
        replications=1_000,
        seed=92,
    )

    assert homogeneous.pooled_rejection_rate > 0.99
    assert homogeneous.sign_consistent_rejection_rate > 0.90
    assert heterogeneous.pooled_rejection_rate > 0.95
    assert heterogeneous.any_negative_cell_rate > 0.99
    assert heterogeneous.sign_consistent_rejection_rate < 0.01
    assert len(heterogeneous.mean_cell_estimates) == 4


def test_panel_design_controls_pooled_null_rejection() -> None:
    null = evaluate_panel_design(
        targets_per_cell=240,
        discordance_probabilities=(0.10, 0.10, 0.20, 0.20),
        directional_risk_differences=(0.0, 0.0, 0.0, 0.0),
        replications=2_000,
        seed=93,
    )

    assert null.pooled_rejection_rate <= 0.06
    assert abs(null.mean_pooled_estimate) < 0.01
