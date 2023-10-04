"""Contains the TimeSeriesSet class.

This is the main persistent input for our processing pipeline.

A TimeSeriesSet can be created by using the Importer,
or by re-creating it from a previously imported
Set with a known SetID.

To import a TimeSeriesSet, see the _importer package.

To recreate a TimeSeriesSet from a known SetID, simply
init the set with that ID:

>>> ts_set = TimeSeriesSet(set_id=12345)
... # doctest: +SKIP


"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pyProcessingPipeline.types import ProcessingStepInput, ProcessingStepOutput

from ._database import (
    DatabaseSource,
    Tables,
    active_database_cursor,
    get_datetime_from_database,
    get_int_from_database,
    get_string_from_database,
)
from ._records import TimeSeriesRecord
from .exceptions import EmptySetError, UnknownSetError, UnknownSourceError

if TYPE_CHECKING:
    import datetime

logger = logging.getLogger(__name__)


class TimeSeriesSet(ProcessingStepInput):
    """Representation of a TimeSeriesSet from the processing database.

    This is the main input used for our ProcessingRuns.
    It is uniquely identified by its set_id.

    TimeSeriesSets can not be created by themself, they
    can only be recreated from previously persisted timeseriessets.
    To recreate a set with a known ID, simply call

    >>> ts_set = TimeSeriesSet(set_id=12345)
    ... # doctest: +SKIP

    To create a completely new TimeSeriesSet, you have to use the
    processing.Importer.
    """

    _set_id: int
    _name: str
    _description: str
    _source: DatabaseSource
    _lastmodified: datetime.datetime | None

    _records: list[TimeSeriesRecord]
    _data: ProcessingStepOutput

    def __init__(self, set_id: int) -> None:
        """Create a TimeSeriesSet from a given set_id.

        This set_id should already exist in the processing db.

        Parameters
        ----------
        set_id : int
            The id of the set for which this class should be instantiated.

        Raises
        ------
        UnknownSetError
            If the given set_id is unknown.
        """
        self._set_id = int(set_id)
        if not self.__check_if_set_exists():
            raise UnknownSetError(set_id)
        # Check if source is a known table.
        _ = self.source

    def __repr__(self) -> str:
        return f"TimeSeriesSet {self.set_id} : {self.name}"

    def __len__(self) -> int:
        return len(self.records)

    def __check_if_set_exists(self) -> bool:
        """Check if this instance's set_id exists in our processing db.

        Returns
        -------
        bool
            True if the set exists, else False.
        """
        set_id = get_int_from_database(
            name="id", table=Tables.TIMESERIES_SOURCE, item_id=self.set_id
        )
        if set_id == self.set_id:
            return True
        return False

    @property
    def set_id(self) -> int:
        """ID of the TimeSeriesSet, as specified in our processing db."""
        # This is setup as a property so that it is impossible to be
        # overwritten once instanciated. This makes sure that we always deal
        # with a valid set id.
        return self._set_id

    @property
    def name(self) -> str:
        """The name of this TimeSeriesSet."""
        if not hasattr(self, "_name"):
            self._name = (
                get_string_from_database(
                    name="name", table=Tables.TIMESERIES_SOURCE, item_id=self.set_id
                )
                or "Unknown"
            )

        return self._name

    @property
    def description(self) -> str:
        """Description of this TimeSeriesSet."""
        if not hasattr(self, "_description"):
            self._description = (
                get_string_from_database(
                    name="description",
                    table=Tables.TIMESERIES_SOURCE,
                    item_id=self.set_id,
                )
                or "Unknown"
            )

        return self._description

    @property
    def source(self) -> DatabaseSource:
        """Database source where the Set entries are stored.

        E.g. STS, ImportedWFDB etc.
        """
        if not hasattr(self, "_source"):
            source = get_string_from_database(
                name="source", table=Tables.TIMESERIES_SOURCE, item_id=self.set_id
            )
            match source:
                case Tables.MACSIM_TIME_SERIES.value:
                    self._source = DatabaseSource.MACSIM_TIME_SERIES
                case Tables.RAW_TIME_SERIES.value:
                    self._source = DatabaseSource.RAW_TIME_SERIES
                case Tables.SIMULATED_TIME_SERIES.value:
                    self._source = DatabaseSource.SIMULATED_TIME_SERIES
                case Tables.WFDB.value:
                    self._source = DatabaseSource.WFDB
                case _:
                    raise UnknownSourceError(str(source))

        return self._source

    @property
    def lastmodified(self) -> datetime.datetime | None:
        """Unixtimestamp (UTC) when the Set was last modified."""
        if not hasattr(self, "_lastmodified"):
            self._lastmodified = get_datetime_from_database(
                name="lastmodified", table=Tables.TIMESERIES_SOURCE, item_id=self.set_id
            )

        return self._lastmodified

    @property
    def records(self) -> list[TimeSeriesRecord]:
        """All records contained in this TimeSeriesSet."""
        if not hasattr(self, "_records"):
            self._get_records_from_database()

        return self._records

    @property
    def data(self) -> ProcessingStepOutput:
        if not hasattr(self, "_data"):
            self._data = []
            logger.info("Getting record data for %s.", self)
            self._data = [record.data for record in self.records]

        return self._data

    def _get_records_from_database(self) -> None:
        # Find all record IDs for this set:
        with active_database_cursor() as cursor:
            query = f"""
                SELECT sourceId
                FROM {Tables.TIMESERIES_SET.value}
                WHERE setId = %s
                ORDER BY elementId ASC;
            """
            params = (self.set_id,)

            # Execute query:
            cursor.execute(operation=query, params=params)
            rows = cursor.fetchall()
            if rows is not None:
                record_ids = [int(item[0]) for item in rows]
            else:
                raise EmptySetError(self)

            logger.info("Found %d records in %s", len(record_ids), self)

        # Create records.
        self._records = [
            TimeSeriesRecord.new(source=self.source, record_id=record_id)
            for record_id in record_ids
        ]
