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
import pytest

@pytest.fixture
def X_y():
    X, y = make_classification(n_samples=1000, n_informative=20, n_redundant=0)
    X = pd.DataFrame(X)
    X.columns = [f"col_{i}" for i in X.columns]
    y = pd.Series(y, name="y", dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X_train, X_test, y_train, y_test


def test_search(X_y):
    X_train, X_test, y_train, y_test = X_y

    gsf = GeneticSearch(
        iterations = 5, 
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
        )
    )



    best_cols = gsf.search()

    assert isinstance(best_cols[0], str)
    assert best_cols[0].startswith("col_")
    assert len(best_cols) == 5
