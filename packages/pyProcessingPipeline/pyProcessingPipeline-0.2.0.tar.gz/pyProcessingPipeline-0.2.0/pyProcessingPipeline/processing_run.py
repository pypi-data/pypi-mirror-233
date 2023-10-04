"""ProcessingRun is the main class that makes the processing pipeline possible.

It is used to define a complete pipeline,
chaining multiple ProcessingSteps together,
keeping intermediate results and handling the
persistence of every result.

Classes
-------
ProcessingRun
    Used to chain ProcessingSteps together and
    executing them in order.

"""

import datetime
import logging
import struct
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np
from mysql.connector.abstracts import MySQLCursorAbstract as DatabaseCursor

from .exceptions import ProcessingError
from .io._database import Tables, active_database_cursor, array_to_bytes
from .io._timeseries import TimeSeriesSet
from .steps._base import ProcessingStep
from .types import (
    FloatArray,
    LabeledProcessingStepInput,
    LabelMapping,
    ListBasedProcessingStepInput,
    ProcessingStepInput,
    ProcessingStepOutput,
)

logger = logging.getLogger(__name__)


class UnpersistableInputError(ProcessingError):
    """Raised if the input given for a ProcessingRun is not persistable in our database."""


@dataclass
class _ProcessingRunInfo:
    """Info object for a processing run.

    Attributes
    ----------
    name : str
        Name of the processing run.
    description : str
        Description of the processing run.
    lastmodified : datetime.datetime
        Time the run was last modified.
    is_persistent : bool
        Wether the results are stored in our database or not.
    """

    name: str
    description: str
    lastmodified: datetime.datetime
    is_persistent: bool


@dataclass
class _ProcessingRunDatabaseInfo:
    """Info object that keeps a processing run's data related to the persistent data store.

    Attributes
    ----------
    run_id : int
        The main run ID in our database.
    source : Literal["TS", "PS"]
        Wether this run used a TimeSeriesSet or a
        previous ProcessingStep as input.
    main_id : int
        ID of the TimeSeriesSet or the
        ProcessingRun the input step belongs to.
    sub_id: Optional[int]
        ID of the ProcessingStep whose results were
        used as input, if the source is "PS".
    """

    run_id: int
    source: Literal["TS", "PS"]
    main_id: int
    sub_id: int | None


