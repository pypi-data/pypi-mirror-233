##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class KafkaSchema(BaseModel):
    broker: str = Field(
        title='Broker',
        description='host[:port] that the producer should contact to bootstrap initial cluster metadata. Default port is 9092')
    sasl_username: str = Field(
        '',
        title='SASL Username',
        description='Username for SASL PlainText Authentication.')
    sasl_password: SecretStr = Field(
        '',
        title='SASL Password',
        description='Password for SASL PlainText Authentication.')
    zookeeper: Optional[str] = Field(
        '',
        title='Zookeeper',
        description='zookeeper connection string. This is needed to do health checks. Eg: host[:port]. The default port is 2182')
