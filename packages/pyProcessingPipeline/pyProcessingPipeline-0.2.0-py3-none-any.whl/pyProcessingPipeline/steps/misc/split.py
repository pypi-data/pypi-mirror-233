"""Steps for splitting timeseries.

Classes
-------
Split
    Used for splitting a timeseries into multiple
    sub-series with the same length.
"""

import logging
from collections.abc import Sequence

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class Split(ProcessingStep):
    """Split a timeseries into equal sub-series.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_split = [
    ...     [1, 2, 3, 4, 5, 6],
    ...     [6, 5, 4, 3, 2, 1],
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2))
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2, 3]), array([4, 5, 6]), array([6, 5, 4]), array([3, 2, 1])]

    If the input signals can not be evenly divided into
    n splits, the unsplittable arrays are dropped.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_split = [
    ...     [1, 2, 3, 4, 5],
    ...     [5, 4, 3, 2, 1],
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2))
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2]), array([3, 4]), array([5, 4]), array([3, 2])]

    Here, the output is missing '5' from the first array,
    and '1' from the second.

    The input mapping shows which input got mapped to which outputs:

    >>> processing_run.steps[0].input_mapping
    {0: [0, 1], 1: [2, 3]}
    """

    _num_sub_series: int

    def __init__(self, number_of_sub_series: int):
        """Split a timeseries into n equal subseries.

        Parameters
        ----------
        number_of_sub_series : int
            Amount of sub-series to create from the input.
        """
        super().__init__(locals())

        self._num_sub_series = number_of_sub_series

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_SPLIT

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                results = self._split(item)
            except Exception:
                logger.info(
                    "Could not split input array %d", input_index, exc_info=True
                )
                self._input_mapping[input_index] = None
            else:
                output_indices: list[int] = []
                for result in results:
                    self._data.append(result)
                    output_indices.append(output_index)
                    output_index += 1
                self._input_mapping[input_index] = output_indices

    def _split(self, data: FloatArray) -> list[FloatArray]:
        """Split the given array into equal sub-arrays.

        Return a list of sub arrays.

        Parameters
        ----------
        data : FloatArray
            The array to split.

        Returns
        -------
        list[FloatArray]
            The split arrays.
        """
        length_of_split = len(data) // self._num_sub_series
        logger.info("Using split length of %s", length_of_split)
        results: list[FloatArray] = []
        for i in range(self._num_sub_series):
            left_index = i * length_of_split
            right_index = left_index + length_of_split
            results.append(data[left_index:right_index])
        return results
