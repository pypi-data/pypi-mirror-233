# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import urllib.request
import urllib.error

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


@pytest.mark.skipif(not ak._util.win, reason="need Windows to test this case")
def test():
    url = "https://raw.githubusercontent.com/Chicago/osd-bike-routes/5f556dc/data/Bikeroutes.geojson"
    try:
        bikeroutes_json = urllib.request.urlopen(url).read()
    except urllib.error.URLError:
        pytest.skip(msg="couldn't download sample dataset")

    # This shouldn't fail (see #1084)
    ak.from_json(bikeroutes_json)
