# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import sys
import threading

import pyarrow
import pyarrow.flight
from azureml.featurestore._utils._constants import PACKAGE_NAME
from azureml.featurestore._utils.utils import _build_logger
from azureml.featurestore.online._online_feature_getter_v2 import OnlineFeatureGetterV2

from azure.ai.ml._telemetry.activity import ActivityType, log_activity
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, MlException, ValidationException
from azure.core.credentials import AccessToken

package_logger = None


def _get_logger():
    global package_logger
    if package_logger is None:
        package_logger = _build_logger(__name__)
    return package_logger


class AuthTokenCredential(object):
    def __init__(self, token_dict):
        self.tokens = token_dict

    def get_token(self, *scopes, **kwargs):
        if len(scopes) != 1:
            msg = "This credential requires exactly one scope per token request."
            raise ValidationException(
                message=msg,
                no_personal_data_message=msg,
                target=ErrorTarget.IDENTITY,
                error_category=ErrorCategory.USER_ERROR,
            )

        token = self.tokens[scopes[0]]
        return AccessToken(token["token"], token["expires_on"])


class FlightFeatureRetrievalServer(pyarrow.flight.FlightServerBase):
    def __init__(self, location, credential, feature_uris, on_the_fly_feature_set_uris):
        print("initializing feature getter", flush=True)
        self.online_feature_getter = OnlineFeatureGetterV2(credential, feature_uris, on_the_fly_feature_set_uris)
        self.logger = _get_logger()
        print("Finished feature getter initiailization, starting server", flush=True)
        super(FlightFeatureRetrievalServer, self).__init__(location)
        print("Started gRPC server", flush=True)

        log_activity(
            self.logger,
            f"{PACKAGE_NAME}->FlightFeatureRetrievalServer->Init",
            ActivityType.INTERNALCALL,
            {"feature_count": len(feature_uris), "redis_database_count": len(self.online_feature_getter.redis_clients)},
        )

    def _log_success(self, num_rows, num_cols):
        """Log a successful feature data retrieval event.
        This method should *never* throw."""
        try:
            log_activity(
                self.logger,
                f"{PACKAGE_NAME}->FlightFeatureRetrievalServer->DoExchange->Success",
                ActivityType.INTERNALCALL,
                {
                    "feature_data_rows": num_rows,
                    "feature_data_columns": num_cols,
                },
            )
        except:
            pass

    def _log_error(self, exception):
        """Log an unsuccessful feature data retrieval event.
        This method should *never* throw."""
        try:
            if isinstance(exception, MlException):
                self.logger.error(
                    f"{PACKAGE_NAME}->FeatureStoreClient->DoExchange->Error, {type(exception).__name__}: {exception.no_personal_data_message}"
                )
                log_activity(
                    self.logger,
                    f"{PACKAGE_NAME}->FlightFeatureRetrievalServer->DoExchange->Error",
                    ActivityType.INTERNALCALL,
                    {
                        "exception": f"{type(exception).__name__}: {exception.no_personal_data_message}",
                    },
                )
            else:
                self.logger.error(
                    f"{PACKAGE_NAME}->FeatureStoreClient->DoExchange->Error, {type(exception).__name__}: {exception}"
                )
                log_activity(
                    self.logger,
                    f"{PACKAGE_NAME}->FlightFeatureRetrievalServer->DoExchange->Error",
                    ActivityType.INTERNALCALL,
                    {
                        "exception": f"{type(exception).__name__}: {exception}",
                    },
                )
        except:
            pass

    def do_exchange(self, context, descriptor, reader, writer):
        """Write data to a flight.
        Applications should override this method to implement their
        own behavior. The default method raises a NotImplementedError.
        Parameters
        ----------
        context : ServerCallContext
            Common contextual information.
        descriptor : FlightDescriptor
            The descriptor for the flight provided by the client.
        reader : MetadataRecordBatchReader
            A reader for data uploaded by the client.
        writer : MetadataRecordBatchWriter
            A writer to send responses to the client.
        """
        try:
            # Get feature list from descriptor
            scenario = descriptor.path[0].decode("utf-8")

            if scenario == "online":
                feature_getter = self.online_feature_getter.get_online_features
            elif scenario.startswith("offline:"):
                raise NotImplementedError("Offline feature data retrieval over grpc is not yet supported.")
            else:
                raise NotImplementedError(f"Unsupported scenario: {scenario}")

            feature_uris = [path.decode("utf-8") for path in descriptor.path[1:]]

            # Get observations dataframe from request
            observation_df = reader.read_all()
            features_df = feature_getter(feature_uris, observation_df)

            writer.begin(features_df.schema)
            writer.write_table(features_df)
            writer.close()
        except Exception as ex:
            self._log_error(ex)
            raise
        else:
            self._log_success(features_df.num_rows, features_df.num_columns)


def sentinel(server):
    # Wait as long as stdin is open.
    for line in sys.stdin:
        pass

    # stdin was closed - the parent process is likely dead.
    # Emit telemetry to appinsights
    try:
        log_activity(
            _get_logger(), f"{PACKAGE_NAME}->FlightFeatureRetrievalServer->Shutdown", ActivityType.INTERNALCALL
        )
    except:
        pass

    # Flush logs
    sys.stdout.flush()
    sys.stderr.flush()

    # Shut the server down
    server.shutdown()


def main(location, credential, feature_uris, on_the_fly_feature_sets):
    server = FlightFeatureRetrievalServer(location, credential, feature_uris, on_the_fly_feature_sets)
    threading.Thread(target=sentinel, args=(server,)).start()
    server.serve()


if __name__ == "__main__":
    # Read initialization params from stdin
    initialization_params = json.loads(sys.stdin.readline())
    location = initialization_params["location"]
    feature_uris = initialization_params["features"]
    credential = AuthTokenCredential(initialization_params["tokens"])
    on_the_fly_feature_sets = initialization_params["on_the_fly_feature_sets"]

    main(location, credential, feature_uris, on_the_fly_feature_sets)
