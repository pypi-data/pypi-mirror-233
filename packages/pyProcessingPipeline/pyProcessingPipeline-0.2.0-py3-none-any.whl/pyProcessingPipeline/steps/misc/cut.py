"""Steps for cutting timeseries.

Classes
-------
Cut
    Cut can be used to cut a signals length down
    by removing a specific amount of samples from
    the beginning and end.
    Can be used to equalize different timeseries.
"""

import logging
from collections.abc import Sequence

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class NoBoundsError(ProcessingError):
    """Raised if no suitable bounds are given."""


class Cut(ProcessingStep):
    """Cut a signal and return the signal between lower and upper bound.

    This makes all signals the same length, unless the upper bound
    is set to None. In this case, the signals will stay different lengths.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_cut = [
    ...     [1, 1, 1, 1, 1],
    ...     [1, 2, 3, 4, 5],
    ...     [5, 4, 3, 2, 1],
    ...     [1, 2, 3, 4, 5]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal cutter",
    ... )
    ... # Remove first and last entry for every signal
    >>> processing_run.add_step(Cut(global_lower_bound=1, global_upper_bound=4))
    >>> processing_run.run(signals_to_cut)
    >>> processing_run.results
    [array([1, 1, 1]), array([2, 3, 4]), array([4, 3, 2]), array([2, 3, 4])]

    The lower bound will default to 0 if not set:

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_cut = [[1, 2, 3, 4, 5]]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal cutter",
    ... )
    ... # Lower bound defaults to 0
    >>> processing_run.add_step(Cut(global_lower_bound=None, global_upper_bound=3))
    >>> processing_run.run(signals_to_cut)
    >>> processing_run.results
    [array([1, 2, 3])]

    While the upper bound will default to whatever length the original
    signal has. This means that signals with differing lengths will
    still be different lengths if global_upper_bound is set to None.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_cut = [
    ...     [1, 2],
    ...     [1, 2, 3],
    ...     [1, 2, 3, 4]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal cutter",
    ... )
    ... # Not setting an upper bound keeps arrays of different lengths
    >>> processing_run.add_step(Cut(global_lower_bound=1, global_upper_bound=None))
    >>> processing_run.run(signals_to_cut)
    >>> processing_run.results
    [array([2]), array([2, 3]), array([2, 3, 4])]

    If some signals are shorter than the upper bound,
    signals of differing lengths will also be produced.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_cut = [
    ...     [1],
    ...     [1, 2],
    ...     [1, 2, 3],
    ...     [1, 2, 3, 4]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal cutter",
    ... )
    ... # Remove first and last entry for every signal
    >>> processing_run.add_step(Cut(global_lower_bound=None, global_upper_bound=2))
    >>> processing_run.run(signals_to_cut)
    >>> processing_run.results
    [array([1]), array([1, 2]), array([1, 2]), array([1, 2])]

    The input mapping shows which input got mapped to which output:

    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 1, 2: 2, 3: 3}
    """

    _lower_bound: int
    _upper_bound: int | None

    def __init__(
        self,
        global_lower_bound: int | None,
        global_upper_bound: int | None,
    ):
        super().__init__(locals())

        # Set default value for lower bound (0) if its not given:
        if global_lower_bound is None or global_lower_bound < 0:
            logger.warning("Lower bound '%s' replaced with 0.", global_lower_bound)
            global_lower_bound = 0

        # Check bounds
        if global_upper_bound is not None:
            if global_upper_bound < global_lower_bound:
                raise NoBoundsError(
                    "Lower bound must be lower than upper bound!",
                    global_lower_bound,
                    global_upper_bound,
                )

        self._lower_bound = global_lower_bound
        self._upper_bound = global_upper_bound

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_CUT

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        # Warn the user that signals shorter than the upper bound
        # will have a different length than signals longer than
        # the upper bound.
        if self._upper_bound is not None and not all(
            len(signal) >= self._upper_bound for signal in step_input.data
        ):
            logger.warning(
                "Some signals are shorter than the upper bound. "
                + "This will result in signals of differing lengths."
            )

        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result: FloatArray = self._cut(
                    item, self._lower_bound, self._upper_bound
                )
            except Exception:
                logger.info("Could not cut signal %d", input_index, exc_info=True)
                self._input_mapping[input_index] = None
            else:
                self._input_mapping[input_index] = output_index
                self._data.append(result)
                output_index += 1

    def _cut(
        self,
        signal: FloatArray,
        lower_bound: int,
        upper_bound: int | None,
    ) -> FloatArray:
        """Cuts a signal and returns the signal between lower and upper bound.

        Optional bounds will be ignored.

        Parameters
        ----------
        signal : FloatArray
            The signal to which should be cut.
        lower_bound : Optional[int]
            The lower bound. Everything in the signal before this
            index will be removed.
        upper_bound : Optional[int]
            The upper bound. Everything after this index will be removed.
            If no index is given, the length of the signal is used instead.

        Returns
        -------
        FloatArray
            The signal, cut between the given bounds.
        """
        if upper_bound is None or upper_bound > len(signal):
            return signal[lower_bound:]

        return signal[lower_bound:upper_bound]
