"""Contains functions for importing records.

To import records, call the classmethods of the
Importer class. Remember to setup your database
connection first.
::

    from pyProcessingPipeline import Importer, setup_processing_database

    # Setup database credentials
    setup_processing_database(
        host="127.0.0.1",
        database="processing_db",
        user="processing_pipeline_user",
        password="processing_password",
    )

    # Import every wfdb file from a given path. The given signal name
    # has to be present in every found record.
    new_timeseries_set = Importer.import_wfdb(
        records="wfdb_sample_dataset/physionet.org/files/bidmc/1.0.0",
        timeseries_name="Imported from Path",
        description="This timeseries was imported by importing every file from a path.",
        signal_name="RESP,",
    )


Classes
-------
Importer
    Used for importing records.
"""
import logging
import os
from collections import defaultdict
from typing import TYPE_CHECKING, Any

import wfdb
from mysql.connector.abstracts import MySQLCursorAbstract

from ._database import Tables, active_database_cursor, array_to_bytes, get_unit_id
from ._timeseries import TimeSeriesSet

if TYPE_CHECKING:
    from pyProcessingPipeline.types import FloatArray

logger = logging.getLogger(__name__)


class Importer:
    """Used for importing timeseries into the processing database."""

    @classmethod
    def import_wfdb(
        cls,
        records: list[wfdb.Record] | os.PathLike[Any] | str,
        timeseries_name: str,
        description: str,
        signal_to_import: str,
    ) -> TimeSeriesSet:
        """Import wfdb records into processing database.

        This imports all given wfdb records (or all wfdb records
        found in the given path) into the processing database
        and groups them into a new TimeSeriesSet.
        The newly created TimeSeriesSet will be returned.
        This can then be used in processing runs.
        ::

            # Import all wfdb files from path.
            # Every record has to contain the given signal_name.
            time_series_set = Importer.import_wfdb(
                records="path/to/wfdb/records",
                timeseries_name="Sample wfdb timeseries",
                description="This is a sample run for our documentation."
                "It uses the WFDB import as a source.",
                signal_to_import="RESP,",
            )

        If you know that some records don't contain a signal
        name, you'll have to filter and read them yourself and instead
        call the importer with a list of records.
        Still, every given record should contain the signal_to_import that
        you wish to import.
        ::

            records: list[wfdb.Record] = []
            records.append(wfdb.rdrecord("path/to/record/00"))

            time_series_set = Importer.import_wfdb(
                records=records,
                timeseries_name="Sample wfdb timeseries",
                description="This is a sample run for our documentation."
                + "It uses the WFDB import as a source.",
                signal_to_import="RESP,",
            )

        Parameters
        ----------
        records : list[wfdb.Record] | os.PathLike | str
            The records to import, or a path that contains all
            records to import.
        timeseries_name : str
            Name under which to create the new TimeSeriesSet.
            Only used for descriptive purposes.
        description : str
            Description for the newly created TimeSeriesSet.
        signal_to_import : str
            Name of the signal contained in each wfdb record that
            should be imported.
            Only the same signal name can be imported per function call
            e.g. "RESP", "AVR",...
            This is done so that each TimeSeriesSet consists only of
            signals of the same type.

        Returns
        -------
        TimeSeriesSet
            The newly created TimeSeriesSet, ready to be used in a
            processing run.

        Raises
        ------
        TypeError
            If the given records is not a path/str or not a list of
            wfdb records.
        """
        # Switch record type
        if isinstance(records, str | os.PathLike):
            return _create_timeseries_set_from_wfdb_path(
                path=records,
                timeseries_name=timeseries_name,
                description=description,
                signal_to_import=signal_to_import,
            )
        if isinstance(records, list):
            return _create_timeseries_set_from_wfdb_records(
                records=records,
                timeseries_name=timeseries_name,
                description=description,
                signal_to_import=signal_to_import,
            )
        raise TypeError(
            f"Expected Pathlike or list of wfdb.Record, got {type(records)}"
        )


def _create_timeseries_set_from_wfdb_path(
    path: os.PathLike[Any] | str,
    timeseries_name: str,
    description: str,
    signal_to_import: str,
) -> TimeSeriesSet:
    """Import all WFDB records from path and return the newly created TimeSeriesSet.

    This reads all .dat files (wfdb records) in the given path,
    imports each one into the ImportedWFDB table, creates a TimeSeriesSet
    that links to all records and returns the newly created TimeSeriesSet.

    Parameters
    ----------
    path : os.PathLike | str
        Folder from which to import all wfdb records.
    timeseries_name : str
        Name under which to create the new TimeSeriesSet.
        Only used for descriptive purposes.
    description : str
        Description of the newly created TimeSeriesSet.
    signal_to_import : str
        Name of the signal that should be imported from the
        wfdb records.
        Every record in the given folder path must contain this
        signal, otherwise a KeyError is raised.

    Returns
    -------
    TimeSeriesSet
        The newly imported TimeSeriesSet. This can now be used
        as an input for a new processing run.

    Raises
    ------
    NotImplementedError
        _description_
    """
    # Find all .dat files in give folder
    records: list[wfdb.Record] = []
    all_files = os.listdir(path)
    wfdb_files = [file for file in all_files if file.endswith(".dat")]
    logger.debug("Found %d wfdb files in path %s", len(wfdb_files), path)
    if not wfdb_files:
        raise LookupError("Could not find any wfdb records in", path)
    for wfdb_file in wfdb_files:
        record = wfdb.rdrecord(os.path.join(path, wfdb_file).removesuffix(".dat"))
        records.append(record)

    if not records:
        raise ValueError("Could not load any wfdb records from", path)

    return _create_timeseries_set_from_wfdb_records(
        records=records,
        timeseries_name=timeseries_name,
        description=description,
        signal_to_import=signal_to_import,
    )


