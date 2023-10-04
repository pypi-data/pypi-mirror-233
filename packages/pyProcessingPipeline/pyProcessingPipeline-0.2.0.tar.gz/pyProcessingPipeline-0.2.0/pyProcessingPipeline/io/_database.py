"""Everything database related."""
# pylint: disable=global-statement
import datetime
import logging
import struct
from collections import namedtuple
from collections.abc import Generator
from contextlib import contextmanager
from enum import Enum, unique
from typing import Any, Literal, TypedDict

import mysql.connector
import numpy as np
from mysql.connector.abstracts import MySQLCursorAbstract as DatabaseCursor

from pyProcessingPipeline.io.exceptions import (
    DatabaseConnectionNotSetError,
    MissingTablesError,
    UnconvertibleTypeError,
    UncreatableUnitError,
    UnknownStepClassError,
    UnknownStepIdError,
    UnknownUnitError,
)
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_lookup import StepLookup
from pyProcessingPipeline.types import FloatArray, StepLog

logger = logging.getLogger(__name__)


ArrayType = Literal["float", "double", "integer", "unsignedInteger"]


@unique
class Tables(Enum):
    """All Tables contained in our processing database."""

    CHARACTERISTIC_TIME_SERIES = "CTS"
    CHARACTERISTIC_TS_SET = "CtsSet"
    CLINIC = "Clinic"
    CLINICAL_SET = "ClinicalSet"
    DIAGNOSE = "Diagnose"
    EXPERIMENTAL_SET = "ExperimentalSet"
    MACSIM = "MacSim"
    MACSIM_TIME_SERIES = "MTS"
    MEASUREMENT = "Measurement"
    PATIENT = "Patient"
    PARAMETER_SET = "ParamSet"
    PROCESSING_RUN = "ProcessingRun"
    PROCESSING_STEP = "ProcessingStep"
    RAW_TIME_SERIES = "RTS"
    SIMULATED_TIME_SERIES = "STS"
    SOLVER_RUN = "SolverRun"
    STATISTICAL_SET = "StatisticalSet"
    STEP_INPUT_MAPPING = "StepInputMapping"
    STEP_LOG = "StepLog"
    STEP_PARAMETERS = "StepParameters"
    STEP_RESULTS = "StepResults"
    TIMESERIES_SOURCE = "TimeSeriesSource"
    TIMESERIES_SET = "TimeSeriesSet"
    UNITS = "Units"
    WFDB = "ImportedWFDB"


#: Tables needed by the Processing package.
REQUIRED_TABLES: set[str] = {table.value for table in Tables}


@unique
class DatabaseSource(Enum):
    """All time series sources available."""

    RAW_TIME_SERIES = Tables.RAW_TIME_SERIES.value
    SIMULATED_TIME_SERIES = Tables.SIMULATED_TIME_SERIES.value
    MACSIM_TIME_SERIES = Tables.MACSIM_TIME_SERIES.value
    WFDB = Tables.WFDB.value


class _DatabaseConnection(TypedDict):
    """Contains login information for the processing database."""

    host: str
    database: str
    user: str
    password: str


# This is pretty much a singleton, since there will only
# ever be a single instance of this created in setup_database_connection.
# This can not be accessed outside of this module.
__DATABASE_CONNECTION: _DatabaseConnection = None  # type: ignore


def setup_processing_database(
    host: str, database: str, user: str, password: str
) -> None:
    """Set up the database connection, used for our processing pipeline.

    This also checks if the given database contains all tables
    needed.

    Parameters
    ----------
    host : str
        Host of the database. Can be an IP or hostname.
    database : str
        Name of the database to connect to.
    user : str
        Database user.
    password : str
        Password for the given database user.

    Raises
    ------
    MissingTablesError
        If the given database is missing any of the tables
        given in :py:const:`REQUIRED_TABLES`
    mysql.connector.Error
        If the given connection could not be established or the
        user does not have the required rights.
    """
    # Connection is global to emulate a Singleton,
    # which only exists once.
    global __DATABASE_CONNECTION  # noqa: PLW0603

    # Test connection, this might raise mysql errors.
    if __DATABASE_CONNECTION:
        logger.warning("Database connection already exists, will be overwritten.")
    with mysql.connector.connect(
        host=host, database=database, user=user, password=password
    ) as connection:
        logger.info("Connected to database %s", connection.database)
        # Check if all expected tables are present
        with connection.cursor() as cursor:
            cursor.execute("show tables;")
            rows = cursor.fetchall()
            tables = {row[0] for row in rows}
            if not REQUIRED_TABLES.issubset(tables):
                missing_tables = REQUIRED_TABLES.difference(tables)
                raise MissingTablesError(database, missing_tables)

    # Connection works, so store login info
    __DATABASE_CONNECTION = _DatabaseConnection(
        host=str(host),
        database=str(database),
        user=str(user),
        password=str(password),
    )


