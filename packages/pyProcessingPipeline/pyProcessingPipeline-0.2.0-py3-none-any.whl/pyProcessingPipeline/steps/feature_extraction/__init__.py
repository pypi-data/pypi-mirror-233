"""Steps used for extracting features from timeseries.

These can then be used for classification tasks.

Modules
-------
:py:mod:`~pyProcessingPipeline.steps.feature_extraction.spectrum`
    Feature extraction from the complex frequency spectrum.
"""

from . import spectrum

__all__ = ["spectrum"]
