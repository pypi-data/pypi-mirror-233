# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    a = ak.Array([[1, 2, 3, 4], [5, 6, 7, 8]])
    assert ak.unflatten(a, [2, 2, 2, 2], axis=1).tolist() == [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
    ]
    assert ak.unflatten(a, 2, axis=1).tolist() == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
