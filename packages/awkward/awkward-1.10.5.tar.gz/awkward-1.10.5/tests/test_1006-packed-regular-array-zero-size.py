# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    array = ak.from_numpy(np.zeros((1, 0), dtype=np.int32), regulararray=True)
    packed = ak.packed(array)
    assert ak.to_list(packed) == [[]]