@contextmanager
def active_database_cursor() -> Generator[DatabaseCursor, None, None]:
    """Return a cursor for the (previously set) database connection.

    Using the cursor starts an SQL transaction which will only be
    commited if no error happens inside the scope of the context manager.

    If any error happens while using the context manager,
    the cursor rolls back previous changes and reraises
    the error.

    The cursor will automatically be closed once the context is exited.
    Use like
    ::

        with active_database_cursor() as cursor:
            cursor.execute("show tables;")
            tables = cursor.fetchall()

    Returns
    -------
    DatabaseCursor
        Cursor for the active database, which can be
        used to execute queries.

    Raises
    ------
    DatabaseConnectionNotSetError
        If the database connection has not been previously setup.
        This happens if :py:func:`setup_database_connection` has
        not been called by the user yet.
    """
    if __DATABASE_CONNECTION:
        with mysql.connector.connect(**__DATABASE_CONNECTION) as connection:
            with connection.cursor() as cursor:
                yield cursor
                # Try to commit all queries since no error happened.
                try:
                    logger.debug("Commiting SQL commands.")
                    connection.commit()
                except mysql.connector.DatabaseError as error:
                    logger.fatal(
                        "Rolling back SQL transaction because of error: %s", error
                    )
                    connection.rollback()
                    raise
    else:
        raise DatabaseConnectionNotSetError


def get_unit_id(unit: str, create_if_not_exists: bool = False) -> int:
    """Get the id of the given unit, used in the unit table.

    If the unit does not already exist, it can be
    created if create_if_not_exists is set to True.

    Parameters
    ----------
    unit : str
        Unit for which to get the id.
    create_if_not_exists : bool
        If set to True, unknown units will be created.
        Otherwise, nothing will be returned.

    Returns
    -------
    int
        ID of the given unit.

    Raises
    ------
    KeyError
        If the unit is unknown and create_if_not_exists is not set.
    """
    with active_database_cursor() as cursor:
        logger.debug("Getting Unit-ID for %s", unit)
        query = f"""
            SELECT id
            FROM {Tables.UNITS.value}
            WHERE name = %s
            LIMIT 1;
        """
        cursor.execute(operation=query, params=(str(unit),))
        row = cursor.fetchone()
        unit_id: int | None
        if row:
            unit_id = int(row[0])
            logger.debug("UnitID for %s is %s", unit, unit_id)
            return unit_id

        if create_if_not_exists:
            logger.debug("Trying to create new unit %s", unit)
            insert = f"""
                INSERT INTO {Tables.UNITS.value}
                (name)
                VALUES (%s)
            """
            cursor.execute(operation=insert, params=(str(unit),))
            unit_id = cursor.lastrowid
            if unit_id is not None:
                logger.debug("Created new unit %s with id %s", unit, unit_id)
                return unit_id
            raise UncreatableUnitError(unit)

    raise UnknownUnitError(unit)


def get_float_from_database(
    name: str, table: Tables | DatabaseSource, item_id: int
) -> float | None:
    """Get a single float value from the database.

    Parameters
    ----------
    name : str
        Name of the value to retrieve.
    table : Tables | DatabaseSource
        Table from which to retrieve the value.
    item_id : int
        The primary key for the item.

    Returns
    -------
    Optional[float]
        If a float was found, this returns the float.
        Otherwise, None is returned.
    """
    with active_database_cursor() as cursor:
        query = f"""
            SELECT {name}
            FROM {table.value}
            WHERE id = %s;
        """

        params = (item_id,)

        # Execute query
        cursor.execute(query, params)
        response = cursor.fetchone()

        # If the response is not empty, the given
        # record with source and id exists.
        if response:
            return float(response[0])

        return None


