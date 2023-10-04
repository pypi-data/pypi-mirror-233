import numpy as np
import pandas as pd
from sklearn.feature_selection import f_regression


def softmax(x, tau = 1):
    if isinstance(x, list):
        return np.exp([y/tau for y in x])/sum(np.exp([y/tau for y in x])) 
    return np.exp(x/tau)/sum(np.exp(x/tau))


def calc_f_score(X, y, sort = True):
    f = pd.Series(f_regression(X, y)[0], index=X.columns)
    if sort:
        f = f.sort_values(ascending=False)
    return f
