##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class SplunkSchema(BaseModel):
    hostname: str = Field(
        title='Hostname',
        description='Hostname of the splunk.'
    )
    port: int = Field(
        title='Port',
        description='Port on which splunk server is listening.'
    )
    token: Optional[str] = Field(
        default='',
        title='Bearer Token',
        description='Bearer token for splunk authentication.'
    )
