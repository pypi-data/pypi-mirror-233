# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List

from azureml.featurestore.contracts.feature_transformation import FeatureTransformation
from azureml.featurestore.transformation.transformation_expression import TransformationExpression

from azure.ai.ml._utils._experimental import experimental


@experimental
class TransformationExpressionCollection(FeatureTransformation):
    """Group of Feature transformation expression representations
    :param transformation_expressions: list of transformation expressions
    :type transformation_expressions: list, required
    """

    def __init__(self, *, transformation_expressions: List[TransformationExpression], **kwargs):
        super().__init__()

    def __repr__(self):
        pass

    def __str__(self):
        pass
