"""Simple Classifiers.

Contains classifiers like the k-nearest-neighbor or
naive bayes classifier.
Outputs of the classifier steps are the classification score,
not the classified labels.

These steps are meant as an easy way to validate your pipelines
with simple classifiers, without having to switch packages.
More sophisticated classifying tasks should be implemented
outside of the pyProcessingPipeline.
"""

from .knn import KNearestNeighbor

__all__ = ["KNearestNeighbor"]
