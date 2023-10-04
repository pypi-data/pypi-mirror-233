"""pyProcessingPipeline is a package for modifying timeseries data.

The pyProcessingPipeline package enables you to easily write and share
so called "processing pipelines", which are a way of specifying
sequential calculations on sets of timeseries data.

Usage
-----
To start using this package, simply import the ProcessingRun
and the steps module:

>>> from pyProcessingPipeline import ProcessingRun
>>> import pyProcessingPipeline.steps as prs

Now you can create a run definition and add some steps,
which will be executed in the order they are added:

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
...     prs.preprocessing.normalization.NormalizeFundamentalFrequency()
... )

The run can then be executed by givin ig a sequence of timeseries,
e.g. numpy arrays

>>> import numpy as np
>>> sample_signal_one = np.sin(np.linspace(0, 2*np.pi, 200))
>>> sample_signal_two = np.sin(np.linspace(0, 4*np.pi, 200))

and simply calling the run function with your sequence of signals

>>> pr.run([sample_signal_one, sample_signal_two])

The results will then be available in the run's result:

>>> pr.results
[array(...), array(...)]


Persisting a ProcessingRun
--------------------------
Processing runs, including their inputs, outputs and intermediate
step results can be persisted in a MySQL database.
For this, you will have to have setup your MySQL database with
the required tables.

>>> from pyProcessingPipeline import setup_processing_database
>>> setup_processing_database(
...     host="localhost",
...     database="processing_db",
...     user="processing_pipeline_user",
...     password="processing",
... )
... # doctest: +SKIP


Persistent runs require a TimeSeriesSet, which can either be imported

>>> from pyProcessingPipeline import Importer
>>> time_series_set = Importer.import_wfdb(
...     records="wfdb_sample_dataset/physionet.org/files/bidmc/1.0.0",
...     timeseries_name="Sample wfdb timeseries",
...     description="This is a sample run for our documentation."
...     "It uses the WFDB import as a source.",
...     signal_name="RESP,",
... )
... # doctest: +SKIP

or re-created from a pre-existing TimeSeriesSet

>>> time_series_set = TimeSeriesSet(set_id=1337)
... # doctest: +SKIP

For more info on creating TimeSeriesSet inputs, see the io-Package.

Once you have a persistent TimeSeriesSet, simply create a run
with persist_results = True

>>> persistent_run = ProcessingRun(
...     name="ExampleRun",
...     description="Run that is persisted in the database",
...     persist_results = True
... )

You can then call the run-function with your persistent input

>>> persistend_run.run(time_series_set)
... # doctest: +SKIP

which will have persisted the run in your database.


Modules
---------------------
:py:mod:`~pyProcessingPipeline.processing_run`
    Contains the definition of the main component, the ProcessingRun.
:py:mod:`~pyProcessingPipeline.steps`
    Contains every ProcessingStep.
    Steps are the building blocks of every ProcessingRun.
:py:mod:`~pyProcessingPipeline.io`
    Contains everything needed to get data in and
    out of the persistence layer (currently MySQL only).
:py:mod:`~pyProcessingPipeline.exceptions`
    Contains the base class for every exception thrown
    by the processing package. Use this in try/except blocks
    to keep your program from crashing in case of an error.
:py:mod:`~pyProcessingPipeline.types`
    Contains type definitions used throughout the processing package,
    Mostly used internally.
:py:mod:`~pyProcessingPipeline.util`
    Helper functions.
"""

from .io import Importer, TimeSeriesSet, setup_processing_database
from .processing_run import ProcessingRun

__all__ = [
    "Importer",
    "ProcessingRun",
    "setup_processing_database",
    "TimeSeriesSet",
]
