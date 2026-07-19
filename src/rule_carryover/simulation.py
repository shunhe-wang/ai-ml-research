from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class PairedBinaryOutcome:
    target_index: int
    positive: int
    negative: int


@dataclass(frozen=True)
class PairedRiskDifference:
    risk_difference: float
    standard_error: float
    ci_low: float
    ci_high: float
    n_targets: int


@dataclass(frozen=True)
class OperatingCharacteristics:
    targets: int
    true_risk_difference: float
    pair_coupling: float
    replications: int
    rejection_rate: float
    coverage: float
    mean_estimate: float
    bias: float


@dataclass(frozen=True)
class DiscordanceOperatingCharacteristics:
    targets: int
    discordance_probability: float
    true_risk_difference: float
    replications: int
    rejection_rate: float
    mean_estimate: float
    bias: float
    mean_discordance_rate: float


@dataclass(frozen=True)
class PanelOperatingCharacteristics:
    cells: int
    targets_per_cell: int
    total_targets: int
    discordance_probabilities: tuple[float, ...]
    true_cell_risk_differences: tuple[float, ...]
    true_mean_risk_difference: float
    replications: int
    pooled_rejection_rate: float
    sign_consistent_rejection_rate: float
    any_negative_cell_rate: float
    all_positive_cell_rate: float
    mean_pooled_estimate: float
    mean_cell_estimates: tuple[float, ...]
    cell_rejection_rates: tuple[float, ...]
    mean_discordance_rate: float


def simulate_paired_binary(
    *,
    targets: int,
    negative_history_probability: float,
    directional_risk_difference: float,
    pair_coupling: float = 1.0,
    seed: int,
) -> tuple[PairedBinaryOutcome, ...]:
    """Generate maximally paired binary decisions with a known marginal risk difference."""
    if targets <= 0:
        raise ValueError("targets must be positive")
    positive_probability = negative_history_probability + directional_risk_difference
    if not 0.0 <= negative_history_probability <= 1.0:
        raise ValueError("negative history probability must be in [0, 1]")
    if not 0.0 <= positive_probability <= 1.0:
        raise ValueError("positive history probability must be in [0, 1]")
    if not 0.0 <= pair_coupling <= 1.0:
        raise ValueError("pair_coupling must be in [0, 1]")

    rng = random.Random(seed)
    rows = []
    for index in range(targets):
        shared = rng.random() < pair_coupling
        if shared:
            positive_latent = negative_latent = rng.random()
        else:
            positive_latent = rng.random()
            negative_latent = rng.random()
        rows.append(
            PairedBinaryOutcome(
                target_index=index,
                positive=int(positive_latent < positive_probability),
                negative=int(negative_latent < negative_history_probability),
            )
        )
    return tuple(rows)


def estimate_paired_risk_difference(
    outcomes: Sequence[PairedBinaryOutcome],
    *,
    critical_value: float = 1.959963984540054,
) -> PairedRiskDifference:
    """Estimate a paired marginal risk difference and Wald interval."""
    n = len(outcomes)
    if n < 2:
        raise ValueError("at least two paired targets are required")
    differences = [row.positive - row.negative for row in outcomes]
    effect = sum(differences) / n
    sample_variance = sum((difference - effect) ** 2 for difference in differences) / (n - 1)
    standard_error = math.sqrt(sample_variance / n)
    half_width = critical_value * standard_error
    return PairedRiskDifference(
        risk_difference=effect,
        standard_error=standard_error,
        ci_low=effect - half_width,
        ci_high=effect + half_width,
        n_targets=n,
    )


def evaluate_design(
    *,
    targets: int,
    negative_history_probability: float,
    directional_risk_difference: float,
    pair_coupling: float,
    replications: int,
    seed: int,
) -> OperatingCharacteristics:
    """Estimate rejection and interval coverage for the paired analysis."""
    if replications <= 0:
        raise ValueError("replications must be positive")
    rng = random.Random(seed)
    estimates = []
    rejected = 0
    covered = 0
    for _ in range(replications):
        outcomes = simulate_paired_binary(
            targets=targets,
            negative_history_probability=negative_history_probability,
            directional_risk_difference=directional_risk_difference,
            pair_coupling=pair_coupling,
            seed=rng.randrange(2**63),
        )
        estimate = estimate_paired_risk_difference(outcomes)
        estimates.append(estimate.risk_difference)
        if estimate.ci_low > 0.0 or estimate.ci_high < 0.0:
            rejected += 1
        if estimate.ci_low <= directional_risk_difference <= estimate.ci_high:
            covered += 1
    mean_estimate = sum(estimates) / replications
    return OperatingCharacteristics(
        targets=targets,
        true_risk_difference=directional_risk_difference,
        pair_coupling=pair_coupling,
        replications=replications,
        rejection_rate=rejected / replications,
        coverage=covered / replications,
        mean_estimate=mean_estimate,
        bias=mean_estimate - directional_risk_difference,
    )


def _exact_upper_p(positive_only: int, discordant: int) -> float:
    if discordant == 0:
        return 1.0
    numerator = sum(
        math.comb(discordant, value) for value in range(positive_only, discordant + 1)
    )
    return float(numerator) / float(2**discordant)