def get_int_from_database(
    name: str, table: Tables | DatabaseSource, item_id: int
) -> int | None:
    """Return a single integer value from our database.

    Parameters
    ----------
    name : str
        Name of the value to retrieve.
    table : Tables | DatabaseSource
        Table from which to retrieve the value.
    item_id : int
        The primary key for the item.

    Returns
    -------
    Optional[int]
        The requested integer, if it was found.
        Otherwise, None.
    """
    with active_database_cursor() as cursor:
        query = f"""
            SELECT {name}
            FROM {table.value}
            WHERE id = %s;
        """

        params = (item_id,)

        # Execute query
        cursor.execute(query, params)
        response = cursor.fetchone()

        # If the response is not empty, the given
        # record with source and id exists.
        if response:
            return int(response[0])

        return None


def get_string_from_database(
    name: str, table: Tables | DatabaseSource, item_id: int
) -> str | None:
    """Return a single string from our database.

    Parameters
    ----------
    name : str
        Name of the value to retrieve.
    table : Tables | DatabaseSource
        Table from which to retrieve the value.
    item_id : int
        The primary key for the item.

    Returns
    -------
    Optional[str]
        The requested string, if it was found.
        Otherwise, None.
    """
    with active_database_cursor() as cursor:
        query = f"""
            SELECT {name}
            FROM {table.value}
            WHERE id = %s;
        """

        params = (item_id,)

        # Execute query
        cursor.execute(query, params)
        response = cursor.fetchone()

        # If the response is not empty, the given
        # record with source and id exists.
        if response:
            return str(response[0])

        return None


def get_datetime_from_database(
    name: str, table: Tables | DatabaseSource, item_id: int
) -> datetime.datetime | None:
    """Return a single string from our database.

    Parameters
    ----------
    name : str
        Name of the value to retrieve.
    table : Tables | DatabaseSource
        Table from which to retrieve the value.
    item_id : int
        The primary key for the item.

    Returns
    -------
    Optional[str]
        The requested string, if it was found.
        Otherwise, None.
    """
    with active_database_cursor() as cursor:
        query = f"""
            SELECT {name}
            FROM {table.value}
            WHERE id = %s;
        """

        params = (item_id,)

        # Execute query
        cursor.execute(query, params)
        response = cursor.fetchone()

        # If the response is not empty, the given
        # record with source and id exists.
        if response:
            if isinstance(response[0], datetime.datetime):
                return response[0]

        return None


def get_array_from_database(
    name: str, table: Tables | DatabaseSource, item_id: int, dtype: ArrayType
) -> FloatArray | None:
    """Return a single array from our database.

    This parses the binary stored array into a numpy array.

    Parameters
    ----------
    name : str
        Name of the value to retrieve.
    table : Tables | DatabaseSource
        Table from which to retrieve the value.
    item_id : int
        The primary key for the item.

    Returns
    -------
    Optional[FloatArray]
        If the array was found, it is returned.
        Otherwise, None.
    """
    with active_database_cursor() as cursor:
        query = f"""
            SELECT {name}
            FROM {table.value}
            WHERE id = %s;
        """

        params = (item_id,)

        # Execute query
        cursor.execute(query, params)
        response = cursor.fetchone()

        # If response exists, we need to parse the record.
        if response:
            buffer: bytes
            buffer = response[0]
            # Parse bytes into numpy array
            data = bytes_to_array(buffer, dtype)
            return data

        return None


