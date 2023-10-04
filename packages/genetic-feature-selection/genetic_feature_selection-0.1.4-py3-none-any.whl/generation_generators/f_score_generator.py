from logging import warning
import numpy as np
from genetic_stats import softmax, calc_f_score
from abc import ABC, abstractmethod


class FScoreInitPop(ABC):
    def __init__(self, X, y) -> None:
        self.f_scores = calc_f_score(X, y)
        self.y = y
        self.map_col_to_index(X)
        self.X = X.rename(columns = self.col2int)

    @abstractmethod
    def gen_pop(self):
        pass

    def map_col_to_index(self, X):
        self.int2col = {i:col for i,col in enumerate(X.columns)}
        self.col2int = {col:i for i,col in enumerate(X.columns)}


class GreedyFScoreInitPop(FScoreInitPop):
    def gen_pop(self, soln_per_pop, n_features, select_n_features):
        # f_scores <- calculate f-score 
        # generate i empty feature vectors
        # for each x_i in f_score:
        #   add x_i to to feature_vec_i in such a manner that
        #   feature_vec_i = [x_i, x_(2*i), ..., x_(n_features*i)]
        i = 0
        j = 0
        solns = []

        for _ in range(select_n_features):
            for _ in range(soln_per_pop):
                if len(solns) < soln_per_pop:
                    solns.append([])
                solns[i].append(self.col2int[self.f_scores.index[j]])
                
                i += 1
                if i >= self.soln_per_pop:
                    i = 0
                j += 1

        return solns


class FScoreSoftmaxInitPop(FScoreInitPop):
    def __init__(self, X, y, tau = 50) -> None:
        super().__init__(X, y)
        self.f_scores = calc_f_score(X, y, sort = False).fillna(0)
        self.tau = tau
        self.probs = softmax(self.f_scores, self.tau)

        if any(np.isnan(self.probs)):
            raise ValueError(
                "Det er NaNs i sannsynlighetene. Dette kan bety at noen variabler har fått svært høy f-score. Prøv å øke verdien til tau parameteren i ")

    def gen_pop(self, soln_per_pop, n_features, select_n_features):
        selected_features = np.random.choice(
            self.X.columns, size = (select_n_features, soln_per_pop),
            p = self.probs, replace=False
        )
        
        return selected_features.T.tolist()
