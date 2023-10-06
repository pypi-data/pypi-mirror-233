# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from collections import OrderedDict
from typing import Dict

from azureml.featurestore._utils.utils import _resolve_hdfs_path_from_storage_info
from azureml.featurestore.contracts.datetimeoffset import DateTimeOffset
from azureml.featurestore.contracts.timestamp_column import TimestampColumn

from azure.ai.ml.entities._assets._artifacts.artifact import ArtifactStorageInfo

from .feature_source_base import FeatureSourceBase


class SimpleFeatureSource(FeatureSourceBase):
    """A simple feature source (abstract)
    :param path: The source data path
    :type path: str, required
    :param timestamp_column: Timestamp column for this feature set
    :type timestamp_column: TimestampColumn, required
    :param source_delay: The source delay
    :type source_delay: DateTimeOffset, optional"""

    def __init__(
        self,
        *,
        path: str,
        timestamp_column: TimestampColumn = None,
        source_delay: DateTimeOffset = None,
    ):
        self.path = path
        super().__init__(timestamp_column=timestamp_column, source_delay=source_delay)

    def _update_path(self, asset_artifact: ArtifactStorageInfo) -> None:
        # Workaround for cross-workspace data access
        hdfs_path = _resolve_hdfs_path_from_storage_info(asset_artifact)
        self.path = hdfs_path

    def _to_dict(self) -> Dict:
        info = OrderedDict()
        info["path"] = self.path
        info["timestamp_column"] = self.timestamp_column.__repr__()
        info["source_delay"] = self.source_delay.__repr__()

        return info
