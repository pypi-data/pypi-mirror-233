##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class AWSv2Schema(BaseModel):
    aws_access_key_id: SecretStr = Field(
        title='Access Key ID',
        description='AWS Access Key ID')
    aws_secret_access_key: SecretStr = Field(
        title='AWS Secret Access Key',
        description='')
    aws_session_token: str = Field(
        title='Session Token',
        description='Token used to validate the temporary security credentials')
