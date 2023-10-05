# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import collections

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


ParquetMetadata = collections.namedtuple(
    "ParquetMetadata",
    ["form", "fs", "paths", "metadata"],
)


def metadata_from_parquet(
    path, storage_options=None, row_groups=None, ignore_metadata=False, scan_files=True
):
    """
    This function differs from ak.from_parquet._metadata as follows:

      * this function will always use a _metadata file, if present
      * if there is no _metadata, the schema comes from _common_metadata or the first
        data file
      * the total number of rows is always known  # TODO: is this true?

    Args:
        path (str): Local filename or remote URL, passed to fsspec for resolution.
            May contain glob patterns. A list of paths is also allowed, but they
            must be data files, not directories.
        storage_options: Passed to `fsspec`.

    Returns dict containing

      * `form`: an Awkward Form representing the low-level type of the data
         (use `.type` to get a high-level type),
      * `fs`: the fsspec filesystem object,
      * `paths`: a list of matching path names,
      * `metadata`: the Parquet metadata, which includes `.num_rows` for the length
         of the array that would be read by #ak.from_parquet and `.num_row_groups`
         for the units that can be filtered (for the #ak.from_parquet `row_groups`
         argument).

    See also #ak.from_parquet, #ak.to_parquet.
    """
    import awkward._v2._connect.pyarrow  # noqa: F401

    with ak._v2._util.OperationErrorContext(
        "ak._v2.metadata_from_parquet",
        dict(
            path=path,
            storage_options=storage_options,
        ),
    ):
        return _impl(
            path,
            storage_options,
            row_groups=row_groups,
            ignore_metadata=ignore_metadata,
            scan_files=scan_files,
        )


def _impl(
    path, storage_options, row_groups=None, ignore_metadata=False, scan_files=True
):
    results = ak._v2.operations.ak_from_parquet.metadata(
        path, storage_options, row_groups, None, ignore_metadata, scan_files
    )
    parquet_columns, subform, actual_paths, fs, subrg, col_counts, metadata = results

    out = {
        "form": subform,
        "paths": actual_paths,
        "col_counts": col_counts,
        "columns": parquet_columns,
    }
    if col_counts:
        out["num_row_groups"] = len(col_counts)
        out["col_counts"] = col_counts
        out["num_rows"] = sum(col_counts)
    else:
        out["num_rows"] = None
        out["num_row_groups"] = None
    return out
