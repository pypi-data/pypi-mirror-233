# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import unittest

import pytest
from azureml.featurestore.contracts import DateTimeOffset
from azureml.featurestore.transformation.aggregation_function import AggregationFunction
from azureml.featurestore.transformation.window_aggregation import WindowAggregation


@pytest.mark.unittest
class TransformationTest(unittest.TestCase):
    def test_window_aggregation(self):
        rwa = WindowAggregation(
            feature_name="3d_sum_of_column1",
            source_column="column1",
            aggregation=AggregationFunction.SUM,
            window=DateTimeOffset(3, 0, 0),
        )
