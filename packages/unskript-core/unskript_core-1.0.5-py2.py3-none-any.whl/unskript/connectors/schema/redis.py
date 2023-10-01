##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class RedisSchema(BaseModel):
    host: str = Field(
        title='Hostname',
        description='Hostname of the redis server.'
    )
    port: Optional[int] = Field(
        6379,
        title='Port',
        description='Port on which redis server is listening.'
    )
    username: Optional[str] = Field(
        '',
        title='Username',
        description='Username to authenticate to redis.'
    )
    password: Optional[SecretStr] = Field(
        '',
        title='Password',
        description='Password to authenticate to redis.'
    )
    db: int = Field(
        0,
        title='Database',
        description='ID of the database to connect to.'
    )
    use_ssl: bool = Field(
        False,
        title='Use SSL',
        description='Use SSL for communicating to Redis host.'
    )
