"""All processing steps available in the pipeline.

Steps are the building block of the processing package.
Every step implements a specific data manipulation step,
like filtering, cutting, averaging, and many more.

Steps, together with the ProcessingRun, can make it easier
to create and share scripts for data processing.

E.g. to filter a signal and cut off the begining and end,
you would simply create a run that contains the right steps

>>> from pyProcessingPipeline import ProcessingRun
>>> import pyProcessingPipeline.steps as prs
>>> import numpy as np
>>> signal = np.sin(np.linspace(0, 2*np.pi, 100))
>>> pr = ProcessingRun(
...     name="ExampleRun",
...     description="Run that does some things :)",
... )
>>> pr.add_step(
...     prs.filters.butterworth.LowpassButter(
...         cutoff_frequency=1.5,
...         filter_order=3,
...         sampling_frequency=125,
...     )
... )
>>> pr.add_step(
...     prs.misc.Cut(
...         global_lower_bound=10,
...         global_upper_bound=90
...     )
... )
>>> pr.run([signal])

Modules
--------
:py:mod:`~pyProcessingPipeline.steps.feature_extraction`
    Contains steps for feature extraction.
:py:mod:`~pyProcessingPipeline.steps.filters`
    Contains filters for filtering a signal.
:py:mod:`~pyProcessingPipeline.steps.misc`
    Contains miscellaneous functions, like cutting, uniting...
:py:mod:`~pyProcessingPipeline.steps.preprocessing`
    Contains steps specifically made for preprocessing, like Baseline removal
"""
from . import classification, feature_extraction, filters, misc, preprocessing

__all__ = ["feature_extraction", "filters", "misc", "preprocessing", "classification"]