class ProcessingRun:
    """Class used for managing ProcessingSteps.

    A ProcessingRun is used for chaining multiple
    processing steps together into a single unit,
    which can then be applied to multiple timeseries
    at once.
    A processing run can be used offline or with a database.

    Creating a processing run is as easy as instantiating this class,
    adding whatever processing steps you might want, and calling run
    with the sequence of timeseries that you want to transform.

    Creating a run
    --------------

    Simply create an instance of this processing run class:

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="This is a sample run which uses some test data.",
    ... )

    Now you may add as many steps as you want.

    >>> from pyProcessingPipeline.steps.misc import Average, Cut, Split
    >>> processing_run.add_step(Cut(global_lower_bound=0, global_upper_bound=4))
    >>> processing_run.add_step(Average(average_over=2))
    >>> processing_run.add_step(Split(2))

    and however many more steps you might want to add.
    Steps are executed in the order they are added.

    To start processing your input, you will need some sequence of
    input signals (in this case, a simple example):

    >>> signals = [
    ...     [1, 1, 1, 1, 1],
    ...     [1, 2, 3, 4, 5],
    ...     [5, 4, 3, 2, 1],
    ...     [1, 2, 3, 4, 5]
    ... ]

    To start the calculations, simply call
    'run' on your sequence of timeseries:

    >>> processing_run.run(signals)
    ... # Results will then be available in the run's results:
    >>> processing_run.results
    [array([1. , 1.5]), array([2. , 2.5]), array([3., 3.]), array([3., 3.])]

    To find out which input got mapped to which output, every step keeps
    a mapping like so:

    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 1, 2: 2, 3: 3}

    Steps might also reduce multiple inputs to a single output,
    like Average:

    >>> processing_run.steps[1].input_mapping
    {0: 0, 1: 0, 2: 1, 3: 1}

    Other steps might again turn a single input into
    multiple outputs, like Split:

    >>> processing_run.steps[2].input_mapping
    {0: [0, 1], 1: [2, 3]}

    If an output could not be calculated for an input,
    because some kind of error happened, the input
    will be mapped to None:

    >>> from pyProcessingPipeline.steps.preprocessing.averaging import CoherentAveraging
    >>> processing_run.add_step(CoherentAveraging())
    >>> processing_run.run(signals)
    >>> processing_run.results
    []

    >>> processing_run.steps[3].input_mapping
    {0: None, 1: None, 2: None, 3: None}
    """

    _info: _ProcessingRunInfo
    _database_info: _ProcessingRunDatabaseInfo
    _steps: list[ProcessingStep]
    _labels: Sequence[str | None] | None = None

    def __init__(
        self, name: str, description: str, persist_results: bool = False
    ) -> None:
        """Create a ProcessingRun from a given input.

        Parameters
        ----------
        name : str
            Name of this processing run, which is stored in the database
            if persist_results is True.
        description : str
            Description of this run, stored in our database if
            persist_results is True.
        persist_results : bool, optional
            Wether to persist results in our database, by default False.
        """
        self._steps = []
        self._info = _ProcessingRunInfo(
            name=name,
            description=description,
            lastmodified=datetime.datetime.now(),
            is_persistent=persist_results,
        )

    def add_step(self, step: ProcessingStep) -> None:
        """Add a processing step to this run.

        ProcessingSteps are applied to the input of a run
        sequentially.

        Parameters
        ----------
        step : ProcessingStep
            The step which should be added to this processing run.
        """
        self._steps.append(step)
        logger.info("Added step %s to run %s.", step, self)

    def run(
        self,
        run_input: ProcessingStepInput | list[FloatArray],
    ) -> None:
        """Run the ProcessingRun on all added steps with given input.

        Parameters
        ----------
        run_input : ProcessingStepInput
            _description_
        """
        # Auto-convert lists to a regular processing step input
        if isinstance(run_input, list):
            step_input: ProcessingStepInput = ListBasedProcessingStepInput(run_input)
        else:
            step_input = run_input

        match self.info.is_persistent:
            case True:
                self._run_with_persistence(step_input)
            case False:
                self._run_without_persistence(step_input)

    def _run_with_persistence(self, step_input: ProcessingStepInput) -> None:
        # Creating the database cursor now makes sure that
        # all commands are only commited to our database if
        # no error happens. Otherwise, a rollback is performed.
        with active_database_cursor() as cursor:
            # Store current run in database and get run_id:
            self._init_persistent_run(cursor=cursor, first_step=step_input)
            labels = self._get_labels_from_initial_step_input(step_input)

            for index, step in enumerate(self._steps):
                logger.info("Running step %d:%s with input %s", index, step, step_input)
                # Run step on previous output
                start_time = datetime.datetime.now()
                step.run(step_input, labels=labels)
                end_time = datetime.datetime.now()

                self._persist_step(
                    cursor=cursor,
                    step=step,
                    index=index,
                    start_time=start_time,
                    end_time=end_time,
                )

                # Set input for next step to be this step.
                self._steps[index] = step
                step_input = step

                # Also update labels for the next run, if the io/mapping exists
                # and the labels exist.
                labels = self._reindex_labels(labels, step.input_mapping)

        self._labels = labels
        logger.info("Finished run %s", self)

    def _run_without_persistence(self, step_input: ProcessingStepInput) -> None:
        labels = self._get_labels_from_initial_step_input(step_input)
        for index, step in enumerate(self._steps):
            logger.info("Running step %d:%s with input %s", index, step, step_input)
            # Run step on previous output
            step.run(step_input, labels=labels)

            # Set input for next step to be this step.
            self._steps[index] = step
            step_input = step

            # Also update labels for the next run, if the io/mapping exists
            # and the labels exist.
            labels = self._reindex_labels(labels, step.input_mapping)

        self._labels = labels
        logger.info("Finished run %s", self)

    def _get_labels_from_initial_step_input(
        self, timeseries: ProcessingStepInput | TimeSeriesSet
    ) -> Sequence[str | None] | None:
        """Get all labels from the step input.

        Retrieves all labels for every record in a TimeSeriesSet.

        Parameters
        ----------
        timeseries : ProcessingStepInput | TimeSeriesSet
            The first step_input of a ProcessingRun.

        Returns
        -------
        Sequence[str | None] | None
            If the given step_input is a TimeSeriesSet, this returns
            a list of optional labels.
            Otherwise, it returns None.
        """
        if isinstance(timeseries, TimeSeriesSet):
            return [record.label for record in timeseries.records]
        elif isinstance(timeseries, LabeledProcessingStepInput):
            return timeseries.labels
        return None

    @staticmethod
    def _reindex_labels(
        labels: Sequence[str | None] | None,
        io_mapping: LabelMapping,
    ) -> Sequence[str | None] | None:
        """Update labels by reindex them to fit the io mapping.

        This is done so that consecutive steps have access to the right labels,
        even if the original input index no longer corresponds to the right item.

        Parameters
        ----------
        labels : Sequence[str | None] | None
            Current list of labels or None.
        io_mapping : Optional[LabelMapping]
            Input/Output-mapping of the recently finished ProcessingStep.

        Returns
        -------
        Sequence[str | None] | None
            Reindexed list of labels to fit with the input indices of the
            next ProcessingStep.
        """
        # Don't do anything if there are no labels or no output index
        if labels is None or all(output is None for output in io_mapping.values()):
            return None

        # The output maps each output index to a label.
        output: dict[int, str | None] = {}

        for input_index, input_label in enumerate(labels):
            output_indices = io_mapping.get(input_index)
            match output_indices:
                case int(output_index):
                    # Check if output already contains a label
                    match output.get(output_index):
                        # No label in output yet, so set the new label
                        case None:
                            output[output_index] = input_label
                        # Label already exists, so check if they need to be merged.
                        case str(current_label):
                            if str(input_label) in current_label:
                                pass
                            else:
                                output[
                                    output_index
                                ] = f"{current_label}\r\n{input_label}"
                case list(_):
                    for output_index in output_indices:
                        # Same as above, but multiple times
                        # Check if output already contains a label
                        match output.get(output_index):
                            # No label in output yet, so set the new label
                            case None:
                                output[output_index] = input_label
                            # Label already exists, so check if they need to be merged.
                            case str(current_label):
                                if str(input_label) in current_label:
                                    pass
                                else:
                                    output[
                                        output_index
                                    ] = f"{current_label}\r\n{input_label}"
                case None:
                    pass

        # No we'll have to turn this dictionary mapping each index to a new label
        # into a list.
        # Find maximum index for iteration (yeah I know, iteration is slow)
        max_index = max(output.keys())

        output_list: Sequence[str | None] = [
            output.get(index) for index in range(max_index + 1)
        ]

        return output_list

    def _init_persistent_run(
        self, cursor: DatabaseCursor, first_step: ProcessingStepInput
    ) -> None:
        """Store the processing run in the database.

        This updates the run's _database_info.

        Parameters
        ----------
        cursor : DatabaseCursor
            Cursor to the active database.
        first_step : ProcessingStepInput
            The first step this Run is called for.
            This is used to set up the run's Source and IDs.

        Raises
        ------
        UnpersistableInput
            If the Input was a simple list-based input that was
            not previously imported to the database.
        ProcessingError
            If storing failed for whatever reason.
        """
        source: Literal["TS", "PS"]
        match first_step:
            case TimeSeriesSet():
                source = "TS"
                main_id = first_step.set_id
                sub_id = None
            case ProcessingStep():
                source = "PS"
                main_id = first_step.run_id
                sub_id = first_step.step_id
            case _:
                raise UnpersistableInputError(
                    f"Can not persist input of type {type(first_step)}! "
                    "Persistence is only available for TimeSeriesSets "
                    "or previously persisted ProcessingSteps"
                )

        query = f"""
            INSERT INTO {Tables.PROCESSING_RUN.value}
            (name, description, lastmodified, source, mainIdIn, subIdIn)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.info.name,
            self.info.description,
            self.info.lastmodified,
            source,
            main_id,
            sub_id,
        )
        cursor.execute(operation=query, params=params)
        run_id = cursor.lastrowid
        if run_id is None:
            raise ProcessingError("Could not store run_id!")

        self._database_info = _ProcessingRunDatabaseInfo(
            run_id=run_id, source=source, main_id=main_id, sub_id=sub_id
        )

    def _persist_step(
        self,
        cursor: DatabaseCursor,
        step: ProcessingStep,
        index: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ) -> None:
        """Store the given step in our database.

        This uses the given cursor, so that storing is
        rolled back if any error happens.

        Parameters
        ----------
        cursor : DatabaseCursor
            Database cursor to our current active database.
            Used for storing the step.
        step : ProcessingStep
            The step which should be stored in our database.
        index : int
            The index of the step in the current processing run.
            Used to track the order of steps.
        start_time : datetime.datetime
            Time when the step started execution.
        end_time : datetime.datetime
            Time when the step finished execution. Can be used
            to calculate the total time spent per step.
        """
        self._store_processing_step(
            cursor=cursor,
            step=step,
            index=index,
            start_time=start_time,
            end_time=end_time,
        )
        self._store_step_parameters(cursor=cursor, step=step)
        self._store_step_io_mapping(cursor=cursor, step=step)
        self._store_step_log(cursor=cursor, step=step)
        self._store_step_results(cursor=cursor, step=step)

    def _store_processing_step(
        self,
        cursor: DatabaseCursor,
        step: ProcessingStep,
        index: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ) -> None:
        """Store a single processing step in the database.

        The step is stored in the ProcessingStep table.
        This also updates the step's step_id, which uniquely
        identifies the step.

        Parameters
        ----------
        cursor : DatabaseCursor
            Cursor to our active database connection.
            Used for storing the step.
        step : ProcessingStep
            The step that should be persisted in our database.
        index : int
            The index of this step in the current processing run.
            This is used to keep the right order when storing
            steps.
        start_time : datetime.datetime
            When the step execution was started.
        end_time : datetime.datetime
            When the step was finished. Can be used to calculate
            the total time a step needed.

        Raises
        ------
        ProcessingError
            If the step could not be stored.
        """
        query = f"""
            INSERT INTO {Tables.PROCESSING_STEP.value}
            (name, description, version, prId, stepNumber, startTime, endTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            step.identifier().name,
            "Description Feature missing.",
            0,
            self._database_info.run_id,
            index,
            start_time,
            end_time,
        )

        cursor.execute(operation=query, params=params)
        step_id = cursor.lastrowid
        if step_id is None:
            raise ProcessingError("Could not store processing step!")

        # Make the step remember its own ID :)
        step._update_database_ids(step_id, self._database_info.run_id)

    def _store_step_parameters(
        self, cursor: DatabaseCursor, step: ProcessingStep
    ) -> None:
        """Store the parameters for the given step in our database.

        The step is assumed to have already been persisted,
        so it should contain a step_id.

        Parameters
        ----------
        cursor : DatabaseCursor
            Cursor for our active database connection.
        step : ProcessingStep
            The step whose parameters should be persisted.
            Has to contain a step_id.

        Raises
        ------
        ProcessingError
            If storing the parameters failed.
        """
        query = f"""
            INSERT INTO {Tables.STEP_PARAMETERS.value}
            (stepId, name, type, value)
            VALUES (%s, %s, %s, _binary %s)
        """
        params: list[tuple[int, str, str, bytes]] = []
        for parameter_name, parameter_value in step.parameters.items():
            # Allowed names for type are 'integer' and 'double'.
            # All values are stored as binary representations,
            # with little endian byte order.
            match parameter_value:
                case int(_):
                    representation = "integer"
                    byte_value = struct.pack("<i", parameter_value)
                case float(_):
                    representation = "double"
                    byte_value = struct.pack("<d", parameter_value)
                case _:
                    # We don't know in how to pack unknown values
                    # into bytes, so for now this raises an error
                    raise ProcessingError(
                        "Cannot convert unknown value of type "
                        f"{type(parameter_value)} to bytes!"
                    )
            # Add current parameter to list of parameters
            # to send to our database.
            params.append((step.step_id, parameter_name, representation, byte_value))

        cursor.executemany(operation=query, seq_params=params)

        row_id = cursor.lastrowid
        if row_id is None:
            raise ProcessingError("Could not store step parameters!")

    def _store_step_io_mapping(
        self, cursor: DatabaseCursor, step: ProcessingStep
    ) -> None:
        """Store the step's io mapping in our database.

        This stores the values that map each input
        to its corresponding output.
        Its an N:N mapping, meaning that a single input
        can be mapped to multiple outputs, and a
        single output can be mapped to multiple inputs.

        Parameters
        ----------
        cursor : DatabaseCursor
            Cursor for our active database connection.
        step : ProcessingStep
            The step whose input mapping should be stored.

        Raises
        ------
        ProcessingError
            If storing the mapping failed.
        """
        if step.input_mapping is None:
            return

        query = f"""
            INSERT INTO {Tables.STEP_INPUT_MAPPING.value}
            (stepId, indexIn, indexOut)
            VALUES (%s, %s, %s)
        """

        # Since the input mapping might map a single value
        # to a single output, to a list of outputs or to nothing
        # at all, we'll have to check which case it actually is.

        params: list[tuple[int, int, int]] = []
        for index_in, index_out in step.input_mapping.items():
            match index_out:
                case None:
                    # Skip storing this index,
                    # since it does not map to any output.
                    continue
                case list(_):
                    # Store multiple entries for this index,
                    # since it maps to multiple output values.
                    params.extend(
                        [
                            (step.step_id, index_in, output_index)
                            for output_index in index_out
                        ]
                    )
                case int(_):
                    # Store single entry for this index
                    params.append((step.step_id, index_in, index_out))
                case _:
                    raise ProcessingError(
                        f"Cannot map input index {index_in}"
                        f" to unknown value {index_out}"
                    )

        cursor.executemany(operation=query, seq_params=params)
        row_id = cursor.lastrowid
        if row_id is None:
            raise ProcessingError("Could not store step input mapping!")

    def _store_step_log(self, cursor: DatabaseCursor, step: ProcessingStep) -> None:
        """Store a step's logs in our database.

        Parameters
        ----------
        cursor : DatabaseCursor
            Cursor for the currently active database connection.
        step : ProcessingStep
            Step whose logs should be stored.

        Raises
        ------
        ProcessingError
            If storing the logs failed.
        """
        if step.logs is None:
            return

        query = f"""
            INSERT INTO {Tables.STEP_LOG.value}
            (stepId, element, description, type, data)
            VALUES (%s, %s, %s, %s, _binary %s)
        """

        params: list[tuple[int, int, str, str, bytes]] = []
        for log in step.logs:
            value = log["value"]
            match value:
                case int(_):
                    representation = "integer"
                    byte_value = struct.pack("<i", value)
                case float(_):
                    representation = "double"
                    byte_value = struct.pack("<d", value)
                case _:
                    # Maybe this is a numpy array, but they don't support
                    # match-cases yet. So we'll check by hand:
                    if isinstance(value, np.ndarray):
                        byte_value, representation = array_to_bytes(value)
                    else:
                        # We don't know in how to pack unknown values
                        # into bytes, so for now this raises an error
                        raise ProcessingError(
                            "Cannot convert unknown value of type "
                            f"{type(value)} to bytes!"
                        )
            params.append(
                (
                    step.step_id,
                    log["element_index"],
                    log["description"],
                    representation,
                    byte_value,
                )
            )

        cursor.executemany(operation=query, seq_params=params)
        row_id = cursor.lastrowid
        if row_id is None:
            raise ProcessingError("Could not store step logs!")

    def _store_step_results(self, cursor: DatabaseCursor, step: ProcessingStep) -> None:
        query = f"""
            INSERT INTO {Tables.STEP_RESULTS.value}
            (stepId, element, type, data)
            VALUES (%s, %s, %s, _binary %s)
        """
        params: list[tuple[int, int, str, bytes]] = []
        for index, result in enumerate(step.data):
            buffer, result_type = array_to_bytes(result)
            params.append((step.step_id, index, result_type, buffer))

        cursor.executemany(operation=query, seq_params=params)
        row_id = cursor.lastrowid
        if row_id is None:
            raise ProcessingError("Could not store step results!")

    @property
    def steps(self) -> list[ProcessingStep]:
        """List of all processing steps added to this run."""
        return self._steps

    @property
    def labels(self) -> Sequence[str | None] | None:
        """The labels as returned from the last step."""
        return self._labels

    @property
    def info(self) -> _ProcessingRunInfo:
        """Info about this processing run, such as name, description, etc."""
        return self._info

    @property
    def results(self) -> ProcessingStepOutput:
        """The results of this processing run."""
        if not self.steps:
            raise KeyError("Processing run does not contain any steps.")

        # Results of the run are the same as the output of the last step
        return self.steps[-1].data

    def __repr__(self) -> str:
        """Representation of a ProcessingRun."""
        representation = (
            f"ProcessingRun {self.info.name}: "
            f"{self.info.description}, "
            f"last modified on {self.info.lastmodified}."
        )

        if hasattr(self, "_database_info"):
            representation += f"RunID: {self._database_info.run_id}"

        return representation
