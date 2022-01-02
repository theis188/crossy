import unittest

from ..classes import MRNA, Codon, Substitution


class TestCodon(unittest.TestCase):
    def setUp(self):
        self.codon_sequence = "CCG"
        self.codon = Codon.from_sequence(self.codon_sequence)

    def test_codon_loading(self):
        self.assertEqual(len(Codon.CODONS_DICT), 61)

    def test_codon(self):
        self.assertEqual(
            self.codon,
            Codon(codon_sequence="CCG", stability=-
                  0.178554217, amino_acid="P"),
        )

    def test_synonomous_codons(self):
        synonomous_codon_strs = self.codon.synonomous_codon_strings
        self.assertEqual(set(synonomous_codon_strs),
                         set(["CCA", "CCT", "CCC", "CCG"]))


class TestMRNA(unittest.TestCase):
    def setUp(self):
        self.mrna = MRNA.from_sequence("CCGTCG")

    def test_mrna(self):
        self.assertEqual(
            self.mrna,
            MRNA(
                codon_sequence=[Codon.from_sequence(
                    "CCG"), Codon.from_sequence("TCG")]
            ),
        )

    def test_total_stability(self):
        stability = self.mrna.total_stability
        self.assertAlmostEqual(stability, -0.302168675)

    def test_candidate_substitutions(self):
        substitutions = self.mrna.get_candidate_substitutions()
        self.assertEqual(len(substitutions), 2)
        self.assertEqual(len(substitutions[0]), 4)
        self.assertEqual(len(substitutions[1]), 6)
        self.assertEqual(
            substitutions[0][0],
            Substitution(
                from_codon=Codon.from_sequence("CCG"),
                to_codon=Codon.from_sequence("CCA"),
            ),
        )


class TestSubstitutions(unittest.TestCase):
    def test_substitution(self):
        substitution = Substitution(
            from_codon=Codon.from_sequence("CCG"), to_codon=Codon.from_sequence("CCA")
        )
        stability_change = substitution.stability_change
        self.assertAlmostEqual(stability_change, 0.33542168699999997)
