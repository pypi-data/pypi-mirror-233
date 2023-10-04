"""ProcessingSteps for averaging inputs.

Classes
-------
CoherentAveraging
    A method for coherent averaging of signals,
    which makes it possible to estimate statistical properties
    of periodic signals. Creates an average representation
    of a single period from a signal containing multiple periods.
"""

import itertools
import logging
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
import scipy.signal

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput, StepLog

logger = logging.getLogger(__name__)


class NonPeriodicSignalError(ProcessingError):
    """Raised if a signals periodicity could not be determined."""

    def __init__(self) -> None:
        super().__init__("No periodicity in signal could be determined.")


class NoPeriodsFoundError(ProcessingError):
    """Raised if no periods could be found in a given signal."""

    def __init__(self) -> None:
        super().__init__("Could not determine the locations of any periods in signal!")


class CoherentAveraging(ProcessingStep):
    """Coherently average multiple signal periods.

    Averages each period of a periodic signal.
    This creates an average representation of a single
    period and its deviation per signal.
    Can be used for e.g. inter-patient analysis.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> # Sample signal with 10 periods
    >>> signal = np.sin(10 * np.linspace(0, 2*np.pi, 200))
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that averages multiple periods",
    ... )
    >>> processing_run.add_step(CoherentAveraging())
    >>> processing_run.run([signal])
    >>> # The result should now contain a single period,
    >>> # starting at it's lowest point (shifted by 3/2 pi)
    >>> single_period = np.sin(3/2 * np.pi + 10 * np.linspace(0, 2*np.pi / 10, 20))
    >>> # Mean difference between both signals should be small
    >>> np.mean(abs(processing_run.results[0] - single_period)) < 0.1
    True

    >>> # The standard deviation, contained in the step's logs,
    >>> #should also be small
    >>> np.mean(processing_run.steps[0].logs[0]["value"]) < 0.1
    True

    The input mapping shows which input got mapped to which output:

    >>> processing_run.steps[0].input_mapping
    {0: 0}
    """

    def __init__(self) -> None:
        super().__init__(locals())

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.PREPROCESSING_COHERENT_AVERAGING

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                result = self._coherent_averaging(item)
                average = result[0]
                standard_deviation = result[1]
            except Exception:
                logger.info("Could not determine average for signal %d", input_index)
                self._input_mapping[input_index] = None
            else:
                self._data.append(average)
                self._logs.append(
                    StepLog(
                        description="Standard deviation of averaged signal.",
                        element_index=output_index,
                        value=standard_deviation,
                    )
                )
                self._input_mapping[input_index] = output_index
                output_index += 1

    def _coherent_averaging(self, signal: FloatArray) -> tuple[FloatArray, FloatArray]:
        """Average periods of a periodic signal and return the average period and deviation.

        This function finds single oscillations in a periodic signal
        and averages each found oscillation.

        The returned signal resembles an average oscillation found
        in the given signal, including the standard deviation
        from that average signal present in the input.

        Parameters
        ----------
        signal : FloatArray
            The periodic signal for which to find the average
            oscillation.

        Returns
        -------
        average_signal: FloatArray
            The mean signal, averaged over every found oscillation.
        signal_deviation: FloatArray
            The standard deviation of the average signal.
        """
        # Check if signal is periodic. If it isn't, this function does
        # not make any sense :)
        if not self._signal_is_periodic(signal):
            raise NonPeriodicSignalError

        # Estimate peak find parameters:
        peaks = self._find_peaks(signal)

        # We need atleast two peaks to determine a single period
        # ( left and right edge)
        minimum_required_peaks = 2
        if len(peaks) < minimum_required_peaks:
            raise NoPeriodsFoundError

        # ------------- Start coherent averaging ---------------
        # Find out how much elements we need to store
        max_period_size = np.diff(peaks).max()
        mean_start_and_end_value = signal[peaks].mean()
        num_periods = len(peaks) - 1
        logger.info(
            "Using maximum period size %d, max size %d and %d periods.",
            max_period_size,
            max_period_size,
            num_periods,
        )

        # Create array that will store every period and initialize it
        # with the mean of the received signal.
        periods = (
            np.ones(shape=(num_periods, max_period_size)) * mean_start_and_end_value
        )

        # Put all periods into the periods array
        period_index = 0
        for start_peak, end_peak in itertools.pairwise(peaks):
            current_period = signal[start_peak:end_peak]
            periods[period_index, : len(current_period)] = current_period
            period_index += 1

        # Create average and standard deviation signal
        average_signal = periods.mean(axis=0)
        signal_deviation = periods.std(axis=0)

        return average_signal, signal_deviation

    def _find_peaks(self, signal: FloatArray) -> npt.NDArray[np.int64]:
        """Find periods in signal and return index of each period start.

        This function tries to estimate the peak find parameters
        and returns the starting indices of every period found.

        Parameters
        ----------
        signal : FloatArray
            Array containing a periodic signal.

        Returns
        -------
        npt.NDArray[np.int64]
            Array containing the indices of each period found in
            signal.
        """
        # Remove signal baseline, which is annoying when estimating the
        # peak find parameters
        signal_without_baseline = scipy.signal.detrend(signal)

        # Using the standard deviation as required signal prominence,
        # until I find a better estimate.
        estimated_prominence = signal_without_baseline.std()
        logger.info("Estimated peak prominence as %s", estimated_prominence)

        # Using half of the main period as a minimum distance,
        # which might fail if there is a lot of variation in the
        # periodicity, like e.g. in an ECG under stress.
        highest_fft_peak_index = np.argmax(
            np.abs(np.fft.fft(signal_without_baseline))[: len(signal) // 2]
        )
        estimated_peak_distance = len(signal_without_baseline) / highest_fft_peak_index
        logger.info("Estimated peak to peak distance as %s", estimated_peak_distance)

        # Find peaks (actually find troths, since otherwise we would have to
        # shift the resulting signal to make it look good...)
        peaks: npt.NDArray[np.int64] = scipy.signal.find_peaks(
            x=-signal_without_baseline,
            prominence=estimated_prominence,
            distance=estimated_peak_distance / 2,
        )[0]
        logger.info("Found %d peaks.", len(peaks))
        return peaks

    def _signal_is_periodic(self, _signal: FloatArray) -> bool:
        logger.warning("Determining signal periodicity is not implemented yet!")
        return True
