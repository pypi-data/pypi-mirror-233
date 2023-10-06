import rpy2.robjects as ro
from .util import (
    convert2py,
    prepare_input,
)
from .pckg import importr_tryhard
from pandas import DataFrame

__gs = importr_tryhard("GaussSuppression")


def suppress_small_counts(
    data: DataFrame,
    max_n: int,
    freq_var: str = None,
    dim_var: list[str] = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
    formula: str = None,
    protect_zeros: bool = True,
    secondary_zeros: bool = False,
) -> DataFrame:
    """Wrapper function for suppressing small counts in frequency tables. See the documentation of SuppressSmallCounts in the R package GaussSuppression for all the details.

    Args:
        - data (DataFrame): Input data as pandas.DataFrame
        - max_n (int): Maximum value to be suppressed. Defaults to 3.
        - freq_var (str, optional): Name of the variable containing frequency information. Defaults to "freq".
        - dim_var (list[str], optional): List of variable names defining the categorical variables of the table. Defaults to None.
        - hierarchies (dict[str, DataFrame  |  list[DataFrame]], optional): A dictionary containing hierarchies. Each key is a variable name, each value is a list of pandas.DataFrames describing the hierarchies associated with the key. Defaults to None.
        - formula (str, optional): An R model formula for table definition. Defaults to None.
        - protect_zeros (bool, optional): Boolean value, determines whether zeros should be suppressed. Defaults to True.
        - secondary_zeros (bool, optional): Boolean value, determines whether zeros can be used as secondary suppressions. Defaults to False.

    Returns:
        pandas.DataFrame: A DataFrame containing the output table, as well as suppression information.
    """

    (
        rdata,
        freq_var,
        _,
        dim_var,
        hierarchies,
        formula,
    ) = prepare_input(
        data=data,
        freq_var=freq_var,
        num_var=None,
        dim_var=dim_var,
        hierarchies=hierarchies,
        formula=formula,
    )
    out = __gs.SuppressSmallCounts(
        data=rdata,
        maxN=max_n,
        freqVar=freq_var,
        dimVar=dim_var,
        hierarchies=hierarchies,
        formula=formula,
        protectZeros=protect_zeros,
        secondaryZeros=secondary_zeros,
    )
    return convert2py(out)


def suppress_few_contributors(
    data: DataFrame,
    max_n: int,
    freq_var: str = None,
    num_var: str = None,
    dim_var: list[str] = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
    formula: str = None,
    contributor_var=None,
    remove_codes: list[str] = None,
    remove0=True,
    protect_zeros=False,
    secondary_zeros=False,
) -> DataFrame:
    """Wrapper function for suppressing few contributors in magnitude tables. See the documentation of SuppressFewContributors in the R package GaussSuppression for all the details.

    Args:
        - data (DataFrame): Input data as pandas.DataFrame
        - max_n (int): Maximum number of contributors to be suppressed.
        - freq_var (str, optional): Name of the variable containing frequency information. Defaults to "freq".
        - num_var (str, optional): Name (or list of names) of variables containing numerical variables.
        - dim_var (list[str], optional): List of variable names defining the categorical variables of the table. Defaults to None.
        - hierarchies (dict[str, DataFrame  |  list[DataFrame]], optional): A dictionary containing hierarchies. Each key is a variable name, each value is a list of pandas.DataFrames describing the hierarchies associated with the key. Defaults to None.
        - formula (str, optional): An R model formula for table definition. Defaults to None.
        - contributor_var(str, optional): Variable determining contributor holding information. Defaults to None.
        - remove_codes(list[str], optional): List of codes to omitted when counting contributors. Defaults to None.
        - remove0(bool, optional): Boolean value to determine whether empty cells should be omitted in output. Defaults to True.
        - protect_zeros (bool, optional): Boolean value, determines whether zeros should be suppressed. Defaults to True.
        - secondary_zeros (bool, optional): Boolean value, determines whether zeros can be used as secondary suppressions. Defaults to False.

    Returns:
        pandas.DataFrame: A DataFrame containing the output table, as well as suppression information.
    """
    (
        rdata,
        freq_var,
        num_var,
        dim_var,
        hierarchies,
        formula,
    ) = prepare_input(
        data=data,
        freq_var=freq_var,
        num_var=num_var,
        dim_var=dim_var,
        hierarchies=hierarchies,
        formula=formula,
    )
    if remove_codes is None:
        remove_codes = ro.StrVector([])
    else:
        remove_codes = ro.StrVector(remove_codes)
    if contributor_var is None:
        contributor_var = ro.NULL
    out = __gs.SuppressFewContributors(
        data=rdata,
        maxN=max_n,
        freqVar=freq_var,
        numVar=num_var,
        dimVar=dim_var,
        hierarchies=hierarchies,
        formula=formula,
        contributorVar=contributor_var,
        removeCodes=remove_codes,
        remove0=remove0,
        protectZeros=protect_zeros,
        secondaryZeros=secondary_zeros,
    )
    return convert2py(out)


