import pathlib
from typing import Callable, List
from genetic_funcs import *
from roulette_wheel_selection import roulette
from vanilla_generator import GenPopVanilla
from genetic_iter import GeneticIter


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
        n_features : int,
        keep_n_best_individuals : int,
        select_n_features : int,
        fitness_func : Callable[[List[int]], float],
        num_parents_mating : int,
        gen_pop = GenPopVanilla(),
        path : str = None
    ) -> None:
        self.iterations = iterations
        self.sol_per_pop = sol_per_pop
        self.generations = generations
        self.n_features = n_features
        self.keep_n_best_individuals = keep_n_best_individuals
        self.select_n_features = select_n_features
        self.fitness_func = fitness_func
        self.num_parents_mating = num_parents_mating
        self.gen_pop = gen_pop.gen_pop
        self.path = path

    def dump_results(self, txt : str):
        if not self.path:
            self.path = pathlib.Path("search-log.log")
        else:
            self.path = pathlib.Path(self.path)
        
        with open(self.path, "a") as f:
            f.write(txt + "\n")
        
    def train(self, dump = True):
        self.results = []

        for i in range(self.iterations):
            print(f"Iteration {i}")
            best_cols, score, iter_scores = self.one_iteration()
            self.results.append(GeneticIter(i, score, best_cols, iter_scores))

            if dump:
                self.dump_results(str(self.results[-1]))
    
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

        return best_cols, prev_best, scores
