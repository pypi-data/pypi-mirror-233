"""Finite-Impulse-Response filters for use with the processing pipeline."""

import logging
from collections.abc import Sequence

from scipy.signal import filtfilt, firwin, kaiserord

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class LowpassFIR(ProcessingStep):
    """Lowpass filter with a finite impulse response using the Kaiser window.

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
    ...     LowpassFIR(
    ...         sampling_frequency=1000/20,
    ...         cutoff_frequency=1.5,
    ...         attenuation=60,
    ...         transition_width=1
    ...     )
    ... )
    >>> processing_run.run([signal])

    The lowpass-filtered signal is now available in the results:

    >>> result = processing_run.results[0]

    and its average distance to a pure sinewave is a lot closer now:

    >>> round(np.mean(abs(result - np.sin(x))), 2)
    0.0

    """

    _sampling_frequency: float
    _cutoff_frequency: float
    _attenuation: float
    _transition_width: float
    _kaiser_window: FloatArray

    def __init__(
        self,
        sampling_frequency: float,
        cutoff_frequency: float,
        attenuation: float,
        transition_width: float,
    ):
        """Create a LowpassFIR step.

        Parameters
        ----------
        sampling_frequency : float
            Sampling frequency of the signal this filter should filter, in Hz.
        cutoff_frequency : float
            Cutoff frequency of the lowpass filter, in Hz.
        attenuation : float
            Signal attenuation in the stop band, in dB.
        transition_width : float
            Width of the transition from pass- to stopband, in Hz.
        """
        super().__init__(locals())

        self._sampling_frequency = sampling_frequency
        self._cutoff_frequency = cutoff_frequency
        self._attenuation = attenuation
        self._transition_width = transition_width

        kaiser_taps, kaiser_beta = kaiserord(
            ripple=self._attenuation,
            width=2 * self._transition_width / self._sampling_frequency,
        )

        self._kaiser_window = firwin(
            numtaps=kaiser_taps,
            cutoff=self._cutoff_frequency,
            fs=self._sampling_frequency,
            window=("kaiser", kaiser_beta),
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.FILTERS_FIR_LOWPASS

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result = filtfilt(b=self._kaiser_window, a=1.0, x=item)
            except Exception as error:
                print("Could not filter signal", input_index, error)
                self._input_mapping[input_index] = None
            else:
                self._data.append(result)
                self._input_mapping[input_index] = output_index
                output_index += 1
