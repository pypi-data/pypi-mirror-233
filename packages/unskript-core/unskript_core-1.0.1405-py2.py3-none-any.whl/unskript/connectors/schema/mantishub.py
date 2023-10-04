##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class MantishubSchema(BaseModel):
    base_url: str = Field(
        title='Base URL',
        description='Base URL of Mantishub account')
    api_token: SecretStr = Field(
        default='',
        title='API Token',
        description='API token for authentication'
    )
