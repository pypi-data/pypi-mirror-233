"""Steps that create statistical measures of timeseries.

Classes
-------
Average
    Averages multiple signals and returns the mean and std.
    Should not be used on a timeseries directly, instead use this
    after e.g. feature extraction or
    aligning signals with CoherentAveraging.
"""

import logging
from collections.abc import Sequence

import numpy as np

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput, StepLog
from pyProcessingPipeline.util import batch_generator

logger = logging.getLogger(__name__)


class Average(ProcessingStep):
    """Average multiple signals and return the mean and standard deviation.

    The standard deviation can be found in the step logs.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signal_to_average = [
    ...     [1, 1, 1, 1, 1],
    ...     [1, 2, 3, 4, 5],
    ...     [5, 4, 3, 2, 1],
    ...     [1, 2, 3, 4, 5]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal averager",
    ... )
    ... # Average over 2 arrays
    >>> processing_run.add_step(Average(average_over=2))
    >>> processing_run.run(signal_to_average)
    >>> processing_run.results
    [array([1. , 1.5, 2. , 2.5, 3. ]), array([3., 3., 3., 3., 3.])]

    >>> # Standard deviation is contained in the logs
    >>> for log in processing_run.steps[0].logs:
    ...     print(log)
    {'description': 'Standard deviation', 'element_index': 0, 'value': array([0. , 0.5, 1. , 1.5, 2. ])}
    {'description': 'Standard deviation', 'element_index': 1, 'value': array([2., 1., 0., 1., 2.])}

    The input mapping shows which input got mapped to which outputs:

    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 0, 2: 1, 3: 1}

    """

    _average_over: int

    def __init__(self, average_over: int):
        """Average multiple results and return the mean and std.

        You can choose over how many input arrays the average should
        be created.

        Parameters
        ----------
        average_over : int
            Amount of datasets to average over.
        """
        super().__init__(locals())
        self._average_over = average_over

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_AVERAGE_OVER

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        input_index = 0
        output_index = 0

        for input_batch in batch_generator(
            list_to_batch=step_input.data, batch_size=self._average_over
        ):
            try:
                result = self._average_batch(input_batch)
                mean = result[0]
                std = result[1]
            except Exception:
                logger.info("Could not average item batch", exc_info=True)
                for _ in range(len(input_batch)):
                    self._input_mapping[input_index] = None
                    input_index += 1
            else:
                self._data.append(mean)
                self._logs.append(
                    StepLog(
                        description="Standard deviation",
                        element_index=output_index,
                        value=std,
                    )
                )
                for _ in range(len(input_batch)):
                    self._input_mapping[input_index] = output_index
                    input_index += 1
                output_index += 1

    def _average_batch(
        self, input_batch: list[FloatArray]
    ) -> tuple[FloatArray, FloatArray]:
        """Average a batch of arrays (or coefficients) and return the mean and std.

        Parameters
        ----------
        input_batch : list[FloatArray]
            Batch over which to average the values.

        Returns
        -------
        tuple[FloatArray, FloatArray]
            Returns the mean and std
        """
        mean = np.mean(input_batch, axis=0)
        std = np.std(input_batch, axis=0)
        return mean, std
