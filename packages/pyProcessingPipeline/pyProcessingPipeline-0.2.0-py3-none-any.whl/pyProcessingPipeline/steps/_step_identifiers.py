"""Unique identifiers used for storing and restoring steps in our database."""
from enum import Enum, auto, unique


@unique
class StepIdentifier(Enum):
    """Unique step identifiers,."""

    # Features
    FEATURE_COMPLEX_HARMONICS = auto()
    FEATURE_COMPLEX_HARMONIC_QUOTIENT = auto()

    # Filters
    FILTERS_LOWPASS_BESSEL = auto()
    FILTERS_LOWPASS_BUTTERWORTH = auto()
    FILTERS_LOWPASS_CHEBYSHEV = auto()
    FILTERS_LOWPASS_CHEBYSHEV2 = auto()
    FILTERS_FIR_LOWPASS = auto()

    # Misc
    MISC_CUT = auto()
    MISC_SPLIT = auto()
    MISC_UNITE = auto()
    MISC_AVERAGE_OVER = auto()
    MISC_LABELS_SHUFFLE = auto()

    # Preprocessing
    PREPROCESSING_COHERENT_AVERAGING = auto()
    PREPROCESSING_BASELINE_CORRECTION_FIR = auto()
    PREPROCESSING_NORMALIZE_AMPLITUDE = auto()
    PREPROCESSING_NORMALIZE_FUNDAMENTAL_FREQ = auto()

    # Classification
    CLASSIFIER_KNN = auto()
