# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


# @ak._v2._connect.numpy.implements("min")
def min(
    array,
    axis=None,
    keepdims=False,
    initial=None,
    mask_identity=True,
    flatten_records=False,
):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        axis (None or int): If None, combine all values from the array into
            a single scalar result; if an int, group by that axis: `0` is the
            outermost, `1` is the first level of nested lists, etc., and
            negative `axis` counts from the innermost: `-1` is the innermost,
            `-2` is the next level up, etc.
        keepdims (bool): If False, this reducer decreases the number of
            dimensions by 1; if True, the reduced values are wrapped in a new
            length-1 dimension so that the result of this operation may be
            broadcasted with the original array.
        initial (None or number): The maximum value of an output element, as
            an alternative to the numeric type's natural identity (e.g. infinity
            for floating-point types, a maximum integer for integer types).
            If you use `initial`, you might also want `mask_identity=False`.
        mask_identity (bool): If True, reducing over empty lists results in
            None (an option type); otherwise, reducing over empty lists
            results in the operation's identity.
        flatten_records (bool): If True, axis=None combines fields from different
            records; otherwise, records raise an error.

    Returns the minimum value in each group of elements from `array` (many
    types supported, including all Awkward Arrays and Records). The identity
    of minimization is `inf` if floating-point or the largest integer value
    if applied to integers. This identity is usually masked: the minimum of
    an empty list is None, unless `mask_identity=False`.
    This operation is the same as NumPy's
    [amin](https://docs.scipy.org/doc/numpy/reference/generated/numpy.amin.html)
    if all lists at a given dimension have the same length and no None values,
    but it generalizes to cases where they do not.

    See #ak.sum for a more complete description of nested list and missing
    value (None) handling in reducers.

    See also #ak.nanmin.
    """
    with ak._v2._util.OperationErrorContext(
        "ak._v2.min",
        dict(
            array=array,
            axis=axis,
            keepdims=keepdims,
            initial=initial,
            mask_identity=mask_identity,
            flatten_records=flatten_records,
        ),
    ):
        return _impl(array, axis, keepdims, initial, mask_identity, flatten_records)


# @ak._v2._connect.numpy.implements("nanmin")
def nanmin(
    array,
    axis=None,
    keepdims=False,
    initial=None,
    mask_identity=True,
    flatten_records=False,
):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        axis (None or int): If None, combine all values from the array into
            a single scalar result; if an int, group by that axis: `0` is the
            outermost, `1` is the first level of nested lists, etc., and
            negative `axis` counts from the innermost: `-1` is the innermost,
            `-2` is the next level up, etc.
        keepdims (bool): If False, this reducer decreases the number of
            dimensions by 1; if True, the reduced values are wrapped in a new
            length-1 dimension so that the result of this operation may be
            broadcasted with the original array.
        initial (None or number): The maximum value of an output element, as
            an alternative to the numeric type's natural identity (e.g. infinity
            for floating-point types, a maximum integer for integer types).
            If you use `initial`, you might also want `mask_identity=False`.
        mask_identity (bool): If True, reducing over empty lists results in
            None (an option type); otherwise, reducing over empty lists
            results in the operation's identity.
        flatten_records (bool): If True, axis=None combines fields from different
            records; otherwise, records raise an error.

    Like #ak.min, but treating NaN ("not a number") values as missing.

    Equivalent to

        ak.min(ak.nan_to_none(array))

    with all other arguments unchanged.

    See also #ak.min.
    """
    with ak._v2._util.OperationErrorContext(
        "ak._v2.nanmin",
        dict(
            array=array,
            axis=axis,
            keepdims=keepdims,
            initial=initial,
            mask_identity=mask_identity,
            flatten_records=flatten_records,
        ),
    ):
        array = ak._v2.operations.ak_nan_to_none._impl(array, False, None)

        return _impl(array, axis, keepdims, initial, mask_identity, flatten_records)


def _impl(array, axis, keepdims, initial, mask_identity, flatten_records):
    layout = ak._v2.operations.to_layout(array, allow_record=False, allow_other=False)

    if axis is None:
        if not layout.nplike.known_data or not layout.nplike.known_shape:
            reducer_cls = ak._v2._reducers.Min

            def map(x):
                return ak._v2._typetracer.MaybeNone(
                    ak._v2._typetracer.UnknownScalar(
                        np.dtype(reducer_cls.return_dtype(x.dtype))
                    )
                )

        else:

            def map(x):
                return layout.nplike.min(x)

        def reduce(xs):
            if len(xs) == 0:
                return None
            elif len(xs) == 1:
                return xs[0]
            else:
                return layout.nplike.minimum(xs[0], reduce(xs[1:]))

        tmp = layout.completely_flatten(
            function_name="ak.min", flatten_records=flatten_records
        )
        return reduce([map(x) for x in tmp if not x.shape[0] <= 0])

    else:
        behavior = ak._v2._util.behavior_of(array)
        out = layout.min(
            axis=axis,
            mask=mask_identity,
            keepdims=keepdims,
            initial=initial,
            behavior=behavior,
        )
        if isinstance(out, (ak._v2.contents.Content, ak._v2.record.Record)):
            return ak._v2._util.wrap(out, behavior)
        else:
            return out
