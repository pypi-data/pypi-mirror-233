from sat_heuristic_validator.struct import And, Var


def count_vars(f: And) -> bool:
    all_unique_vars = set(
        x.i if isinstance(x, Var) else x.x.i for or_ in f.xs for x in or_.xs
    )
    return max(all_unique_vars) if all_unique_vars else 0


def is_satisfiable_brute(f: And) -> bool:
    n = count_vars(f)
    for i in range(1 << n):
        if f.eval(mask=i):
            return True
    return False
