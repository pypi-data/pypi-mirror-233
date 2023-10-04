from dataclasses import dataclass
from typing import List, Tuple, Union


class Var:
    i: int

    def __init__(self, i: int):
        self.i = i
        assert self.i > 0

    def __str__(self) -> str:
        return f"x{self.i}"

    def __repr__(self) -> str:
        return f"Var({self.i})"

    def eval(self, mask: int) -> bool:
        return bool(mask & (1 << (self.i - 1)))


@dataclass
class Neg:
    x: Var

    def __init__(self, x: int):
        self.x = x

    def __str__(self) -> str:
        return f"¬{self.x}"

    def __repr__(self) -> str:
        return f"Neg({repr(self.x)})"

    def eval(self, mask: int) -> bool:
        return not bool(mask & (1 << (self.x.i - 1)))


@dataclass
class Or:
    xs: Tuple[Union[Var, Neg], ...]

    def __init__(self, *xs: Tuple[Union[Var, Neg], ...]):
        self.xs = xs

    def __str__(self) -> str:
        return " ∨ ".join(map(str, self.xs))

    def __repr__(self) -> str:
        return f"Or({', '.join(map(repr, self.xs))})"

    def eval(self, mask: int) -> bool:
        for x in self.xs:
            if x.eval(mask):
                return True
        return False


@dataclass
class And:
    xs: Tuple[Or, ...]

    def __init__(self, *xs: Tuple[Or, ...]):
        self.xs = xs

    def __str__(self) -> str:
        return "∧".join(map(lambda x: f"({x})", self.xs))

    def __repr__(self) -> str:
        return f"And({', '.join(map(repr, self.xs))})"

    def eval(self, mask: int) -> bool:
        for x in self.xs:
            if not x.eval(mask):
                return False
        return True
