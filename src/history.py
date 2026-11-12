"""Yield model that starts from a district's own recent yield and learns the adjustment.

prediction = reference yield x exp(adjustment)

The reference is a column of X (the mean yield of the previous years for the same
district, crop and season). The wrapped regressor learns log(yield / reference)
from the other features, so it only has to explain why this season differs from
the district's recent past.
"""

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, clone


class HistoryAdjustedRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, regressor, reference_col="yield_recent_mean"):
        self.regressor = regressor
        self.reference_col = reference_col

    def fit(self, X, y):
        reference = X[self.reference_col].to_numpy(dtype=float)
        self.regressor_ = clone(self.regressor).fit(X, np.log(np.asarray(y, dtype=float) / reference))
        return self

    def predict(self, X):
        reference = X[self.reference_col].to_numpy(dtype=float)
        return reference * np.exp(self.regressor_.predict(X))
