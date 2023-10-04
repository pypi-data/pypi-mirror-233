"""ProcessingSteps for normalization.

Classes
-------
NormalizeAmplitude
    Used for normalizing a timeseries' amplitude to a given range.
NormalizeFundamentalFrequency
    Used for normalizing a timeseries' fundamental frequency.
"""

import logging
from collections.abc import Sequence

import numpy as np

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class NormalizeFundamentalFrequency(ProcessingStep):
    """Normalize the fundamental frequency's amplitude to 1.

    This finds the fundamental frequency, calculates it's power
    and normalizes the signal so that the amplitude of the fundamental
    frequency is about 1.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> # Sample signal with 10 periods and an amplitude of 0.1
    >>> signal = 0.1 * np.sin(10 * np.linspace(0, 2*np.pi, 200))
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that normalizes the fundamental frequency",
    ... )
    >>> processing_run.add_step(NormalizeFundamentalFrequency())
    >>> processing_run.run([signal])
    >>> # Amplitude of Signal should be 0.10
    >>> round(max(signal), 1)
    0.1

    >>> # Amplitude after processing should be about 1.0
    >>> round(max(processing_run.results[0]), 1)
    1.0

    The input mapping shows which input got mapped to which output:
    >>> processing_run.steps[0].input_mapping
    {0: 0}
    """

    def __init__(self) -> None:
        super().__init__(locals())

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.PREPROCESSING_NORMALIZE_FUNDAMENTAL_FREQ

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0
        for input_index, item in enumerate(step_input.data):
            try:
                normalized = self._normalize(item)
            except Exception:
                logger.warning("Could not normalize signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(normalized)
                self._input_mapping[input_index] = output_index
                output_index += 1

    def _normalize(self, data: FloatArray) -> FloatArray:
        """Normalize signal using the fundamental frequency.

        Calculates the datas fft, finds the fundamental
        frequency and divides the signal by the power of
        that frequency.
        """
        # Make sure that the mean of the signal is 0:
        zero_mean: FloatArray = data - data.mean()
        # Calculate fft and make it symmetrical
        fft = np.fft.fft(zero_mean)
        fft = np.fft.fftshift(fft)
        # Zero-centered power
        power = np.sqrt(fft * np.conjugate(fft)) * (2.0 / len(zero_mean))
        # Find the amplitue of fundamental frequency
        fundamental_amplitude = max(power)
        # and normalize the signal
        normalized: FloatArray = zero_mean / np.real(fundamental_amplitude)

        return normalized


class NormalizeAmplitude(ProcessingStep):
    """Normalize the signals amplitude.

    This simply takes the min and max of the signal
    and normalizes it to a given range.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> # Sample signal with a minimum of -110 and a maximum of -90.
    >>> signal = 10 * np.sin(10 * np.linspace(0, 2*np.pi, 200)) - 100
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that normalizes a signals amplitude",
    ... )
    >>> processing_run.add_step(NormalizeAmplitude(minimum=-1.0, maximum=1.0))
    >>> processing_run.run([signal])

    Maximum of Signal should be -90 and minimum should be -100
    >>> round(max(signal), 1)
    -90.0

    >>> round(min(signal), 1)
    -110.0

    Maximum after processing should be about 1.0
    >>> round(max(processing_run.results[0]), 1)
    1.0

    while minimum should be -1.0
    >>> round(min(processing_run.results[0]), 1)
    -1.0

    The input mapping shows which input got mapped to which output:
    >>> processing_run.steps[0].input_mapping
    {0: 0}
    """

    _min: float
    _max: float

    def __init__(self, minimum: float = 0.0, maximum: float = 1.0) -> None:
        super().__init__(locals())
        if minimum > maximum:
            raise ProcessingError(
                f"Minimum {minimum} must be smaller than maximum {maximum}"
            )
        self._min = minimum
        self._max = maximum

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.PREPROCESSING_NORMALIZE_AMPLITUDE

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0
        for input_index, item in enumerate(step_input.data):
            try:
                normalized = self._normalize(item)
            except Exception:
                logger.warning("Could not normalize signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(normalized)
                self._input_mapping[input_index] = output_index
                output_index += 1

    def _normalize(self, data: FloatArray) -> FloatArray:
        """Normalize signal using the fundamental frequency.

        Calculates the datas fft, finds the fundamental
        frequency and divides the signal by the power of
        that frequency.
        """
        # Make sure that the mean of the signal is 0:

        current_min: float = min(data)
        current_max: float = max(data)
        previous_amplitude = current_max - current_min

        # Normalize data from 0 to 1
        normalized = (data - current_min) / (previous_amplitude)

        # Normalize from self._min to self._max
        new_amplitude = self._max - self._min
        normalized = normalized * (new_amplitude) + self._min

        return normalized
