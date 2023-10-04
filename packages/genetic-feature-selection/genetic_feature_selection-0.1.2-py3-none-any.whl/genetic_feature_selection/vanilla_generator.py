import numpy as np


class GenPopVanilla:
    def gen_pop(self, sol_per_pop : int, n_features : int, select_n_features : int) -> list:
        pop = []
        for _ in range(sol_per_pop):
            pop.append(np.random.choice([i for i in range(n_features)], size=select_n_features, replace=False).tolist())
        return pop


if __name__ == "__main__":
    vanilla_pop = GenPopVanilla()
    pop = vanilla_pop.gen_pop(5, 50, 15)
    
    for p in pop:
        print(sorted(p))
