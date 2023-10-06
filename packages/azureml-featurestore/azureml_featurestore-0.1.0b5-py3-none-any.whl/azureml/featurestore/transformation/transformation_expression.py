# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from abc import ABC

from azure.ai.ml._utils._experimental import experimental


@experimental
class TransformationExpression(ABC):
    """Feature transformation expression representation"""
