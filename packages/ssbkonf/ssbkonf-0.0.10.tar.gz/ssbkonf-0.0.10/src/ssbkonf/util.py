import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from pandas import DataFrame

from .pckg import __ssbtools


def prepare_input(
    data: DataFrame,
    freq_var=None,
    num_var=None,
    dim_var: list[str] = None,
    formula: str = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
):
    rdata = convert2r(data)
    if formula is None and hierarchies is None and dim_var is None:
        raise ValueError(
            "You must specify at least one of: formula, hierarchies, dim_var"
        )
    if freq_var is None:
        freq_var = ro.NULL
    if num_var is None:
        num_var = ro.NULL
    else:
        if isinstance(num_var, list):
            num_var = ro.StrVector(num_var)
    if dim_var is None:
        dim_var = ro.NULL
    else:
        dim_var = ro.StrVector(dim_var)
    if formula is not None:
        formula = convert_formula2r(formula)
    else:
        formula = ro.NULL
    if hierarchies is not None:
        hierarchies = convert_hierarchies(hierarchies)
    else:
        hierarchies = ro.NULL
    return (
        rdata,
        freq_var,
        num_var,
        dim_var,
        hierarchies,
        formula,
    )


def find_hierarchies(data, total="Total"):
    return convert2py(__ssbtools.FindHierarchies(data=convert2r(data), total=total))


def convert2r(data):
    with (ro.default_converter + pandas2ri.converter).context():
        return ro.conversion.get_conversion().py2rpy(data)


def convert2py(data):
    with (ro.default_converter + pandas2ri.converter).context():
        return ro.conversion.get_conversion().rpy2py(data)


def convert_formula2r(formula):
    if formula is None:
        return ro.r("NULL")
    return ro.r("as.formula(" + formula + ")")


def convert_hierarchies(hier):
    names = []
    vals = []
    for ni in range(len(hier.keys())):
        nm = [*hier.keys()][ni]
        if isinstance(hier[nm], list):
            names += [nm] * len(hier[nm])
            vals += [convert2r(x) for x in hier[nm]]
        else:
            if isinstance(hier[nm], DataFrame):
                names += [nm]
                vals += convert2r([hier[nm]])
            else:
                raise ValueError(
                    "hierarchies must be DataFrames or lists of Dataframes."
                )

    rhier = ro.ListVector.from_length(len(vals))
    for i in range(len(rhier)):
        rhier[i] = vals[i]
    rhier.names = names
    return rhier
