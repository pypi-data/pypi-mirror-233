import numpy as np
from genetic_feature_selection.genetic_stats import softmax
import random


def get_features(X, genes):
    return X.iloc[:,genes]


def evaluate_generation(population, fitness_func):
    evaluted_gen = []

    for ind in population:
        score = fitness_func(ind)
        evaluted_gen.append((score, ind))
    return evaluted_gen


def mate_parents(parent1, parent2):
    parent1, parent2 = list(parent1), list(parent2)
    child = parent1[:int(len(parent1)/2)] + parent2[int(len(parent1)/2):]
    assert len(child) == len(parent1)
    return child


def weighted_selection(p1, p2):
    probs = softmax([p1[0], p2[0]])
    select_from = np.random.choice([0,1], size=len(p1[1]), p=probs).tolist()
    child = []
    parents = (p1, p2)

    for i,p in enumerate(select_from):
        child.append(parents[p][1][i])

    return child


def _add_random_gene(ind, desired_len, max_gene):
    if len(ind) == desired_len:
        return ind
    
    rand_int = random.randrange(max_gene)
    if rand_int not in ind:
        ind.append(rand_int)
    
    return _add_random_gene(ind, desired_len, max_gene)


def _replace_dup_genes(child, n_genes):
    # ertstatt dupliserte gener med tilfeldige gener som ikke eksisterer i individet 
    no_dups = set(child)

    if len(no_dups) < len(child):
        child_w_dups = list(no_dups)

        child = _add_random_gene(child_w_dups, len(child), n_genes)

    return child


def main():
    efvs = [
        (0.9, [1,2,3,4]),
        (0.0, [5,6,7,8]),
    ]

    p1, p2 = efvs[0], efvs[1]

    # child = weighted_selection(
    #     efvs[0], 
    #     efvs[1]
    # )

    # print(child)

    probs = softmax([p1[0], p2[0]])
    print(probs)
    select_from = np.random.choice([0,1], size=len(p1[1]), p=probs).tolist()
    child = []
    parents = (p1, p2)

    for i,p in enumerate(select_from):
        child.append(parents[p][1][i])

if __name__ == "__main__":
    main()
