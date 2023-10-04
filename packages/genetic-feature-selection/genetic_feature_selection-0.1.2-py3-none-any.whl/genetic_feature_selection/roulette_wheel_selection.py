from genetic_feature_selection.genetic_funcs import _replace_dup_genes, mate_parents, evaluate_generation, weighted_selection
import numpy as np
from genetic_feature_selection.genetic_stats import softmax


def roulette(
    evaluted_pop, num_parents_mating, n_genes, fitness_func
):
    probs = softmax([i[0] for i in evaluted_pop])
    parents = [i[1] for i in evaluted_pop]
    children = []

    # make mating group 
    # this is done by selecting num_parents_mating 
    # indices, these will be parents.
    mates = np.random.choice(
        len(parents),
        size=num_parents_mating, 
        replace=False, 
        p=probs
    )

    parents2mate = []
    for i in mates:
        parents2mate.append(evaluted_pop[i])
    parents2mate.sort(reverse=True, key=lambda x: x[0])

    # use indices to split mating group in to list 
    # of pairs [[p1, p2], [p3, p4] ...]
    mating_pairs = []
    i = 0 
    while (i < len(mates)):
        pair = []
        for _ in range(2):
            pair.append(parents2mate[i])
            i += 1
        mating_pairs.append(pair)

    # produce children from mating pairs
    for pair in mating_pairs:
        # child = mate_parents(pair[0][1], pair[1][1])
        child = weighted_selection(pair[0], pair[1])
        child = _replace_dup_genes(child, n_genes)
        children.append(child)

    evaluted_children = evaluate_generation(
        children, fitness_func
    )
    # evaluted_children.sort(reverse=True, key=lambda x: x[0])

    return evaluted_children





def main():
    p = [
        (0.9, [1, 2, 1, 4]), 
        (0.88, [5, 6, 1, 8]),
        (0.87, [1, 10, 1, 12]),
        (0.84, [1, 14, 1, 16]),
        (0.77, [1, 18, 1, 20]),
        (0.50, [1, 22, 1, 24])
    ]

    def fitness_func(a,b):
        return sum(a)

    print(roulette(p, 4, 24, fitness_func))


if __name__ == "__main__":
    main()
