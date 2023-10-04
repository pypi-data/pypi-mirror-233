"""Contains the base class used for every processing step."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, final

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.types import (
    LabelMapping,
    Model,
    ProcessingStepInput,
    ProcessingStepOutput,
    StepLog,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ._step_identifiers import StepIdentifier


class UnpersistedStepError(ProcessingError, LookupError):
    """Raised if access to a step's database id is tried on an unpersisted Step."""


class ProcessingStep(ProcessingStepInput, ABC):
    """ProcessingStep base class.

    To implement a processing step, overwrite this
    classes run method.

    To persist a step's parameters, use the
    to_args function.
    """

    _init_parameters: dict[str, Any]

    _data: ProcessingStepOutput

    _input_mapping: LabelMapping
    _logs: list[StepLog]
    _model: Model | None = None

    _step_id: int | None = None
    _run_id: int | None = None

    def __init__(self, init_params: dict[str, Any]):
        self._data = []
        self._input_mapping = {}
        self._logs = []
        # Stores the parameters used for initialization in the
        # _init_parameters dictionary.
        # This is used for persistent storage.
        parameters = {
            key: value
            for key, value in init_params.items()
            if key not in ["self", "args", "kwargs", "__class__"]
        }
        try:
            self._init_parameters = self.__bases__[0]._init_parameters.copy()  # type: ignore
            self._init_parameters.update(parameters)
        except AttributeError:
            self._init_parameters = parameters

    @final
    def _init_results(self) -> None:
        """Initialize the _data, _logs and _input_mapping to empty values.

        Should be called before doing anything in self.run(), so
        that consecutive runs will not keep appending data to
        a previous run's data.
        """
        self._data = []
        self._logs = []
        self._input_mapping = {}

    @final
    @property
    def parameters(self) -> dict[str, Any]:
        """Parameters used to construct this step instance.

        This returns a dictionary, which can be json-dumped
        and stored in a text field in our database for
        persisting the step arguments.
        When reading from our database, the step can be
        recreated with all its arguments by just
        unpacking the retrieved dictionary:
        ::

            # Create a processing step
            step = ProcessingStep(some="Parameters", are="set", already=123)
            # and store it to our database:
            database_entry = json.dumps(step.parameters())

            # To recreate the same step, run:
            step = ProcessingStep(**json.loads(database_entry))

        Returns
        -------
        dict[str, Any]
            Dictionary containing all arguments that were used
            to create this instance of a processing step.
            E.g. for the parameters above, this would return:
            ::

                {
                    "some": "Parameters",
                    "are": "set",
                    "already": 123
                }
        """
        return self._init_parameters

    @final
    @property
    def data(self) -> ProcessingStepOutput:
        if self._data is None:
            raise RuntimeError("Step has not been run yet, cannot access data!")
        return self._data

    @final
    @property
    def input_mapping(self) -> LabelMapping:
        """Containts which element from the input is mapped to which index in the output.

        A single input can be mapped to multiple output values, a single value
        or no value at all.
        """
        return self._input_mapping

    @final
    @property
    def logs(self) -> list[StepLog] | None:
        """Access the step logs.

        Logs contain metadata for a step.
        Each entry in logs corresponds to one entry in
        the results list with the same index.
        """
        return self._logs

    @final
    @property
    def model(self) -> Model | None:
        """Access the step's Model, if any.

        The model that was trained in this processing step,
        if a model was trained.
        """
        return self._model

    @final
    @property
    def step_id(self) -> int:
        """Access the step's primary key.

        The primary key of the processing step, as stored
        in our database. Only available if the step has been stored.
        Otherwise, access will raise an error.
        """
        if self._step_id is None:
            raise UnpersistedStepError(
                f"Cannot access StepID of {self}! Step has not been persisted yet.",
            )
        return self._step_id

    @final
    @property
    def run_id(self) -> int:
        """Access the step's run id.

        The primary key of the processing run this step belongs to,
        as stored in our database. Only available if the step has been stored.
        Otherwise, access will raise an error.
        """
        if self._run_id is None:
            raise UnpersistedStepError(
                f"Cannot access RunID of {self}! Step has not been persisted yet.",
            )
        return self._run_id

    @final
    def _update_database_ids(self, new_step_id: int, new_run_id: int) -> None:
        """Set the step_id and run_id of this step.

        These are the primary keys used in our database.
        The ids should only be updated when this step
        has been saved in our database.

        Parameters
        ----------
        new_step_id : int
            The newly assigned step_id from our database.
        new_run_id : int
            The run_id of the parent run from our database.
        """
        self._step_id = new_step_id
        self._run_id = new_run_id

    @abstractmethod
    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        """Run the processing step.

        Results are stored in the results-parameter of this
        ProcessingStep.

        Parameters
        ----------
        step_input : ProcessingStepInput
            The input on which this processing step should act.
            This might be the output of a previous step
            or from an imported timeseries.
        labels : Sequence[str | None] | None
            Labels for the data in the given step input.
            If given, it has the same length as the step_input sequence.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def identifier() -> StepIdentifier:
        """Get the StepIdentifier.

        Used for reconstructing the step from the database.

        Returns
        -------
        StepIdentifier
            Identifier which uniquely identifies this step class.
        """

    def _set_run_id(self, run_id: int) -> None:
        self._run_id = run_id

    def _set_step_id(self, step_id: int) -> None:
        self._step_id = step_id

    def _set_data(self, data: ProcessingStepOutput) -> None:
        self._data = data

    def _set_logs(self, logs: list[StepLog]) -> None:
        self._logs = logs
