from typing import List, Tuple
import warnings
import numpy as np
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import precision_score, recall_score

warnings.filterwarnings('ignore')

class PAC:
    def __init__(self):
        self.model = PassiveAggressiveClassifier(
            C=0.01,
            max_iter=2,           # Only 1 iteration per batch
            warm_start=True       # Retain model across batches
        )
        self.is_fitted = False  # Only pass classes during initial training

    def train(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float, float, float, float]:
        """Train the model incrementally on the given NumPy arrays"""
        if X.size == 0 or y.size == 0:
            return np.array([]), 0.0, 0.0, 0.0, 0.0

        if not self.is_fitted:
            self.model.partial_fit(X, y, classes=np.arange(10))
            self.is_fitted = True
        else:
            self.model.partial_fit(X, y)

        predictions = self.model.predict(X)

        accuracy = self.model.score(X, y)
        precision = precision_score(y, predictions, labels=np.arange(0, 10), average="macro")
        recall = recall_score(y, predictions, labels=np.arange(0, 10), average="macro")
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        return predictions, accuracy, precision, recall, f1