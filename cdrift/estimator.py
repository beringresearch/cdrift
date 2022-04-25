from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.utils.validation import check_is_fitted

import numpy as np

from scipy.stats import ks_2samp

class DriftDetector(BaseEstimator):
    def __init__(self, estimator, scorer=ks_2samp):
        self.estimator = estimator
        self.scorer = scorer
        self.is_transformer = isinstance(estimator, TransformerMixin())
        self.model = None
        self.reference_X = None
    
    def fit(self, X, y=None):
        check_is_fitted(self.estimator)
        self.reference_X = estimator.transform(X, y)

    def score(self, X):
        result = None
        check_is_fitted(self.estimator)
        if self.model is None:
            raise NotFittedError("Model was not fitted yet. Call `fit` before calling `predict`.")

        if self.is_transformer:
            query_x = self.estimator.transform(X)
            result = self.scorer(self.reference_X, query_x)
        else:
            raise NotImplementedError("only `transformer` types are currently supported.")
        return result

class DriftRandomForestClassifier(BaseEstimator):
    def __init__(self, reference_X, scorer=ks_2samp, **kwargs):
        self.scorer = scorer
        self.reference_X = reference_X
        self.estimator = RandomForestClassifier(**kwargs)
        self.estimator.oob_score=True
    
    def fit(self, X, y=None):
        y = np.concatenate((np.zeros((self.reference_X.shape[0],)), np.ones((X.shape[0], ))))
        Xs = np.concatenate((self.reference_X, X))
        
        self.estimator.fit(Xs, y)


    def score(self, X):
        check_is_fitted(self.estimator)

        probs = self.estimator.oob_decision_function_[:, 1]
        y = np.concatenate((np.zeros((self.reference_X.shape[0],)), np.ones((X.shape[0], ))))

        probs_ref = probs[y == 0]
        probs_cur = probs[y == 1]
        dist, p_val = ks_2samp(probs_ref, probs_cur, alternative='greater')

        return dist, p_val
    
    def score_samples(self, X):
        check_is_fitted(self.estimator)

        probs = self.estimator.oob_decision_function_
        y = np.concatenate((np.zeros((self.reference_X.shape[0],)), np.ones((X.shape[0], ))))
            
        probs = probs[y == 1, 0]
        return probs