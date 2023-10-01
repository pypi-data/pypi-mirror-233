# pylint: skip-file

#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#

import requests
import json
import yaml
import os

from typing import List, Any
from pydantic import BaseModel, Field

from enum import Enum


# CONSTANTS USED IN THIS FILE 
CREDS_DIR = os.environ.get('HOME') + '/.local/share/jupyter/metadata/credential-save'

class UnskriptClient():
    def __init__(self, tenant_url: str, sha_token: str):
        self.url = tenant_url
        self.sha_token = sha_token

    def fetch_vault_token(self) -> str:
        unskript_vault_url = f"{self.url}/v1alpha1/credentials/vault"
        hdr = {"Authorization": f"unskript-sha {self.sha_token}"}
        try:
            result = requests.get(unskript_vault_url,
                headers=hdr
            )
            result.raise_for_status()
        except Exception as e:
            raise e

        output = result.json()
        return str(output.get('token'))


class CheckOutputStatus(Enum):
    SUCCESS = 1
    FAILED  = 2
    RUN_EXCEPTION = 3

class CheckOutput(BaseModel):
    status: CheckOutputStatus = Field (
        title = "Status",
        description = "Execution Status"
    )
    objects: List[Any] = Field (
        default = None,
        title = "Objects",
        description = "Output Object from the lego execution"
    )
    error: str = Field (
        default = "",
        title = "Error String",
        description = "Error String"
    )


def parseARN(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/', 1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':', 1)
    return result


def print_output_in_tabular_format(res):
    """
    Print output in tabulatr format using pandas.
    :param res: list of dict
    :return:
    """
    import pandas as pd
    df = pd.DataFrame(res)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print("\n")
    print(df)
    return res

def eval_with_try(value, vars: None):
    try:
        return eval(value, vars)
    except Exception as e:
        print(f'Could not evaluate argument {value}, {e}')
        raise e


# Utility function to determine if given kubeconfig is
# tied to any cloud provider, like  EKS, GKE or Azure
# This utility returns either AWS/GCP or AZURE as string 
# if it finds tell tale signature of CSP in the configuration else None.
def identify_cloud_provider(kubeconfig:dict):
    if not kubeconfig:
        return None

    for context_info in kubeconfig.get('contexts', []):
        context = context_info.get('context')
        cluster_name = context.get('cluster')
        cluster_info = next(
            (cluster for cluster in kubeconfig.get('clusters', []) if cluster['name'] == cluster_name),
            {}
        )
        server_url = cluster_info.get('cluster', {}).get('server', '')
        if 'eks.amazonaws.com' in server_url:
            return "AWS"
        elif 'gke' in server_url or 'gke' in cluster_name:
            return "GCP"
        elif '.azmk8s.io' in server_url:
            return "AZURE"

    return None


# Utility function that finds out if at least one
# Connector type credential is filled. This does
# not validate the data, but checks if connectorData 
# is empty or not. Returns True if empty.
def is_creds_file_empty(c_type: str):
    if not c_type:
        return True
    c_type = "CONNECTOR_TYPE_" + c_type.upper()
    c_type = c_type.strip()

    for dirpath, dirnames, filenames in os.walk(CREDS_DIR):
        for f in filenames:
            if f.endswith('.json'):
                with open(os.path.join(dirpath, f), 'r') as k:
                    c = json.loads(k.read())
                    _type = c.get('type').strip()

                    if _type == c_type:
                        if c.get('metadata').get('connectorData') != "{}":
                            return False

    return True
