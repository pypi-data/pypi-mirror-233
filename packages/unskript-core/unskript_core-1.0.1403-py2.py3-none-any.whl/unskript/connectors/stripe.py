##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

import stripe
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.stripe import StripeSchema


class StripeConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            stripeCredential = StripeSchema(**data)
            stripe.api_key = stripeCredential.api_key.get_secret_value()
        except ValidationError as e:
            raise e

        return stripe
