"""Steps for modifying labels.

Can be used to shuffle the labels and validate
that classifiers actually found information in our labels.

Classes
-------
Shuffle
    Used for randomly shuffling labels.
"""

import logging
import random
from collections.abc import Sequence

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import ProcessingStepInput

logger = logging.getLogger(__name__)


class Shuffle(ProcessingStep):
    """Shuffles a timeseries' labels.

    Does not modify anything else.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals = [
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [3, 2, 1]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses shuffles our labels.",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Shuffle(seed=0))

    Now add some labels to our data for shuffling.
    >>> from pyProcessingPipeline.types import LabeledProcessingStepInput
    >>> processing_run.run(LabeledProcessingStepInput(
    ...     signals,
    ...     ["Label1", "Label2", "Label3"]
    ...     )
    ... )
    >>> processing_run.run(signals)
    >>> processing_run.results
    [array([1, 2, 3]), array([4, 5, 6]), array([3, 2, 1])]

    The results are the same as the input, but the labels are shuffled.
    >>> processing_run.steps[0].input_mapping
    {0: 0, 1: 2, 2: 1}
    """

    _seed: int

    def __init__(self, seed: int) -> None:
        """Randomly shuffle labels.

        Parameters
        ----------
        seed : int
            Seed for the random shuffling.
            Must be set for reproduceability.
        """
        super().__init__(locals())
        self._seed = seed

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_LABELS_SHUFFLE

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        self._data = step_input.data
        shuffled_indices = list(range(len(self._data)))
        # Set seed and shuffle list
        random.seed(self._seed)
        random.shuffle(shuffled_indices)
        self._input_mapping = {
            input_index: output_index
            for input_index, output_index in zip(
                range(len(self._data)), shuffled_indices, strict=True
            )
        }
