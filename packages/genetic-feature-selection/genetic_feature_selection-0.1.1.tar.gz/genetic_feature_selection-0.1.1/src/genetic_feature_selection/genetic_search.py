import pathlib
from typing import Callable, Dict, Any
from genetic_feature_selection.genetic_funcs import *
from genetic_feature_selection.roulette_wheel_selection import roulette
from genetic_feature_selection.vanilla_generator import GenPopVanilla
from genetic_feature_selection.genetic_iter import GeneticIter
import pandas as pd


class GeneticSearch:
    """Algoritme for genetisk variabel søk. 

    For hver iterasjon genereres det generations antall generasjoner med sol_per_pop antall
    individer. En generasjon er en runde med generering, evaluering og videreføring av de 
    keep_n_best_individuals individene til neste generasjon. 
    Et individ er en vektor med variabler. Hvert genererte individ vil bli gitt en score. Denne
    scoren er med på vekte sannsynligheten for at dette individet for parre seg. Scoren bestemmer
    også hvilke individer som vil bli med til neste generasjon. 
    Scoren til hvert individ kalkuleres ved hjelp av fitness_func. fitness_func er en funksjon som
    trener en modell med variablene angitt i individet og evaluerer denne modellen med en angitt 
    metrikk. 

    Args:
        iterations (int): Hvor mange iterasjoner skal gjennomføres. Det vil bli trent 
            iterations * generations * sol_per_pop modeller når metoden train kalles. 
        sol_per_pop (int): Hvor mange feature vectors skal genereres for hver generasjon. 
        generations (int): Hvor mange generasjoner per iterasjon. 
        n_features (int): Hvor mange features eksisterer det i datasettet.
        keep_n_best_individuals (int): Hvor mange av de beste individene skal videre med til
            neste generasjon.
        select_n_features (int): Hvor mange variabler skal velges. 
        fitness_func (Callable[[List[int]], float]): Funksjon som regner ut score for hvert individ.
        num_parents_mating (int): Hvor mange av individene skal pare seg. 
        gen_pop (_type_, optional): Hvordan skal nye individer genereres Denne klassen må implementere
            en gen_pop metode for å generere en ny generasjon med individer. Defaults to GenPopVanilla().
    """
    def __init__(
        self,
        iterations : int,
        sol_per_pop : int,
        generations : int,
        keep_n_best_individuals : int,
        select_n_features : int,
        num_parents_mating : int,
        X_train : pd.DataFrame,
        y_train : pd.Series,
        X_test : pd.DataFrame,
        y_test : pd.Series,
        clf : Any,
        probas : bool, 
        scorer : Callable[[pd.Series, pd.Series], float], 
        gen_pop = GenPopVanilla(),
        path : str = None,
        clf_params : Dict[str, Any] = {},
        fitness_func = None
    ) -> None:
        self.iterations = iterations
        self.sol_per_pop = sol_per_pop
        self.generations = generations
        self.n_features = X_train.shape[1]
        self.keep_n_best_individuals = keep_n_best_individuals
        self.select_n_features = select_n_features
        self.num_parents_mating = num_parents_mating
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.clf = clf
        self.clf_params = clf_params
        self.probas = probas
        self.scorer = scorer
        self.pop_generator = gen_pop
        self.gen_pop = gen_pop.gen_pop
        self.path = path
        if fitness_func: setattr(self, "fitness_func", fitness_func)

    def _dump_results(self, txt : str):
        if not self.path:
            self.path = pathlib.Path("search-log.log")
        else:
            self.path = pathlib.Path(self.path)
        
        with open(self.path, "a") as f:
            f.write(txt + "\n")
        
    def search(self, dump = True):
        self.results = []

        for i in range(self.iterations):
            print(f"Iteration {i}")
            best_cols, score, iter_scores = self.one_iteration()
            self.results.append(GeneticIter(i, score, best_cols, iter_scores))

            if dump:
                self._dump_results(str(self.results[-1]))

        self.results.sort(key=lambda x: x.score)
        return self.results[-1].cols
    
    def one_iteration(self):
        pop = self.gen_pop(self.sol_per_pop, self.n_features, self.select_n_features)
        prev_best = 0
        scores = []
        keep = []

        for i in range(self.generations):
            evaluted_pop = evaluate_generation(pop, self.fitness_func)

            # Check if child is better than the second best individual in the population
            # This is done to avoid sorting the list twice 
            evaluated_children = roulette(
                evaluted_pop, self.num_parents_mating, self.n_features, self.fitness_func
            )

            evaluted_pop.extend(evaluated_children)
            evaluted_pop.sort(reverse=True, key=lambda x: x[0])

            # keep keep_n_best_individuals best individuals and create a new generation.  
            keep = evaluted_pop[:self.keep_n_best_individuals]
            keep = [i[1] for i in keep]
            
            # add crossover gen to pop list if exists, this is done so we dont have to reevaluate the individuals
            pop = keep + self.gen_pop(
                self.sol_per_pop-self.keep_n_best_individuals, self.n_features, self.select_n_features
            )
            
            curr_best_score = evaluted_pop[0][0]
            scores.append(curr_best_score)

            if curr_best_score > prev_best:
                print("\t generation:", i, "score:", curr_best_score)
                prev_best = curr_best_score
                best_cols = evaluted_pop[0][1]
        
        best_cols = self.pop_generator.int2str(best_cols)
        return best_cols, prev_best, scores

    def fitness_func(self, soln):    
        X_train_soln = get_features(self.X_train, soln)
        X_val_son = get_features(self.X_test, soln)

        clf = self.clf(**self.clf_params)
        clf.fit(X_train_soln, self.y_train)

        if self.probas:
            preds = clf.predict_proba(X_val_son)[:,1]
        else:
            preds = clf.predict(X_val_son)[:,1]

        return self.scorer(self.y_test, preds)
