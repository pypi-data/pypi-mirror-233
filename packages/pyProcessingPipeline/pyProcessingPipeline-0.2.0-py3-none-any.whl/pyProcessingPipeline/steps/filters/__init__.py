"""Filter implementations as ProcessingSteps.

Filters are grouped by their type.

Modules
--------
:py:mod:`~pyProcessingPipeline.steps.filters.bessel`
    Filter implementations based on Bessel filters.
:py:mod:`~pyProcessingPipeline.steps.filters.butterworth`
    Filter implementations based on Butterworth filters.
:py:mod:`~pyProcessingPipeline.steps.filters.chebyshev`
    Filter implementations based on Chebyshev filters.
:py:mod:`~pyProcessingPipeline.steps.filters.fir`
    Finite-impulse-response filters
"""
from . import bessel, butterworth, chebyshev, fir

__all__ = ["bessel", "butterworth", "chebyshev", "fir"]
