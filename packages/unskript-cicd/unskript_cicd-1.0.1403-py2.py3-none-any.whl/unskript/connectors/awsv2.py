##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import os
from boto3.session import Session

import urllib3
import json
from pydantic import ValidationError

from unskript.connectors.schema.awsv2_schema import AWSv2Schema
from unskript.connectors.interface import ConnectorInterface

UNSKRIPT_SIDECAR_URL_ENV_VARIABLE = "UNSKRIPT_SIDECAR_URL"

class AwsV2Connector(ConnectorInterface):
    session = Session()

    def __init__(self):
        sidecar_base = os.getenv(UNSKRIPT_SIDECAR_URL_ENV_VARIABLE, 'http://sidecar.sidecar.svc.cluster.local')
        sidecar_port = ':8080'
        sidecar_action = '/internal/v1alpha1/command'
        self.sidecar_url = sidecar_base + sidecar_port + sidecar_action

    def sidecar_params(self, r, b, c, d, cmd, args):
        params = json.dumps({
            "command_type": "terraform",   # Needed to differentitate commands
            "repo_path": r,
            "repo_branch": b,
            "connector_id": c,
            "dir_path": d,
            "command": cmd,
            "args": args
        })
        return params

    def get_handle(self, data) -> Session:
        try:
            awsv2Credential = AWSv2Schema(**data)
        except ValidationError as e:
            raise e

        self.session = Session(
            aws_access_key_id= awsv2Credential.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=awsv2Credential.aws_secret_access_key.get_secret_value(),
            aws_session_token=awsv2Credential.aws_session_token,
        )

        self.session.sidecar_command = lambda r, b, c, d, cmd, args: urllib3.PoolManager().request(
            'POST',
            self.sidecar_url,
            headers={'Content-Type': 'application/json'},
            body=self.sidecar_params(r, b, c, d, cmd, args))

        return self.session
