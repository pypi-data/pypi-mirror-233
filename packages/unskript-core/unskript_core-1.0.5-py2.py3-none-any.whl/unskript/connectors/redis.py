##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
import boto3
from pydantic import ValidationError
import psycopg2
import redis

from unskript.connectors.schema.redis import RedisSchema
from unskript.connectors.interface import ConnectorInterface

class RedisConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            redisGreSQLCredential = RedisSchema(**data)
        except ValidationError as e:
            raise e

        try:
            if redisGreSQLCredential.username != "":
                conn = redis.StrictRedis(ssl=redisGreSQLCredential.use_ssl,
                                        host=redisGreSQLCredential.host, 
                                        port=redisGreSQLCredential.port, 
                                        db=redisGreSQLCredential.db, 
                                        username=redisGreSQLCredential.username, 
                                        password=redisGreSQLCredential.password.get_secret_value(),
                                        socket_connect_timeout=2)
            else:
                pool = redis.ConnectionPool(host=redisGreSQLCredential.host, 
                                            port=redisGreSQLCredential.port, 
                                            db=redisGreSQLCredential.db
                                            )
                conn = redis.Redis(connection_pool=pool,ssl=redisGreSQLCredential.use_ssl, socket_connect_timeout=2)
            conn.ping()
        except Exception as e:
            raise e
        return conn
