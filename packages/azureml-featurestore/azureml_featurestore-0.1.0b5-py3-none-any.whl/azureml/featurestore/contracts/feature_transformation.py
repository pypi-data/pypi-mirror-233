# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from abc import ABC

from azure.ai.ml._utils._experimental import experimental


@experimental
class FeatureTransformation(ABC):
    """Represents the base class for all feature transformations.
    You should not work with this class directly.
    """

    def __init__(self):
        pass
