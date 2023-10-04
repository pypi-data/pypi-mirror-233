import itertools as it
from typing import List, Sequence, Tuple

from sat_heuristic_validator.satisfy import is_satisfiable_brute
from sat_heuristic_validator.struct import And, Neg, Or, Var


def construct_dataset(formulas: Sequence[And]) -> List[Tuple[And, bool]]:
    return [(formula, is_satisfiable_brute(formula)) for formula in formulas]


def _itertools_powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s) + 1))


def _term(el: Tuple[Tuple[int, ...], int]):
    alternative, mask = el
    return Or(
        *(
            Neg(Var(a)) if (mask & (1 << i)) else Var(a)
            for i, a in enumerate(alternative)
        )
    )


def all_3_sat_formulas(n: int) -> Sequence[And]:
    return map(
        lambda x: And(*x),
        _itertools_powerset(
            it.chain(
                map(_term, it.product(it.combinations(range(1, n + 1), 1), range(2))),
                map(_term, it.product(it.combinations(range(1, n + 1), 2), range(4))),
                map(_term, it.product(it.combinations(range(1, n + 1), 3), range(8))),
            )
        ),
    )


def all_3_sat_dataset(n: int) -> List[Tuple[And, bool]]:
    return construct_dataset(formulas=all_3_sat_formulas(n=n))


def only_3_cnf_formulas(n: int) -> Sequence[And]:
    return map(
        lambda x: And(*x),
        _itertools_powerset(
            map(_term, it.product(it.combinations(range(1, n + 1), 3), range(8))),
        ),
    )


def only_3_cnf_dataset(n: int) -> List[Tuple[And, bool]]:
    return construct_dataset(formulas=only_3_cnf_formulas(n=n))
