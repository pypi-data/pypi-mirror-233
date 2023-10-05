genetic-feature-selection
=========================


This package implements a genetic algorithm used for feature search.
--------------------------------------------------------------------

.. note::

   Note that the package tries to maximize the fitness function. If you want to minimize, for example, MSE, you should multiply it by -1.

Example of use
--------------

.. code:: python 

    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score
    from sklearn.model_selection import train_test_split
    from genetic_feature_selection.genetic_search import GeneticSearch
    from genetic_feature_selection.f_score_generator import FScoreSoftmaxInitPop
    import pandas as pd


    X, y = make_classification(n_samples=1000, n_informative=20, n_redundant=0)
    X = pd.DataFrame(X)
    y = pd.Series(y, name="y", dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X.columns = [f"col_{i}" for i in X.columns]


    gsf = GeneticSearch(
        # the search will do 5 iterations
        iterations = 5, 
        # each generation will have 4 possible solutions
        sol_per_pop = 4, 
        # every iteration will go through 15 generations 
        generations = 15, 
        # in each generation the 4 best individuals will be kept
        keep_n_best_individuals = 4, 
        # we want to find the 5 features that optimize average precision score
        select_n_features = 5,
        # 4 of the parents will be mating, this means the 4 best solutions in
        # each generation will be combined and create the basis for the next
        # generation
        num_parents_mating = 4,
        X_train = X_train,
        y_train = y_train,
        X_test = X_test,
        y_test = y_test,
        clf = LogisticRegression,
        clf_params = dict(max_iter=15),
        probas = True,
        scorer = average_precision_score,
        gen_pop = FScoreSoftmaxInitPop(
            X_train, y_train, tau = 50
        )
    )


    best_cols = gsf.search()


Example of use with f-score initialization and custom fitness function
----------------------------------------------------------------------

.. code:: python 

    import warnings
    warnings.filterwarnings("ignore")
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score
    from genetic_feature_selection.genetic_funcs import get_features
    from sklearn.model_selection import train_test_split
    from genetic_feature_selection.genetic_search import GeneticSearch
    from genetic_feature_selection.f_score_generator import FScoreSoftmaxInitPop
    import pandas as pd


    X, y = make_classification(n_samples=1000, n_informative=20, n_redundant=0)
    X = pd.DataFrame(X)
    y = pd.Series(y, name="y", dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    clf_params = {}
    clf = LogisticRegression


    class FitnessFunc:
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        clf_params = {}
        clf = LogisticRegression


        def fitness_func(self, soln): 
            X_train_soln = get_features(self.X_train, soln)
            X_val_son = get_features(self.X_test, soln)

            clf = self.clf(**self.clf_params)
            clf.fit(X_train_soln, self.y_train)

            preds = clf.predict_proba(X_val_son)[:,1]

            return average_precision_score(self.y_test, preds)

    fitness_func = FitnessFunc().fitness_func


    gsf = GeneticSearch(
        iterations = 10, 
        sol_per_pop = 4, 
        generations = 15, 
        keep_n_best_individuals = 4, 
        select_n_features = 5,
        num_parents_mating = 4,
        X_train = X_train,
        y_train = y_train,
        X_test = X_test,
        y_test = y_test,
        clf = LogisticRegression,
        clf_params = dict(max_iter=15),
        probas = True,
        scorer = average_precision_score,
        gen_pop = FScoreSoftmaxInitPop(
            X_train, y_train, tau = 50
        ),
        fitness_func=fitness_func
    )

    gsf.search()
