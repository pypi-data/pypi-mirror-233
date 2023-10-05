# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import os

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


pyarrow = pytest.importorskip("pyarrow")
pytest.importorskip("pyarrow.parquet")

if int(pyarrow.__version__.split(".")[0]) >= 13:
    list_indicator = "element"
else:
    list_indicator = "item"


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_1(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test1.parquet")
    data = [{"x": one}, {"x": two}, {"x": three}]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {"tmp:col:x[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_2(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test2.parquet")
    data = [{"x": {"y": one}}, {"x": {"y": two}}, {"x": {"y": three}}]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.y[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_3(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test3.parquet")
    data = [
        {"x": {"y": one, "z": 1.1}},
        {"x": {"y": two, "z": 2.2}},
        {"x": {"y": three, "z": 3.3}},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("z").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]"}
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]", "tmp:col:x.y[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_4(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test4.parquet")
    data = [{"x": []}, {"x": [one]}, {"x": [one, two, three]}]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_5(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test5.parquet")
    data = [{"x": {"y": []}}, {"x": {"y": [one]}}, {"x": {"y": [one, two, three]}}]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_6(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test6.parquet")
    data = [
        {"x": {"y": [], "z": 1.1}},
        {"x": {"y": [one], "z": 2.2}},
        {"x": {"y": [one, two, three], "z": 3.3}},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("z").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]"}
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]", "tmp:lst:x.y[0]"}
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]"}
    array.layout.field("x").array.field("z").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]", "tmp:col:x.z[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_7(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test7.parquet")
    data = [
        {"x": []},
        {"x": [{"y": one}]},
        {"x": [{"y": one}, {"y": two}, {"y": three}]},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y:x[0]",
        f"tmp:col:x.list.{list_indicator}.y[0]",
    }
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_8(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test8.parquet")
    data = [
        {"x": []},
        {"x": [{"y": one, "z": 1.1}]},
        {"x": [{"y": one, "z": 1.1}, {"y": two, "z": 2.2}, {"y": three, "z": 3.3}]},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y:x[0]",
        f"tmp:col:x.list.{list_indicator}.y[0]",
    }
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y:x[0]",
        f"tmp:col:x.list.{list_indicator}.y[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y:x[0]"}
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y:x[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y:x[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
        f"tmp:col:x.list.{list_indicator}.y[0]",
    }
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_9(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test9.parquet")
    data = [
        {"x": []},
        {"x": [{"y": {"q": one}}]},
        {"x": [{"y": {"q": one}}, {"y": {"q": two}}, {"y": {"q": three}}]},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("y").array.field("q").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.q:x[0]",
        f"tmp:col:x.list.{list_indicator}.y.q[0]",
    }
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_10(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test10.parquet")
    data = [
        {"x": []},
        {"x": [{"y": {"q": one}, "z": 1.1}]},
        {
            "x": [
                {"y": {"q": one}, "z": 1.1},
                {"y": {"q": two}, "z": 2.2},
                {"y": {"q": three}, "z": 3.3},
            ]
        },
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("y").array.field("q").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.q:x[0]",
        f"tmp:col:x.list.{list_indicator}.y.q[0]",
    }
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.q:x[0]",
        f"tmp:col:x.list.{list_indicator}.y.q[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {f"tmp:off:x.list.{list_indicator}.y.q:x[0]"}
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.q:x[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    array.layout.field("x").array.content.field("y").array.field("q").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.q:x[0]",
        f"tmp:col:x.list.{list_indicator}.y.q[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_11(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test11.parquet")
    data = [
        {"x": []},
        {"x": [{"z": 1.1, "y": {"q": one}}]},
        {
            "x": [
                {"z": 1.1, "y": {"q": one}},
                {"z": 2.2, "y": {"q": two}},
                {"z": 3.3, "y": {"q": three}},
            ]
        },
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert len(set(array.caches[0].keys())) == 1
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert len(set(array.caches[0].keys())) == 1
    array.layout.field("x").array.content.field("y").array
    assert len(set(array.caches[0].keys())) == 1
    array.layout.field("x").array.content.field("y").array.field("q").array
    assert len(set(array.caches[0].keys())) == 2
    array.layout.field("x").array.content.field("z").array
    assert len(set(array.caches[0].keys())) == 3
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert len(set(array.caches[0].keys())) == 1
    assert np.asarray(array.layout.field("x").array.offsets).tolist() == [0, 0, 1, 4]
    assert len(set(array.caches[0].keys())) == 1
    array.layout.field("x").array.content.field("y").array
    assert len(set(array.caches[0].keys())) == 1
    array.layout.field("x").array.content.field("z").array
    assert len(set(array.caches[0].keys())) == 2
    array.layout.field("x").array.content.field("y").array.field("q").array
    assert len(set(array.caches[0].keys())) == 3
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_12(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test12.parquet")
    data = [
        {"x": {"y": []}},
        {"x": {"y": [[one]]}},
        {"x": {"y": [[one, two], [], [three]]}},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_13(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test13.parquet")
    data = [
        {"x": {"y": [], "z": 1.1}},
        {"x": {"y": [[one]], "z": 2.2}},
        {"x": {"y": [[one, two], [], [three]], "z": 3.3}},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("z").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]"}
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:col:x.z[0]", "tmp:lst:x.y[0]"}
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array.field("y").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]"}
    array.layout.field("x").array.field("z").array
    assert set(array.caches[0].keys()) == {"tmp:lst:x.y[0]", "tmp:col:x.z[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_14(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test6.parquet")
    data = [
        {"x": [{"y": [], "z": 1.1}]},
        {"x": []},
        {"x": [{"y": [one, two, three], "z": 3.3}]},
    ]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]"
    }
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
        f"tmp:lst:x.list.{list_indicator}.y[0]",
    }
    assert array.tolist() == data
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.field("x").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]"
    }
    array.layout.field("x").array.content.field("y").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]",
        f"tmp:lst:x.list.{list_indicator}.y[0]",
    }
    array.layout.field("x").array.content.field("z").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:x.list.{list_indicator}.y.list.{list_indicator}:x[0]",
        f"tmp:lst:x.list.{list_indicator}.y[0]",
        f"tmp:col:x.list.{list_indicator}.z[0]",
    }
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_15(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test15.parquet")
    data = [one, two, three]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    array.layout.array
    assert set(array.caches[0].keys()) == {"tmp:col:[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_16(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test15.parquet")
    data = [[one, two], [], [three]]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    assert np.asarray(array.layout.array.offsets).tolist() == [0, 2, 2, 3]
    assert set(array.caches[0].keys()) == {"tmp:lst:[0]"}
    assert array.tolist() == data


@pytest.mark.parametrize("one,two,three", [(1, 2, 3), ("one", "two", "three")])
def test_17(one, two, three, tmp_path):
    filename = os.path.join(str(tmp_path), "test15.parquet")
    data = [[{"x": one}, {"x": two}], [], [{"x": three}]]
    ak.to_parquet(ak.Array(data), filename)
    array = ak.from_parquet(filename, lazy=True, lazy_cache_key="tmp")
    assert set(array.caches[0].keys()) == set()
    assert np.asarray(array.layout.array.offsets).tolist() == [0, 2, 2, 3]
    assert set(array.caches[0].keys()) == {f"tmp:off:.list.{list_indicator}.x:[0]"}
    array.layout.array.content.field("x").array
    assert set(array.caches[0].keys()) == {
        f"tmp:off:.list.{list_indicator}.x:[0]",
        f"tmp:col:.list.{list_indicator}.x[0]",
    }
    assert array.tolist() == data
