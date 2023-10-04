"""Misc steps for manipulating a series' length.

Classes
-------
:py:mod:`~pyProcessingPipeline.steps.misc.statistics`
    Averages multiple timeseries into a single one
:py:mod:`~pyProcessingPipeline.steps.misc.cut`
    Cuts the beginning and end off of a timeseries
:py:mod:`~pyProcessingPipeline.steps.misc.split`
    Splits a single timeseries into multiple smaller subseries
:py:mod:`~pyProcessingPipeline.steps.misc.unite`
    Unites multiple series into a larger series.
    Can be seen as the inverse of Split.
"""
from .cut import Cut
from .labels import Shuffle
from .split import Split
from .statistics import Average
from .unite import Unite

__all__ = ["Average", "Cut", "Split", "Unite", "Shuffle"]