def _create_timeseries_set_from_wfdb_records(
    records: list[wfdb.Record],
    timeseries_name: str,
    description: str,
    signal_to_import: str,
) -> TimeSeriesSet:
    """Import the given wfdb records and return the created TimeSeriesSet.

    This imports all given records into the ImportedWFDB table,
    creates a TimeSeriesSet that links to all records and
    returns the TimeSeriesSet with the newly created setId.

    Parameters
    ----------
    records : list[wfdb.Record]
        List of all WFDB records that should be imported.
    timeseries_name : str
        Name of the TimeSeriesSet that should be created.
    description : str
        Description of the TimeSeriesSet that should be created.
    signal_to_import : str
        The signal name of the signal that should be imported.
        Only the same signal name can be imported per function call
        e.g. "RESP", "AVR",...
        This is done so that each TimeSeriesSet consists only of
        signals of the same type.


    Returns
    -------
    TimeSeriesSet
        The newly created TimeSeriesSet, which includes the setId.

    Raises
    ------
    TypeError
        If not all given records are wfdb records.
    ValueError
        If any of the records are missing the p_signal (physical signal).
    KeyError
        If the given signal_to_import does not exist in every given
        record.
    """
    # Validate input data
    if not all(isinstance(record, wfdb.Record) for record in records):
        raise TypeError("Not all items in records list are wfdb records!")
    if not all((signal.size > 0 for signal in record.p_signal) for record in records):
        # Check which records are missing the signal
        files_with_missing_p_signal: set[str] = set()
        for record in records:
            if not all(signal.size > 0 for signal in record.p_signal):
                files_with_missing_p_signal = files_with_missing_p_signal.union(
                    set(record.file_name)
                )
        raise ValueError(
            "Some records are missing a physical signal!",
            f"Files with a missing p_signal: {files_with_missing_p_signal}",
        )
    if not all(signal_to_import in record.sig_name for record in records):
        # Check which signal names are actually available in every record
        signal_counts: dict[str, int] = defaultdict(int)
        available_signals: list[str] = []
        for record in records:
            for signal_name in record.sig_name:
                signal_counts[signal_name] += 1
        # Remove signals that aren't available in every record
        for signal, counter in signal_counts.items():
            if counter == len(records):
                available_signals.append(signal)
        raise KeyError(
            f"Signal '{signal_to_import}' was not found in every record!",
            f"Signals available in every record are: {available_signals}.",
            f"Other signals found (and how often): {dict(signal_counts)}",
        )

    # Insert record / records into WFDB table
    # and remember which IDs they have.
    with active_database_cursor() as cursor:
        record_ids = [
            _import_single_wfdb_record(
                record=record, signal_name=signal_to_import, cursor=cursor
            )
            for record in records
        ]

        # Create new entry in TimeSeriesSource, using the given name
        # and description. This entries ID is the setId we'll be using to
        # group all records together in TimeSeriesSet
        insert = f"""
            INSERT INTO {Tables.TIMESERIES_SOURCE.value}
            (name, description, source)
            VALUES (%s, %s, %s)
        """
        cursor.execute(
            operation=insert, params=(timeseries_name, description, Tables.WFDB.value)
        )
        set_id = cursor.lastrowid
        if set_id is None:
            raise RuntimeError("Could not create new TimeSeriesSource entry!")

        # Create one entry per record in TimeSeriesSet, using the set_id from
        # above and setting the sourceId to the record_id from our ImportedWFDB table.
        insert = f"""
            INSERT INTO {Tables.TIMESERIES_SET.value}
            (setId, elementId, sourceId)
            VALUES (%s, %s, %s)
        """
        for element_index, record_id in enumerate(record_ids):
            cursor.execute(operation=insert, params=(set_id, element_index, record_id))

    return TimeSeriesSet(set_id=set_id)


def _import_single_wfdb_record(
    record: wfdb.Record, signal_name: str, cursor: MySQLCursorAbstract
) -> int:
    """Import a single wfdb record and return the record id.

    This imports the given record into the ImportedWFDB
    table and returns the unique ID of the imported record.

    Parameters
    ----------
    record : WFDBRecord
        Single WFDBRecord that should be imported
    signal_name : str
        Name of the signal that should be imported from the record.

    Returns
    -------
    int
        Unique record ID that was created when inserting the record.
    """
    insert_sql = f"""
        INSERT INTO {Tables.WFDB.value}
        (record_name, comments, sig_name, unit, p_signal, signal_type, sampling_rate)
        VALUES (%s, %s, %s, %s, _binary %s, %s, %s)
    """

    signal_index: int = record.sig_name.index(signal_name)
    sig_name: str = record.sig_name[signal_index]
    record_name: str = record.record_name
    comments = str(record.comments)
    unit: str = record.units[signal_index]
    p_signal: FloatArray = record.p_signal[:, signal_index]
    sampling_rate: int = record.fs

    # Get unit's id
    unit_id = get_unit_id(unit=unit, create_if_not_exists=True)

    logger.debug("Inserting WFDB record into table.")
    buffer, signal_type = array_to_bytes(p_signal)
    cursor.execute(
        operation=insert_sql,
        params=(
            record_name,
            comments,
            sig_name,
            unit_id,
            buffer,
            signal_type,
            sampling_rate,
        ),
    )
    record_id = cursor.lastrowid
    if record_id is not None:
        logger.debug("Inserted new WFDB record with ID %s", record_id)
        return record_id
    raise RuntimeError("Could not insert WFDB record!")
