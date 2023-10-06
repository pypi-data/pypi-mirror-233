"""
A Python package for applying output disclosure control to pandas.DataFrames.
It is first and foremost a set of wrappers that call the R functions that implement the methods.

The package consists of two main submodules:

- suppress: this module contains functions for applying cell suppression to tables. The current implementation includes a wrapper function for suppressing small counts in frequency tables.
- perturb: this module contains functions for applying perturbative methods to tables. Currently, the only implemented method is small count rounding. Future versions might include cell-key perturbation.
"""
__version__ = "0.0.10"
from . import suppress
from . import util
from . import perturb
from .pckg import __ssbtools


def example_data(name):
    return util.convert2py(__ssbtools.SSBtoolsData(name))
