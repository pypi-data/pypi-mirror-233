"""Everything needed to get data in and out of the persistent database.

Timeseries data from the database is represented by
the TimeSeriesSet class, which can be created by either
importing a set of TimeSeries using the Importer, or
by re-creating it from a previously imported Set
with a known id.

Functions
---------
setup_processing_database
    Used for setting up a connection to
    the processing database.
    Must be called before doing anything
    persistence-related.

Classes
-------
Importer
    Used for importing timeseries data into the
    processing database.
TimeSeriesSet
    Used as an input for a ProcessingRun.
    Can be created by the Importer,
    or from a known SetID.

Modules
--------
Exceptions
    Contains database exceptions.
"""
from ._database import setup_processing_database
from ._importer import Importer
from ._timeseries import TimeSeriesSet

__all__ = [
    "Importer",
    "setup_processing_database",
    "TimeSeriesSet",
]
