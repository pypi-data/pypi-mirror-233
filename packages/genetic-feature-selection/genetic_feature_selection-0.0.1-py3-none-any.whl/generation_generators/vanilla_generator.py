import numpy as np


class GenPopVanilla:
    def gen_pop(self, sol_per_pop, n_features, select_n_features):
        pop = []
        for _ in range(sol_per_pop):
            pop.append(np.random.choice([i for i in range(n_features)], size=select_n_features, replace=False).tolist())
        return pop