def array_to_bytes(
    array: FloatArray,
) -> tuple[bytes, ArrayType]:
    """Turn an array into little-endian bytes.

    These can be stored in the database and read
    using bytes_to_array.

    To convert an array to bytes, simply call this function.
    >>> import numpy as np
    >>> sample = np.array([1, 2, 3], dtype="int")
    >>> buffer, typename = array_to_bytes(sample)
    >>> buffer.hex(), typename
    ('010000000200000003000000', 'integer')

    Converting the received value back into an array
    works with bytes_to_array.
    >>> array = bytes_to_array(buffer, "integer")
    >>> array
    array([1, 2, 3], dtype=int32)

    You will have to know the datatype for this though.

    array_to_bytes can also be used to convert arrays to
    different datatypes before conversion, e.g an int-array
    to a float array:
    >>> import numpy as np
    >>> sample = np.array([1, 2, 3], dtype="float")
    >>> buffer, typename = array_to_bytes(sample)
    >>> buffer.hex(), typename
    ('000000000000f03f00000000000000400000000000000840', 'double')
    """
    match array.dtype:
        case np.float32:
            return np.array(array, dtype="<f").tobytes(), "float"
        case np.float64:
            return np.array(array, dtype="<d").tobytes(), "double"
        case np.int32 | np.int64:
            return np.array(array, dtype="<i").tobytes(), "integer"
        case np.uint32 | np.uint64:
            return np.array(array, dtype="<I").tobytes(), "unsignedInteger"
        case _:
            raise UnconvertibleTypeError(array.dtype, "bytes")


def bytes_to_array(byte_input: bytes, dtype: ArrayType) -> FloatArray:
    """Turn a bytebuffer from our database into an array.

    To convert bytes to an array, simply call this function.
    >>> import numpy as np
    >>> sample = bytes.fromhex('010000000200000003000000')
    >>> array = bytes_to_array(sample, "integer")
    >>> array
    array([1, 2, 3], dtype=int32)

    This also works with floats:
    >>> import numpy as np
    >>> sample = bytes.fromhex('000000000000f03f00000000000000400000000000000840')
    >>> array = bytes_to_array(sample, "double")
    >>> array
    array([1., 2., 3.])


    You will have to know the datatype for this.
    Trying to convert bytes into a wrong format might
    return weird results:
    >>> import numpy as np
    >>> sample = bytes.fromhex('000000000000f03f00000000000000400000000000000840')
    >>> array = bytes_to_array(sample, "float")
    >>> array
    array([0.   , 1.875, 0.   , 2.   , 0.   , 2.125], dtype=float32)

    Or it might fail alltogether:
    >>> import numpy as np
    >>> sample = bytes.fromhex('010000000200000003000000')
    >>> array = bytes_to_array(sample, "double")
    Traceback (most recent call last):
    ...
    ValueError: buffer size must be a multiple of element size
    """
    match dtype:
        case "float":
            return np.frombuffer(buffer=byte_input, dtype="<f")
        case "double":
            return np.frombuffer(buffer=byte_input, dtype="<d")
        case "integer":
            return np.frombuffer(buffer=byte_input, dtype="<i")
        case "unsignedInteger":
            return np.frombuffer(buffer=byte_input, dtype="<I")
        case _:
            raise UnconvertibleTypeError(dtype, "array")


RunDatabaseResponse = namedtuple(
    "RunDatabaseResponse",
    "name description lastmodified source mainIdIn subIdIn modelIn",
)


def get_run_from_database(
    cursor: DatabaseCursor, run_id: int
) -> RunDatabaseResponse | None:
    """Get a single run from the Database.

    Parameters
    ----------
    cursor : DatabaseCursor
        Cursor to our database.
    run_id : int
        The ID of the ProcessingRun whose info should be returned

    Returns
    -------
    RunDatabaseResponse:
        Response from the database.
    """
    query = """
        SELECT name, description, lastmodified, source, mainIdIn, subIdIn, modelIn
        from ProcessingRun
        WHERE id = %s
    """
    cursor.execute(operation=query, params=(run_id,))
    result = cursor.fetchone()
    if result is not None:
        return RunDatabaseResponse(*result)
    return None


StepDatabaseResponse = namedtuple(
    "StepDatabaseResponse",
    "id name description version stepNumber startTime endTime modelOut",
)


def get_all_steps_from_run(
    cursor: DatabaseCursor, run_id: int
) -> list[StepDatabaseResponse]:
    """Get all steps belonging to a processing run."""
    query = """
        SELECT id, name, description, version, stepNumber, startTime, endTime, modelOut
        from ProcessingStep
        WHERE prId = %s
    """
    cursor.execute(operation=query, params=(run_id,))
    return [StepDatabaseResponse(*result) for result in cursor.fetchall()]


