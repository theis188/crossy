# Import from modules
from crossy.analyze import generate_random_mrna_sequence
from crossy.classes import MRNA

mrna_sequence = generate_random_mrna_sequence()
mrna = MRNA.from_sequence
scores = get_stability_score(random_mrna)

substitutions = random_mrna.get_candidate_substitutions()

new_substitutions_idxs = monte_carlo_strategy(substitutions, 1.0)
new_mrna = apply_substitutions(random_mrna, new_substitutions_idxs)

sum(c.stability for c in random_mrna.codon_sequence)
sum(c.stability for c in new_mrna.codon_sequence)
