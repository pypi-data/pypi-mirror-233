import math
from abc import abstractmethod
from dataclasses import dataclass

import numpy as np
import sklearn.metrics

from sat_heuristic_validator.struct import And


@dataclass(eq=False)
class PerformanceMetrics:
    accuracy: float
    precision: np.ndarray
    recall: np.ndarray
    confusion_matrix: np.ndarray

    def __eq__(self, other: "PerformanceMetrics") -> bool:
        return (
            math.isclose(self.accuracy, other.accuracy)
            and np.isclose(self.precision, other.precision).all()
            and np.isclose(self.recall, other.recall).all()
            and np.isclose(self.confusion_matrix, other.confusion_matrix).all()
        )


class AggregationError(Exception):
    pass


class Aggregator:
    @abstractmethod
    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        pass

    @abstractmethod
    def done(self):
        pass


class ConfusionAggregator(Aggregator):
    def __init__(self):
        self.y_true = []
        self.y_pred = []

    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        self.y_true.append(y_expected)
        self.y_pred.append(y_actual)

    def done(self):
        conf_mat = sklearn.metrics.confusion_matrix(
            y_true=self.y_true, y_pred=self.y_pred
        )
        return PerformanceMetrics(
            accuracy=conf_mat.diagonal().sum() / conf_mat.sum(),
            precision=conf_mat.diagonal() / conf_mat.sum(axis=0),
            recall=conf_mat.diagonal() / conf_mat.sum(axis=1),
            confusion_matrix=conf_mat,
        )


class SampleAggregator(Aggregator):
    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        if y_actual != y_expected:
            raise AggregationError(f"{y_actual=} x={x} {y_expected=}")

    def done(self):
        pass


class AllSamplesAggregator(Aggregator):
    def aggregate(self, y_actual: bool, x: And, y_expected: bool):
        if y_actual != y_expected:
            print(f"{y_actual=} x={x} {y_expected=}")

    def done(self):
        pass