def suppress_dominant_cells(
    data: DataFrame,
    n: int | list[int],
    k: int | list[int],
    all_dominance: bool = False,
    freq_var: str = None,
    num_var: str = None,
    dim_var: list[str] = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
    formula=None,
    contributor_var=None,
    s_weight_var=None,
    protect_zeros=False,
    secondary_zeros=False,
) -> DataFrame:
    """Wrapper function for suppressing dominant cells in magnitude tables. See the documentation of SuppressDominantCells in the R package GaussSuppression for all the details.

    Args:
        - data (DataFrame): Input data as pandas.DataFrame
        - n (int | list[int]): a (list of) integer value to be used in the dominance rule. Must be same length as parameter `k`. Represents the number of contributing units.
        - k (int | list[int]): a (list of) integer value to be used in the dominance rule. Must be same length as parameter `n`.  Represents the percentage threshold in the dominance rule.
        - all_dominance (bool, optional): Boolean value that determines whether dominance information should be included in output. Defaults to False.
        - freq_var (str, optional): Name of the variable containing frequency information. Defaults to "freq".
        - num_var (str, optional): Name (or list of names) of variables containing numerical variables.
        - dim_var (list[str], optional): List of variable names defining the categorical variables of the table. Defaults to None.
        - hierarchies (dict[str, DataFrame  |  list[DataFrame]], optional): A dictionary containing hierarchies. Each key is a variable name, each value is a list of pandas.DataFrames describing the hierarchies associated with the key. Defaults to None.
        - formula (str, optional): An R model formula for table definition. Defaults to None.
        - contributor_var(str, optional): Variable determining contributor holding information. Defaults to None.
        - s_weight_var (_type_, optional): Variable name of the sampling weights. Defaults to None.
        - protect_zeros (bool, optional): Boolean value, determines whether zeros should be suppressed. Defaults to True.
        - secondary_zeros (bool, optional): Boolean value, determines whether zeros can be used as secondary suppressions. Defaults to False.
    Returns:
        pandas.DataFrame: A DataFrame containing the output table, as well as suppression information.
    """
    if type(n) != type(k):
        raise ValueError("n and k must both be int, or list of same length.")
    if isinstance(n, list):
        if len(n) != len(k):
            raise ValueError("n and k must have same length.")
        n = ro.IntVector(n)
        k = ro.IntVector(k)
    (
        rdata,
        freq_var,
        num_var,
        dim_var,
        hierarchies,
        formula,
    ) = prepare_input(
        data=data,
        freq_var=freq_var,
        num_var=num_var,
        dim_var=dim_var,
        hierarchies=hierarchies,
        formula=formula,
    )
    if contributor_var is None:
        contributor_var = ro.NULL
    if s_weight_var is None:
        s_weight_var = ro.NULL
    out = __gs.SuppressDominantCells(
        data=rdata,
        n=n,
        k=k,
        allDominance=all_dominance,
        freqVar=freq_var,
        numVar=num_var,
        dimVar=dim_var,
        hierarchies=hierarchies,
        formula=formula,
        contributorVar=contributor_var,
        sWeightVar=s_weight_var,
        protectZeros=protect_zeros,
        secondaryZeros=secondary_zeros,
    )
    return convert2py(out)


__all__ = [
    "suppress_small_counts",
    "suppress_few_contributors",
    "suppress_dominant_cells",
]
