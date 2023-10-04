"""Contains Chebyshev filters for use in the processing pipeline."""

import logging
from collections.abc import Sequence

from scipy.signal import cheby1, cheby2, sosfiltfilt

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class LowpassCheby1(ProcessingStep):
    """Simple lowpass filter step based on a Chebyshev type1 filter.

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
    ...     LowpassCheby1(
    ...         cutoff_frequency=1.5,
    ...         filter_order=3,
    ...         sampling_frequency=1000/20,
    ...         maximum_ripple=1
    ...     )
    ... )
    >>> processing_run.run([signal])

    The lowpass-filtered signal is now available in the results:

    >>> result = processing_run.results[0]

    and its average distance to a pure sinewave is a lot closer now:

    >>> round(np.mean(abs(result - np.sin(x))), 2)
    0.09
    """

    _cutoff_frequency: float
    _order: float
    _sampling_frequency: float
    _maximum_ripple: float
    _cheby1_coeffs: FloatArray

    def __init__(
        self,
        cutoff_frequency: float,
        filter_order: int,
        sampling_frequency: float,
        maximum_ripple: float,
    ):
        super().__init__(locals())
        self._cutoff_frequency = cutoff_frequency
        self._order = filter_order
        self._sampling_frequency = sampling_frequency
        self._maximum_ripple = maximum_ripple
        self._cheby1_coeffs = cheby1(
            N=self._order,
            rp=self._maximum_ripple,
            Wn=self._cutoff_frequency,
            btype="lowpass",
            output="sos",  # Second order sections, used in sosfiltfilt
            fs=self._sampling_frequency,
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result: FloatArray = sosfiltfilt(sos=self._cheby1_coeffs, x=item)
            except Exception:
                logger.info("Could not filter signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._input_mapping[input_index] = output_index
                self._data.append(result)
                output_index += 1


class LowpassCheby2(ProcessingStep):
    """Simple lowpass filter step based on a Chebyshev type2 filter.

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
    ...     LowpassCheby2(
    ...         cutoff_frequency=1.5,
    ...         filter_order=3,
    ...         sampling_frequency=1000/20,
    ...         minimum_attenuation=10
    ...     )
    ... )
    >>> processing_run.run([signal])

    The lowpass-filtered signal is now available in the results:
    >>> result = processing_run.results[0]

    and its average distance to a pure sinewave is a lot closer now:
    >>> round(np.mean(abs(result - np.sin(x))), 2)
    0.08
    """

    _cutoff_frequency: float
    _order: float
    _sampling_frequency: float
    _minimum_attenuation: float
    _cheby2_coeffs: FloatArray

    def __init__(
        self,
        cutoff_frequency: float,
        filter_order: int,
        sampling_frequency: float,
        minimum_attenuation: float,
    ):
        super().__init__(locals())
        self._cutoff_frequency = cutoff_frequency
        self._order = filter_order
        self._sampling_frequency = sampling_frequency
        self._minimum_attenuation = minimum_attenuation
        self._cheby2_coeffs = cheby2(
            N=self._order,
            rs=self._minimum_attenuation,
            Wn=self._cutoff_frequency,
            btype="lowpass",
            output="sos",  # Second order sections, used in sosfiltfilt
            fs=self._sampling_frequency,
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV2

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result: FloatArray = sosfiltfilt(sos=self._cheby2_coeffs, x=item)
            except Exception:
                logger.info("Could not filter signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._input_mapping[input_index] = output_index
                self._data.append(result)
                output_index += 1
