"""Unique ProcessingStep identifier.

Defines the names under which
every processing step is stored in the database.

This allows us to recreate previously stored runs
by knowing which step name corresponds to which
Python step class.

The lookup is defined statically so that type checkers
can know at compile time what steps exist.

The names are defined in their own file so that we do
not create a circular dependency between lookup
and processing step.
"""

from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.steps.classification.knn import KNearestNeighbor
from pyProcessingPipeline.steps.feature_extraction.spectrum import (
    ComplexHarmonicQuotient,
    ComplexHarmonics,
)
from pyProcessingPipeline.steps.filters.bessel import LowpassBessel
from pyProcessingPipeline.steps.filters.butterworth import LowpassButter
from pyProcessingPipeline.steps.filters.chebyshev import LowpassCheby1, LowpassCheby2
from pyProcessingPipeline.steps.filters.fir import LowpassFIR
from pyProcessingPipeline.steps.misc.cut import Cut
from pyProcessingPipeline.steps.misc.split import Split
from pyProcessingPipeline.steps.misc.statistics import Average
from pyProcessingPipeline.steps.misc.unite import Unite
from pyProcessingPipeline.steps.preprocessing.averaging import CoherentAveraging
from pyProcessingPipeline.steps.preprocessing.baseline_correction import (
    FIRBaselineCorrection,
)
from pyProcessingPipeline.steps.preprocessing.normalization import (
    NormalizeAmplitude,
    NormalizeFundamentalFrequency,
)

# mypy: disable-error-code="dict-item"

#: Contains the Lookup from StepIdentifier to the actual ProcessingStep.
StepLookup: dict[str, type[ProcessingStep]] = {
    # Features
    StepIdentifier.FEATURE_COMPLEX_HARMONICS.name: ComplexHarmonics,
    StepIdentifier.FEATURE_COMPLEX_HARMONIC_QUOTIENT.name: ComplexHarmonicQuotient,
    # Filters
    StepIdentifier.FILTERS_LOWPASS_BESSEL.name: LowpassBessel,
    StepIdentifier.FILTERS_LOWPASS_BUTTERWORTH.name: LowpassButter,
    StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV.name: LowpassCheby1,
    StepIdentifier.FILTERS_LOWPASS_CHEBYSHEV2.name: LowpassCheby2,
    StepIdentifier.FILTERS_FIR_LOWPASS.name: LowpassFIR,
    # Misc
    StepIdentifier.MISC_CUT.name: Cut,
    StepIdentifier.MISC_SPLIT.name: Split,
    StepIdentifier.MISC_UNITE.name: Unite,
    StepIdentifier.MISC_AVERAGE_OVER.name: Average,
    # Preprocessing
    StepIdentifier.PREPROCESSING_COHERENT_AVERAGING.name: CoherentAveraging,
    StepIdentifier.PREPROCESSING_BASELINE_CORRECTION_FIR.name: FIRBaselineCorrection,
    StepIdentifier.PREPROCESSING_NORMALIZE_AMPLITUDE.name: NormalizeAmplitude,
    StepIdentifier.PREPROCESSING_NORMALIZE_FUNDAMENTAL_FREQ.name: NormalizeFundamentalFrequency,
    # Classification
    StepIdentifier.CLASSIFIER_KNN.name: KNearestNeighbor,
}
