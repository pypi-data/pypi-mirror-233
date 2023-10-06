# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.featurestore.contracts import DateTimeOffset
from azureml.featurestore.transformation.aggregation_function import AggregationFunction
from azureml.featurestore.transformation.transformation_expression import TransformationExpression

from azure.ai.ml._utils._experimental import experimental


@experimental
class WindowAggregation(TransformationExpression):
    """Feature transformation expression representation for window aggregation
    :param feature_name: The feature name e.g. 3d_sum_of_column1
    :type feature_name: str, required
    :param source_column: The source data path e.g. column1
    :type source_column: str, required
    :param aggregation: The aggregation being performed e.g. SUM, AVG etc.
    :type aggregation: Enum, required
    :param window: The aggregation window e.g. 3d, 5d etc.
    :type window: DateTimeOffset, required
    """

    def __init__(
        self,
        *,
        feature_name: str,
        source_column: str,
        aggregation: AggregationFunction,
        window: DateTimeOffset,
        **kwargs
    ):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass
