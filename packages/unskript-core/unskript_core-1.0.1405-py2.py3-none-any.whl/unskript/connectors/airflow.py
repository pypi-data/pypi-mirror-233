##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from unskript.connectors.schema.airflow import AirflowSchema
from unskript.connectors.interface import ConnectorInterface
import unskript.thirdparty.airflow as airflow


class AirflowConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            airflowCredential = AirflowSchema(**data)
            if airflowCredential.username and airflowCredential.password:
                api = airflow.Client(airflowCredential.base_url, airflowCredential.username,
                                     airflowCredential.password.get_secret_value(), airflowCredential.version)
            else:
                api = airflow.Client(airflowCredential.base_url, airflowCredential.version)

        except Exception as e:
            raise e

        return api
