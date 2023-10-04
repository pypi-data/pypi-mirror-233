"""Contains butterworth filters for use in the processing pipeline."""

import logging
from collections.abc import Sequence

from scipy.signal import butter, sosfiltfilt

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class LowpassButter(ProcessingStep):
    """Simple lowpass filter step based on a butterworth filter.

    Example
    -------

    To filter out higher frequencies, we'll use a sample signal
    consisting of two superpositioned sinewaves:

    >>> import numpy as np
    >>> x = np.linspace(0, 20 * 2*np.pi, 1000)
    >>> signal = np.sin(x)
    >>> signal += np.sin(3*x)

    The average difference from a pure (single-frequency)
    sine is currently:

    >>> round(np.mean(abs(signal - np.sin(x))), 2)
    0.64

    To lowpass-filter this signal, create a processing run

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that lowpass filters a signal",
    ... )

    And add the filter step:

    >>> processing_run.add_step(
    ...     LowpassButter(
    ...         cutoff_frequency=1.5,
    ...         filter_order=3,
    ...         sampling_frequency=1000/20,
    ...     )
    ... )
    >>> processing_run.run([signal])

    The lowpass-filtered signal is now available in the results:

    >>> result = processing_run.results[0]

    and its average distance to a pure sinewave is a lot closer now:

    >>> round(np.mean(abs(result - np.sin(x))), 2)
    0.05
    """

    _cutoff_frequency: float
    _order: float
    _sampling_frequency: float
    _butter_coeffs: FloatArray

    def __init__(
        self,
        cutoff_frequency: float,
        filter_order: int,
        sampling_frequency: float,
    ):
        super().__init__(locals())
        self._cutoff_frequency = cutoff_frequency
        self._order = filter_order
        self._sampling_frequency = sampling_frequency
        self._butter_coeffs = butter(
            N=self._order,
            Wn=self._cutoff_frequency,
            btype="lowpass",
            output="sos",  # Second order sections, used in sosfiltfilt
            fs=self._sampling_frequency,
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.FILTERS_LOWPASS_BUTTERWORTH

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result: FloatArray = sosfiltfilt(sos=self._butter_coeffs, x=item)
            except Exception:
                logger.info("Could not filter signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(result)
                self._input_mapping[input_index] = output_index
                output_index += 1


class HighpassButter(ProcessingStep):
    """Simple highpass filter step based on a butterworth filter.

    Example
    -------

    To filter out lower frequencies, we'll use a sample signal
    consisting of two superpositioned sinewaves:

    >>> import numpy as np
    >>> x = np.linspace(0, 20 * 2*np.pi, 1000)
    >>> signal = np.sin(x)
    >>> signal += np.sin(3*x)

    The average difference from a pure (single-frequency)
    sine is currently:

    >>> round(np.mean(abs(signal - np.sin(3*x))), 2)
    0.64

    To highpass-filter this signal, create a processing run

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that highpass filters a signal",
    ... )

    And add the filter step:

    >>> processing_run.add_step(
    ...     HighpassButter(
    ...         cutoff_frequency=1.5,
    ...         filter_order=3,
    ...         sampling_frequency=1000/20,
    ...     )
    ... )
    >>> processing_run.run([signal])

    The highpass-filtered signal is now available in the results:

    >>> result = processing_run.results[0]

    and its average distance to a pure sinewave is a lot closer now:

    >>> round(np.mean(abs(result - np.sin(3*x))), 2)
    0.05
    """

    _cutoff_frequency: float
    _order: float
    _sampling_frequency: float
    _butter_coeffs: FloatArray

    def __init__(
        self,
        cutoff_frequency: float,
        filter_order: int,
        sampling_frequency: float,
    ):
        super().__init__(locals())
        self._cutoff_frequency = cutoff_frequency
        self._order = filter_order
        self._sampling_frequency = sampling_frequency
        self._butter_coeffs = butter(
            N=self._order,
            Wn=self._cutoff_frequency,
            btype="highpass",
            output="sos",  # Second order sections, used in sosfiltfilt
            fs=self._sampling_frequency,
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.FILTERS_LOWPASS_BUTTERWORTH

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result: FloatArray = sosfiltfilt(sos=self._butter_coeffs, x=item)
            except Exception:
                logger.info("Could not filter signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(result)
                self._input_mapping[input_index] = output_index
                output_index += 1
