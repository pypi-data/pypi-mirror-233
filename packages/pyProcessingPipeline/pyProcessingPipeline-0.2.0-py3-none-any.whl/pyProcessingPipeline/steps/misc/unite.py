"""Steps for combining multiple timeseries.

Classes
-------
Unite
    Used to combine adjacent timeseries by "uniting" them,
    appending a given number of timeseries into a single longer one.
"""

import logging
from collections.abc import Sequence

import numpy as np

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import ProcessingStepInput
from pyProcessingPipeline.util import batch_generator

logger = logging.getLogger(__name__)


class Unite(ProcessingStep):
    """Append multiple timeseries to each other.

    This step combines n adjacent datasets in the input
    into a single output dataset.
    To combine every two records for example,
    create a processing run

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that combines multiple signals",
    ... )

    And add the Unite-step with a n_unite of 2

    >>> processing_run.add_step(Unite(n_unite=2))

    You can then run this processing run on any input:

    >>> signals_to_combine = [
    ...     [1],
    ...     [2],
    ...     [3, 3],
    ...     [4, 4],
    ...     [5, 5, 5],
    ...     [6]
    ... ]
    >>> processing_run.run(signals_to_combine)

    The results will have combined every 2 arrays into a single one:

    >>> processing_run.results
    [array([1, 2]), array([3, 3, 4, 4]), array([5, 5, 5, 6])]

    The input mapping shows you which input
    got reduced to which output:

    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}


    Running the function on inputs which are not cleanly
    divisible by the given unite-number results in the
    extra inputs to be dropped:

    >>> signals_to_combine = [
    ...     [1],
    ...     [2],
    ...     [3, 3],
    ...     [4, 4],
    ...     [5, 5, 5]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that combines multiple signals",
    ... )
    ... # Combine every 3 signals, which drops the last two entries
    >>> processing_run.add_step(Unite(n_unite=3))
    >>> processing_run.run(signals_to_combine)
    >>> processing_run.results
    [array([1, 2, 3, 3])]

    If the input does not contain enough data for any combination,
    the output will be empty:

    >>> signals_to_combine = [
    ...     [1],
    ...     [2]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that combines multiple signals",
    ... )
    ... # Combine every 3 signals, which drops everything
    >>> processing_run.add_step(Unite(n_unite=3))
    >>> processing_run.run(signals_to_combine)
    >>> processing_run.results
    []
    """

    _n_unite: int

    def __init__(self, n_unite: int):
        """Combine multiple timeseries by appending them to eachother.

        Parameters
        ----------
        n_unite : int
            Amount of timeseries/datasets to combine into a single one.
        """
        super().__init__(locals())

        self._n_unite = n_unite

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_UNITE

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        # Warn the user if the input is not cleanly divisible by n
        if len(step_input.data) % self._n_unite != 0:
            logger.warning(
                "Input %s is not cleanly divisible by %s. Dropping extra entries.",
                str(len(step_input.data)),
                str(self._n_unite),
            )
            input_length = len(step_input.data) // self._n_unite * self._n_unite
        else:
            input_length = len(step_input.data)

        self._init_results()
        output_index = 0

        for input_index, item_batch in enumerate(
            batch_generator(step_input.data[:input_length], self._n_unite)
        ):
            batch_length = len(item_batch)
            start_index = batch_length * input_index
            try:
                result = np.concatenate(item_batch)
            except Exception:
                logger.info(
                    "Could not unite input array %d", input_index, exc_info=True
                )
                for i in range(batch_length):
                    self._input_mapping[start_index + i] = None
            else:
                for i in range(batch_length):
                    self._input_mapping[start_index + i] = output_index

                self._data.append(result)
                output_index += 1
