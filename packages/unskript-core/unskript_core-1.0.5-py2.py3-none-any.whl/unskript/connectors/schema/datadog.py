##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class DatadogSchema(BaseModel):
    api_key: SecretStr = Field(
        title='API Key',
        description=' API key to submit metrics and events to Datadog.'
    )
    app_key: SecretStr = Field(
        title='APP Key',
        description='App Key for access to Datadog’s programmatic API.'
    )
    api_host: Optional[str] = Field(
        title='API Host',
        description="Datadog API endpoint. \n"
                    "Supported endponts: ['datadoghq.com', 'us3.datadoghq.com', 'us5.datadoghq.com', 'datadoghq.eu', 'ddog-gov.com']."
    )