StepParameterResponse = namedtuple("StepParameterResponse", "element name type value")


def get_step_parameters(cursor: DatabaseCursor, step_id: int) -> dict[str, Any]:
    """Get a step's parameters from Database."""
    query = """
        SELECT name, type, value
        FROM StepParameters
        WHERE stepId = %s
    """
    cursor.execute(operation=query, params=(step_id,))
    result = cursor.fetchall()
    parameters: dict[str, Any] = {}
    for item in result:
        name, typename, value = item
        match typename:
            case "integer":
                value = struct.unpack("<i", value)[0]
            case "double":
                value = struct.unpack("<d", value)[0]
            case _:
                raise UnconvertibleTypeError(typename, "integer or double")
        parameters[name] = value

    return parameters


def get_step_results(cursor: DatabaseCursor, step_id: int) -> list[FloatArray]:
    """Get a steps results from the database."""
    result_list: list[FloatArray] = []
    query = """
        SELECT element, type, data
        FROM StepResults
        WHERE stepId = %s
    """

    cursor.execute(operation=query, params=(step_id,))
    results = cursor.fetchall()
    result_list = [bytes_to_array(result[2], result[1]) for result in results]

    return result_list


StepIOMappingResponse = namedtuple("StepIOMappingResponse", "indexIn indexOut")


def get_step_io_mapping(
    cursor: DatabaseCursor, step_id: int
) -> list[StepIOMappingResponse]:
    """Get the IO Mapping for a given step."""
    query = """
        SELECT indexIn, indexOut
        FROM StepInputMapping
        WHERE stepId = %s
    """
    cursor.execute(operation=query, params=(step_id,))
    return [StepIOMappingResponse(*result) for result in cursor.fetchall()]


def get_step_logs(cursor: DatabaseCursor, step_id: int) -> list[StepLog]:
    """Get the IO Mapping for a given step."""
    query = """
        SELECT element, description, type, data
        FROM StepLog
        WHERE stepId = %s
    """
    cursor.execute(operation=query, params=(step_id,))

    logs: list[StepLog] = []

    for result in cursor.fetchall():
        index, description, datatype, bytevalue = result
        value = None
        try:
            match datatype:
                case "integer":
                    value = struct.unpack("<i", bytevalue)[0]
                case "double":
                    value = struct.unpack("<d", bytevalue)[0]
        except Exception:
            # Log value might also be an array, so check for that.
            try:
                value = bytes_to_array(bytevalue, datatype)
            except Exception as error:
                raise UnconvertibleTypeError(datatype, "StepLog") from error
        if value is not None:
            logs.append(
                StepLog(description=description, element_index=index, value=value)
            )
        else:
            raise UnconvertibleTypeError(datatype, "StepLog")

    return logs


def processing_step_from_database(step_id: int) -> ProcessingStep:
    """Recreate a processing step that was stored in the database.

    This re-instanciates a step with all of its parameters and results,
    which can be used as a starting point for another processing run.

    Parameters
    ----------
    step_id : int
        The step's ID, as stored in our database.

    Returns
    -------
    ProcessingStep
        The recreated processing step.
    """
    # Try to get the step info from our database
    with active_database_cursor() as cursor:
        # First, get the step info:
        query = f"""
            SELECT name, prId
            FROM {Tables.PROCESSING_STEP.value}
            WHERE id = %s
        """
        cursor.execute(operation=query, params=(step_id,))
        result = cursor.fetchone()
        if result is None:
            raise UnknownStepIdError(step_id)

        name: str
        run_id: int
        name, run_id = result

        # Find right step class
        step_class = StepLookup.get(name)
        if step_class is None:
            raise UnknownStepClassError(name)

        # Then we need to find the step's parameters:
        params = get_step_parameters(cursor=cursor, step_id=step_id)
        results = get_step_results(cursor=cursor, step_id=step_id)
        logs = get_step_logs(cursor=cursor, step_id=step_id)

    # And recreate it from those parameters
    step: ProcessingStep = step_class(**params)
    step._set_data(results)
    step._set_run_id(run_id)
    step._set_step_id(step_id)
    step._set_logs(logs)
    return step
