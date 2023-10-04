##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.prometheus import PrometheusSchema
from unskript.thirdparty.prometheus.prometheus_client import PrometheusApiClient


class PrometheusConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            prometheusCredential = PrometheusSchema(**data)
        except ValidationError as e:
            raise e

        try:
            promClient = PrometheusApiClient(url=prometheusCredential.url, disable_ssl=prometheusCredential.disable_ssl,
                                             headers=prometheusCredential.headers)
        except Exception as e:
            raise e

        return promClient
