import os
import sys
import warnings
from collections import defaultdict

import numpy as np
import pandas as pd


def argmax(a, mode="first"):
    if mode == "first":
        return np.argmax(a)
    elif mode == "last":
        b = a[::-1]
        return len(b) - np.argmax(b) - 1
    else:
        raise Exception("Unknown argmax mode. Use either `first`, or `last`.")


def from_dict(D, *keys):
    return tuple([D[key] for key in keys])


def wrap_yield(iterable, f):
    for e in iterable:
        yield f(e)


def full_like(df, value, dtype=None):
    if isinstance(df, pd.Series):
        dx = pd.Series(value, df.index)
    elif isinstance(df, pd.DataFrame):
        dx = pd.DataFrame(value, index=df.index, columns=df.columns)
    else:
        raise Exception("Please provide either a DataFrame or Series.")

    if dtype is not None:
        dx = dx.astype(dtype)

    return dx


def zeros_like(df, **kwargs):
    return full_like(df, 0, **kwargs)


def ones_like(df, **kwargs):
    return full_like(df, 1, **kwargs)


def to_matrix(df, index, cols, value, fillna=None):
    """
    This method takes a data frame and converts it to panel in the matrix format.

    Parameters
    ----------
    df : pd.DataFrame
        A data frame with the observations being made.
    index : str
        The column that will be the index.
    cols : str
        The column which unique values will become the columns
    value : str
        The values which should be in the panel
    fillna: object
        If not None, NaN values in the panel will be replaced with it.

    Returns
    -------

    panel : pd.DataFrame
        A data frame summarizing the observations in a matrix format.

    """
    dff = df.set_index([index, cols]).sort_index()
    dy = dff[value].unstack(cols)

    if fillna is not None:
        dy.fillna(fillna, inplace=True)

    return dy


def to_matrices(df, index, cols, *values, fillna=None):
    if not isinstance(fillna, dict):
        v = fillna
        fillna = defaultdict(lambda: v)

    return {value: to_matrix(df, index, cols, value, fillna=fillna[value]) for value in values}


def to_balanced(dy):
    p = pd.MultiIndex.from_product(dy.index.levels, names=dy.index.names)
    return dy.reindex(p, fill_value=0)


def time_as_int(x):
    assert x.isna().sum() == 0, "Only series with no nan values can be converted to integers."
    return x.rank(method='dense', ascending=True).astype(int) - 1


def treatment_from_intervention(df: pd.DataFrame,
                                unit: str = "unit",
                                intervention: str = "intervention"):
    treat_units = set(df.query(f"{intervention} == 1")[unit])
    return df[unit].isin(treat_units).astype(int)


def intervention_from_outcome(outcome, time, units):
    intervention = zeros_like(outcome)
    intervention.loc[time:, intervention.columns.isin(units)] = 1
    return intervention


def time_to_intervention(dy, time, fillna=None, dtype=None):
    unit_to_start = dy.query("intervention == 1").groupby("unit")[time].min().to_frame("stime")

    dy = dy.merge(unit_to_start, on="unit", how="left")
    y = dy[time] - dy["stime"]

    if fillna:
        y = y.fillna(fillna)

    if dtype:
        y = y.astype(dtype)

    return y


def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/', 1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':', 1)
    return result


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def nanmean(df, *args, **kwargs):
    if len(df) == 0:
        return np.nan

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.nanmean(df, *args, **kwargs)
