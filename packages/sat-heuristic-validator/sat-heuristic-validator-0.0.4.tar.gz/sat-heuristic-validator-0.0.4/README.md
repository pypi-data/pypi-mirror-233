# SAT validation
A library that helps testing correctness of algorithms for Boolean satisfiability problem.

## Instalation
> pip install sat-heuristic-validator

## How to use
```
from sat_heuristic_validator.dataset import only_3_cnf_dataset
from sat_heuristic_validator.struct import And
from sat_heuristic_validator.validation import validate, ValidationMode

def your_algorithm(f: And) -> bool:
    ...

validate(
    algorithm=your_algorithm,
    dataset=only_3_cnf_dataset(n=3),
    validation_mode=ValidationMode.ALL_SAMPLES,
)
```

### Validation modes
- `ValidationMode.SAMPLE` - output single incorrect sample
- `ValidationMode.CONFUSION_MATRIX` - print confusion metrics
- `ValidationMode.ALL_SAMPLES` - print all incorrectly labeled samples

## Examples
Check out [examples](https://github.com/wanatpj/3-SAT/tree/main/examples).