def evaluate_discordance_design(
    *,
    targets: int,
    discordance_probability: float,
    directional_risk_difference: float,
    replications: int,
    seed: int,
    alpha: float = 0.05,
) -> DiscordanceOperatingCharacteristics:
    """Simulate the exact one-sided paired test from discordance and effect inputs."""
    if targets <= 0 or replications <= 0:
        raise ValueError("targets and replications must be positive")
    if not 0.0 <= discordance_probability <= 1.0:
        raise ValueError("discordance_probability must be in [0, 1]")
    if abs(directional_risk_difference) > discordance_probability:
        raise ValueError("absolute risk difference cannot exceed discordance probability")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")

    positive_only_probability = (
        discordance_probability + directional_risk_difference
    ) / 2
    negative_only_probability = (
        discordance_probability - directional_risk_difference
    ) / 2
    rng = random.Random(seed)
    rejected = 0
    estimates = []
    discordance_rates = []
    for _ in range(replications):
        positive_only = 0
        negative_only = 0
        for _ in range(targets):
            draw = rng.random()
            if draw < positive_only_probability:
                positive_only += 1
            elif draw < positive_only_probability + negative_only_probability:
                negative_only += 1
        discordant = positive_only + negative_only
        estimates.append((positive_only - negative_only) / targets)
        discordance_rates.append(discordant / targets)
        rejected += int(_exact_upper_p(positive_only, discordant) <= alpha)
    mean_estimate = sum(estimates) / replications
    return DiscordanceOperatingCharacteristics(
        targets=targets,
        discordance_probability=discordance_probability,
        true_risk_difference=directional_risk_difference,
        replications=replications,
        rejection_rate=rejected / replications,
        mean_estimate=mean_estimate,
        bias=mean_estimate - directional_risk_difference,
        mean_discordance_rate=sum(discordance_rates) / replications,
    )


def evaluate_panel_design(
    *,
    targets_per_cell: int,
    discordance_probabilities: Sequence[float],
    directional_risk_differences: Sequence[float],
    replications: int,
    seed: int,
    alpha: float = 0.05,
) -> PanelOperatingCharacteristics:
    """Evaluate a pooled exact test when fixed model/world cells may disagree in sign."""
    if targets_per_cell <= 0 or replications <= 0:
        raise ValueError("targets_per_cell and replications must be positive")
    discordances = tuple(discordance_probabilities)
    effects = tuple(directional_risk_differences)
    if len(discordances) < 2 or len(discordances) != len(effects):
        raise ValueError("panel inputs must have equal lengths and at least two cells")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    for discordance, effect in zip(discordances, effects, strict=True):
        if not 0.0 <= discordance <= 1.0:
            raise ValueError("discordance probabilities must be in [0, 1]")
        if abs(effect) > discordance:
            raise ValueError("absolute cell effect cannot exceed discordance probability")

    rng = random.Random(seed)
    cells = len(effects)
    pooled_rejected = 0
    sign_consistent_rejected = 0
    any_negative = 0
    all_positive = 0
    pooled_estimate_sum = 0.0
    cell_estimate_sums = [0.0] * cells
    cell_rejections = [0] * cells
    total_discordant = 0
    for _ in range(replications):
        pooled_positive_only = 0
        pooled_negative_only = 0
        cell_estimates: list[float] = []
        for index, (discordance, effect) in enumerate(
            zip(discordances, effects, strict=True)
        ):
            positive_probability = (discordance + effect) / 2
            negative_probability = (discordance - effect) / 2
            positive_only = 0
            negative_only = 0
            for _ in range(targets_per_cell):
                draw = rng.random()
                if draw < positive_probability:
                    positive_only += 1
                elif draw < positive_probability + negative_probability:
                    negative_only += 1
            discordant = positive_only + negative_only
            estimate = (positive_only - negative_only) / targets_per_cell
            cell_estimates.append(estimate)
            cell_estimate_sums[index] += estimate
            cell_rejections[index] += int(
                _exact_upper_p(positive_only, discordant) <= alpha
            )
            pooled_positive_only += positive_only
            pooled_negative_only += negative_only

        pooled_discordant = pooled_positive_only + pooled_negative_only
        pooled_estimate = (pooled_positive_only - pooled_negative_only) / (
            targets_per_cell * cells
        )
        rejected = _exact_upper_p(pooled_positive_only, pooled_discordant) <= alpha
        pooled_rejected += int(rejected)
        sign_consistent_rejected += int(rejected and all(value > 0 for value in cell_estimates))
        any_negative += int(any(value < 0 for value in cell_estimates))
        all_positive += int(all(value > 0 for value in cell_estimates))
        pooled_estimate_sum += pooled_estimate
        total_discordant += pooled_discordant

    return PanelOperatingCharacteristics(
        cells=cells,
        targets_per_cell=targets_per_cell,
        total_targets=targets_per_cell * cells,
        discordance_probabilities=discordances,
        true_cell_risk_differences=effects,
        true_mean_risk_difference=sum(effects) / cells,
        replications=replications,
        pooled_rejection_rate=pooled_rejected / replications,
        sign_consistent_rejection_rate=sign_consistent_rejected / replications,
        any_negative_cell_rate=any_negative / replications,
        all_positive_cell_rate=all_positive / replications,
        mean_pooled_estimate=pooled_estimate_sum / replications,
        mean_cell_estimates=tuple(value / replications for value in cell_estimate_sums),
        cell_rejection_rates=tuple(value / replications for value in cell_rejections),
        mean_discordance_rate=total_discordant
        / (replications * targets_per_cell * cells),
    )
