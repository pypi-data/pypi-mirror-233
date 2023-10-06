from inspect import Parameter

from act.signatures import *
from act.testing import case_of


test_annotation_sum = case_of(
    (lambda: annotation_sum(int, float), int | float),
    (lambda: annotation_sum(int), int),
    (lambda: annotation_sum(), Parameter.empty),
    (
        lambda: annotation_sum(int, Parameter.empty, float, Parameter.empty, str),
        int | float | str,
    ),
)
