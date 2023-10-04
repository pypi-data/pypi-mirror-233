"""IO-Related exceptions.

Contains all io-related exceptions.
Every exception is a subclass of the
main ProcessingError, so that they can
all be intercepted using a simple
::

    try:
        something()
    except ProcessingError:
        ...

"""

from pyProcessingPipeline.exceptions import ProcessingError


class UnknownStepClassError(ProcessingError, LookupError):
    """Raised if a class with the given StepName is not known."""

    def __init__(self, name: str) -> None:
        """Cannot find step with name {name}."""
        super().__init__(f"Cannot find step with name {name}.")


class UnknownStepIdError(ProcessingError, KeyError):
    """Raised if a step for a given ID was not found."""

    def __init__(self, step_id: int) -> None:
        """Could not load processing step with ID {step_id}."""
        super().__init__(f"Could not load processing step with ID {step_id}")


class UnknownSetError(ProcessingError, KeyError):
    """Raised if a TimeSeriesSet with a given ID does not exist."""

    def __init__(self, set_id: int) -> None:
        """TimeSeriesSet with ID {set_id} is unknown."""
        super().__init__(f"TimeSeriesSet with ID {set_id} is unknown.")


class UnknownSourceError(ProcessingError, KeyError):
    """Raised if a TimeSeriesSet's Source Table is unknown."""

    def __init__(self, source: str) -> None:
        """Source {source} not known."""
        super().__init__(f"Source {source} not known.")


class EmptySetError(ProcessingError):
    """Raised if a TimeSeriesSet contains no records."""

    def __init__(self, empty_object: object) -> None:
        """{empty_object} is empty."""
        super().__init__(f"{empty_object} is empty.")


class UnknownRecordError(ProcessingError, KeyError):
    """Raised if a record with a given source and id does not exist."""

    def __init__(self, source: str, record_id: int) -> None:
        """Unknown record with Source {source} and ID {record_id}."""
        super().__init__(f"Unknown record with Source {source} and ID {record_id}.")


class MissingTablesError(ProcessingError):
    """Raised if the database given is missing a required table.

    If this is the case, the database setup was probably skipped.
    """

    def __init__(self, db_name: str, missing_tables: set[str]) -> None:
        """Database {db_name} is missing tables!", missing_tables."""
        super().__init__(f"Database {db_name} is missing tables!", missing_tables)


class DatabaseConnectionNotSetError(ProcessingError):
    """Raised if the database connection has not been setup before trying to access the database.

    Call setup_database_connection first.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Database connection has not been set! "
            "Call setup_database_connection first."
        )


class UnknownUnitError(ProcessingError, KeyError):
    """Raised if a unit is unknown."""

    def __init__(self, unit: str) -> None:
        """Unknown unit {unit}."""
        super().__init__(f"Unknown unit {unit}.")


class UncreatableUnitError(ProcessingError, KeyError):
    """Raised if a unit could not be created."""

    def __init__(self, unit: str) -> None:
        """Could not create new unit {unit}."""
        super().__init__(f"Could not create new unit {unit}.")


class UnconvertibleTypeError(ProcessingError, TypeError):
    """Raised if a given type can not be converted to bytes."""

    def __init__(self, dtype: object, convert_target: object) -> None:
        """Cannot convert unknown dtype {dtype} into {convert_target}."""
        super().__init__(f"Cannot convert unknown dtype {dtype} into {convert_target}.")
