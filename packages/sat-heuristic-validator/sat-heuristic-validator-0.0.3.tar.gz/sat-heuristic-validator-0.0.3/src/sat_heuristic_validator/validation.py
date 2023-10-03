from concurrent.futures import as_completed, ThreadPoolExecutor, ProcessPoolExecutor
from enum import Enum
from typing import Callable, List, Tuple

from sat_heuristic_validator.aggregate import (
    AggregationError,
    Aggregator,
    AllSamplesAggregator,
    ConfusionAggregator,
    SampleAggregator,
)
from sat_heuristic_validator.struct import And


class ValidationMode(Enum):
    SAMPLE = 1
    CONFUSION_MATRIX = 2
    ALL_SAMPLES = 3

    def get_aggregator(self) -> Aggregator:
        if self is ValidationMode.SAMPLE:
            return SampleAggregator()
        if self is ValidationMode.CONFUSION_MATRIX:
            return ConfusionAggregator()
        if self is ValidationMode.ALL_SAMPLES:
            return AllSamplesAggregator()
        raise NotImplementedError


def validate(
    algorithm: Callable[[And], bool],
    dataset: List[Tuple[And, bool]],
    validation_mode: ValidationMode,
):
    encapsulated_algorithm = lambda x, y: (algorithm(x), x, y)

    results = []
    aggregator = validation_mode.get_aggregator()
    with ThreadPoolExecutor() as executor:
        for data in dataset:
            results.append(executor.submit(encapsulated_algorithm, *data))
        try:
            for future in as_completed(results):
                aggregator.aggregate(*future.result())
        except AggregationError as e:
            for r in results:
                r.cancel()
            raise e
    return aggregator.done()
