"""ProcessingSteps for preprocessing.

This includes tasks like removal of baselines, averaging signals
or normalization.

Modules
-------
:py:mod:`~pyProcessingPipeline.steps.preprocessing.averaging`
    Steps for averaging signals.
:py:mod:`~pyProcessingPipeline.steps.preprocessing.baseline_correction`
    Steps for removing a signals baseline.
:py:mod:`~pyProcessingPipeline.steps.preprocessing.normalization`
    Steps for normalizing timeseries.
"""
from . import averaging, baseline_correction, normalization

__all__ = ["averaging", "baseline_correction", "normalization"]
