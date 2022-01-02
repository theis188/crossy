"""Contains analyze functions for MRNA."""
import random
from typing import List

import pandas as pd

from .classes import DF_INDEXED, MRNA, Substitution


def generate_random_mrna_sequence(n_codons: int = 50) -> str:
    """Generate a random sequence n codons long."""
    codons = DF_INDEXED.index.tolist()
    ret = ""
    for _ in range(n_codons):
        codon = random.choice(codons)
        ret += codon
    return ret


def monte_carlo_strategy(
    substitutions: List[List[Substitution]], target: float, n_rounds: int = 50
) -> List[int]:
    """A random strategy for finding cognate MRNA with different stability levels.

    Args:
        substitutions: A list of lists of substitutions, 
            representing the possible substitutions for each Codon
            in an MRNA.
        target: a float representing the desired total change in MRNA stability.
            An average codon varies from about -0.3 - 0.3 in stability.
            So an average MRNA may vary in stability by about 3 points per 10 bases.
        n_rounds: number of rounds to try.

    Returns:
        List of indexes of substitutions to make.
    """
    # Indexes of all current substitutions
    current_sub_idxs = [
        [sub.stability_change for sub in base_substitutions].index(0.0)
        for base_substitutions in substitutions
    ]
    n_subs = len(substitutions)

    # How much is left to reach target substitution change
    remaining_change = target

    # Repeat n times
    for _ in range(n_rounds):
        # Pick a random substitution index
        idx = random.choice(list(range(n_subs)))
        candidate_substitutions = substitutions[idx]

        # Change in stability represented by currently selected substitution
        current_change = candidate_substitutions[current_sub_idxs[idx]
                                                 ].stability_change

        # Calculate marginal changes
        marginal_changes = [
            sub.stability_change - current_change for sub in candidate_substitutions
        ]
        desired_substitution = min(
            candidate_substitutions,
            key=lambda x: abs(x.stability_change -
                              current_change - (remaining_change)),
        )
        new_sub_idx = candidate_substitutions.index(desired_substitution)
        remaining_change -= (
            candidate_substitutions[new_sub_idx].stability_change
            - candidate_substitutions[current_sub_idxs[idx]].stability_change
        )
        current_sub_idxs[idx] = new_sub_idx
    return current_sub_idxs


def apply_substitutions(mrna: MRNA, sub_idxs: List[int]) -> MRNA:
    substitutions = mrna.get_candidate_substitutions()
    return MRNA(
        [base_subs[idx].to_codon for base_subs,
            idx in zip(substitutions, sub_idxs)]
    )


def get_mrnas_with_different_stability(mrna, stabilities):
    mrnas = [
        apply_substitutions(
            random_mrna, monte_carlo_strategy(substitutions, i))
        for i in stabilities
    ]
    return mrnas
