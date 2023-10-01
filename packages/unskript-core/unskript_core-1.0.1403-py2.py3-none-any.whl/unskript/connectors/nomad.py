##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
import nomad
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.nomad import NomadSchema


class NomadConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            nomadCredential = NomadSchema(**data)
        except ValidationError as e:
            raise e
        try:
            if nomadCredential.namespace!='' and nomadCredential.token!='' and not bool(nomadCredential.verify_certs):
                # For HTTPS Nomad instances with namespace and acl token
                nomadClient = nomad.Nomad(host = nomadCredential.host, timeout=nomadCredential.timeout, secure=nomadCredential.secure, verify=nomadCredential.verify_certs, namespace=nomadCredential.namespace, token=nomadCredential.token.get_secret_value())

            elif nomadCredential.namespace=='' and nomadCredential.token=='' and not bool(nomadCredential.verify_certs):
                # For HTTPS Nomad instances with no self-signed SSL certificates
                nomadClient = nomad.Nomad(host = nomadCredential.host, timeout=nomadCredential.timeout, secure=nomadCredential.secure, verify=nomadCredential.verify_certs)

            elif nomadCredential.namespace=='' and nomadCredential.token=='' and bool(nomadCredential.verify_certs):
                # For HTTPS Nomad instances with self-signed SSL certificates
                nomadClient = nomad.Nomad(host = nomadCredential.host, timeout=nomadCredential.timeout, secure=nomadCredential.secure, verify=nomadCredential.verify_certs)

            else:
                # For HTTP Nomad instances
                nomadClient = nomad.Nomad(host = nomadCredential.host, timeout=nomadCredential.timeout)
        except Exception as e:
            raise e

        return nomadClient
