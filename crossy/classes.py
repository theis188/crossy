import os
import random
from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Dict, List

import pandas as pd

MRNA_PATH = os.path.join(os.path.dirname(__file__), "mrna_csc.csv")
DF_INDEXED = pd.read_csv(MRNA_PATH).set_index("Codon")


@dataclass
class Codon:
    CODONS_DICT: ClassVar[Dict] = {}

    codon_sequence: str
    stability: float
    amino_acid: str

    @classmethod
    def from_sequence(cls, codon):
        return cls.CODONS_DICT[codon]

    @property
    def synonomous_codon_strings(self):
        return self._get_synonomous_codon_strings()

    def _get_synonomous_codon_strings(self):
        return DF_INDEXED[DF_INDEXED["AA"] == self.amino_acid].index.tolist()

    @property
    def synonymous_codons(self):
        return [Codon.CODONS_DICT[codon] for codon in self.synonomous_codon_strings]


@dataclass
class MRNA:
    codon_sequence: List[Codon]

    @classmethod
    def from_sequence(cls, sequence: str) -> "MRNA":
        n = len(sequence)
        codons = []
        for i in range(n // 3):
            codons.append(Codon.from_sequence(sequence[i * 3: i * 3 + 3]))
        return cls(codons)

    @property
    def total_stability(self) -> float:
        return sum(c.stability for c in self.codon_sequence)

    def get_candidate_substitutions(self) -> List[List["Substitution"]]:
        return [
            [
                Substitution(from_codon, to_codon)
                for to_codon in from_codon.synonymous_codons
            ]
            for from_codon in self.codon_sequence
        ]


@dataclass
class Substitution:
    from_codon: Codon
    to_codon: Codon

    @property
    def stability_change(self):
        return self.to_codon.stability - self.from_codon.stability


for codon_sequence, row in DF_INDEXED.iterrows():
    Codon.CODONS_DICT[codon_sequence] = Codon(
        codon_sequence=codon_sequence, stability=row["CSC"], amino_acid=row["AA"]
    )
