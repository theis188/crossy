import random
import unittest

from ..analyze import (apply_substitutions, generate_random_mrna_sequence,
                       monte_carlo_strategy)
from ..classes import MRNA


class TestAnalyzeFunctions(unittest.TestCase):
    def setUp(self):
        random.seed(123)
        self.sequence = generate_random_mrna_sequence(n_codons=50)
        self.mrna = MRNA.from_sequence(self.sequence)

    def test_generate_random(self):
        self.assertEqual(len(self.sequence), 150)
        self.assertLessEqual(set(self.sequence), {"T", "C", "G", "A"})

    def test_monte_carlo_strategy(self):
        substitutions = monte_carlo_strategy(
            self.mrna.get_candidate_substitutions(), target=1
        )
        new_mrna = apply_substitutions(self.mrna, substitutions)
        old_stability = self.mrna.total_stability
        new_stability = new_mrna.total_stability
        difference = new_stability - old_stability
        self.assertGreaterEqual(difference, 0.5)
        self.assertLessEqual(difference, 1.5)
