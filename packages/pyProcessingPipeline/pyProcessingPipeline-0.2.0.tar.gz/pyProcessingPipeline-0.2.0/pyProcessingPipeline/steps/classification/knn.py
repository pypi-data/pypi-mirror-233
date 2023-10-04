"""Contains a k-nearest-neighbor classifier."""

import logging
from collections.abc import Sequence

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import ProcessingStepInput, StepLog

logger = logging.getLogger(__name__)


class MissingLabelsError(ProcessingError):
    """Raised of the labels are empty, therefore no classification possible."""


class KNearestNeighbor(ProcessingStep):
    """K-nearest-neighbor classifier.

    Example
    -------

    To create and test a k-nearest-neighbor classifier,
    we first create some 2d samples with their labels.

    >>> from sklearn.datasets import make_blobs
    >>> x, y = make_blobs(centers=2, random_state=0)

    With both samples and their labels ready,
    we can now create the processing run

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run with a simple nearest neighbor classifier",
    ... )

    and add the classifier as a processing step

    >>> processing_run.add_step(
    ...     KNearestNeighbor(
    ...         n_neighbors=5,
    ...         n_folds=5
    ...     )
    ... )
    >>> from pyProcessingPipeline.types import LabeledProcessingStepInput
    >>> processing_run.run(LabeledProcessingStepInput(x, y))

    We can now check how good the classification with 5 nearest neighbors
    and two-fold cross validation actually is.

    The output contains the accuracy for classification when using the complete set.

    >>> processing_run.results[0]
    0.98

    Comparing this to a 10-nearest-neighbor classifier gives
    a slightly worse result:

    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run with a simple nearest neighbor classifier",
    ... )

    >>> processing_run.add_step(
    ...     KNearestNeighbor(
    ...         n_neighbors=10,
    ...         n_folds=5
    ...     )
    ... )
    >>> processing_run.run(LabeledProcessingStepInput(x, y))
    >>> processing_run.results[0]
    0.97

    To access the actual k-fold accuracy, check the step log.

    >>> processing_run.steps[0].logs[3]
    {'element_index': 0, 'description': 'accuracyFold0', 'value': 0.9}

    >>> processing_run.steps[0].logs[5]
    {'element_index': 0, 'description': 'accuracyFold1', 'value': 1.0}

    and so on.
    """

    _n_neighbors: int
    _n_folds: int
    _stratified: bool

    def __init__(self, n_neighbors: int, n_folds: int = 5, stratified: bool = False):
        """Create a KNN classifier.

        The results of this classifier is an array of scores,
        one for each cross validation fold.

        Parameters
        ----------
        n_neighbors : int
            Amount of neighbors to use for class selection.
        n_folds : int, optional
            Amount of folds to use for cross validation, by default 5.
        stratified : bool
            Wether to use stratified or regular crossvalidation.
        """
        super().__init__(locals())
        self._n_neighbors = n_neighbors
        self._n_folds = n_folds
        self._stratified = stratified

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.CLASSIFIER_KNN

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        if labels is None:
            raise MissingLabelsError("Labels missing.")

        self._init_results()
        # Keep input/output mapping to same,
        # so we can access the given labels after classification
        self._input_mapping = {index: index for index in range(len(step_input.data))}

        # Do one step with all labels in the train set prediction on self...
        classifier = KNeighborsClassifier(n_neighbors=self._n_neighbors).fit(
            step_input.data, labels
        )

        # And store the confusion and accuracy in the step log
        predicted_classes = classifier.predict(step_input.data)
        self._data.append(accuracy_score(labels, predicted_classes))
        self._logs.append(
            StepLog(
                element_index=0,
                description="confusionMatrixAll",
                value=confusion_matrix(labels, predicted_classes),
            )
        )
        self._logs.append(
            StepLog(
                element_index=0,
                description="accuracyAll",
                value=accuracy_score(labels, predicted_classes),
            )
        )

        # Also do one for every cross validation fold...
        if self._stratified:
            k_fold = StratifiedKFold(n_splits=self._n_folds)
        else:
            k_fold = KFold(n_splits=self._n_folds)
        for index, (train_idx, test_idx) in enumerate(
            k_fold.split(step_input.data, labels)
        ):
            indexable_input = np.array(step_input.data)
            indexable_labels = np.array(labels)
            # Fit classifier with train dataset
            classifier = KNeighborsClassifier(n_neighbors=self._n_neighbors).fit(
                indexable_input[train_idx], indexable_labels[train_idx]
            )
            # Predict labels of test dataset
            predicted_classes = classifier.predict(indexable_input[test_idx])
            # Store confusion and accuracy
            self._logs.append(
                StepLog(
                    element_index=0,
                    description=f"confusionMatrixFold{index}",
                    value=confusion_matrix(
                        indexable_labels[test_idx], predicted_classes
                    ),
                )
            )
            self._logs.append(
                StepLog(
                    element_index=0,
                    description=f"accuracyFold{index}",
                    value=accuracy_score(indexable_labels[test_idx], predicted_classes),
                )
            )
