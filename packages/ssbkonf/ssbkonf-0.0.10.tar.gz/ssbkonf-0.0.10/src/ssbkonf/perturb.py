import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from pandas import DataFrame
from .util import convert2r, convert2py, prepare_input
from .pckg import importr_tryhard

__scr = importr_tryhard("SmallCountRounding")


def small_count_rounding(
    data: DataFrame,
    dim_var: list[str] = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
    formula: str = None,
    freq_var: str = "freq",
    round_base: int = 3,
    max_round=None,
    force_inner=False,
    all_small=False,
    max_iter_rows=1000,
) -> DataFrame:
    """Function for applying the small count rouding method to frequency tables

    Args:
        - data (DataFrame): A DataFrame containing the input data, either as frequency data in long format or as microdata.
        - dim_var (list[str], optional): List of variable names defining the categorical variables of the table. Defaults to None.
        - hierarchies (dict[str, DataFrame  |  list[DataFrame]], optional):  A dictionary containing hierarchies. Each key is a variable name, each value is a list of pandas.DataFrames describing the hierarchies associated with the key. Defaults to None.
        - formula (str, optional): An R model formula, written as a string, for table definition. Defaults to None.. Defaults to None.
        - freq_var (str, optional): Name of the variable containing frequency information. Defaults to "freq".
        - round_base (int, optional): Base to be used for rounding. Defaults to 3.
        - max_round (int, optional): Inner cells contributing to original publishable cells equal to or less than max_round will be rounded.
        - If None, value is set to round_base - 1. Defaults to None.
        - force_inner (bool, optional): When True, all inner cells are rounded. Defaults to False.
        - all_small (bool, optional): When True, all small (<= max_round) inner cells are rounded. Defaults to False.
        - max_iter_rows (int, optional): Maximum number of iterations. Defaults to 1000.

    Returns:
        pandas.DataFrame
    """
    if max_round is None:
        max_round = round_base - 1

    (rdata, freq_var, _, dim_var, hierarchies, formula) = prepare_input(
        data=data,
        freq_var=freq_var,
        dim_var=dim_var,
        formula=formula,
        hierarchies=hierarchies,
    )

    out = __scr.PLSroundingPublish(
        data=rdata,
        dim_var=dim_var,
        hierarchies=hierarchies,
        formula=formula,
        freqVar=freq_var,
        roundBase=round_base,
        maxRound=max_round,
        forceInner=force_inner,
        allSmall=all_small,
        maxIterRows=max_iter_rows,
    )
    return convert2py(out)
