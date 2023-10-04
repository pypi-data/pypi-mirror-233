##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import os
from typing import Any
from boto3.session import Session
from boto3 import client
from subprocess import PIPE, run, Popen
import yaml
import urllib3
import json
import subprocess
from pydantic import ValidationError
from pathlib import Path
from unskript.connectors.k8 import K8Connector
from unskript.connectors.schema.aws import AWSSchema, AccessKeySchema
from unskript.connectors.interface import ConnectorInterface
from unskript.thirdparty.cli import execute_cli_sync

UNSKRIPT_SIDECAR_URL_ENV_VARIABLE = "UNSKRIPT_SIDECAR_URL"

class AWSConnector(ConnectorInterface):

    session = Session()

    def __init__(self):
        sidecar_base = os.getenv(UNSKRIPT_SIDECAR_URL_ENV_VARIABLE, 'http://sidecar.sidecar.svc.cluster.local')
        sidecar_port = ':8080'
        sidecar_action = '/internal/v1alpha1/command'
        self.sidecar_url = sidecar_base + sidecar_port + sidecar_action
        self.aws_creds_path = f'{Path.home()}/.aws'

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

    def get_creds(self, rolearn: str, rolename: str, external_id: str) -> str:
        command = 'aws sts assume-role --role-arn ' + rolearn.strip()
        command = command + ' --role-session-name ' + rolename.strip()

        if external_id not in ("", None):
            command = command + ' --external-id ' + external_id.strip()

        env_vars = os.environ.copy()
        exec_res = execute_cli_sync(command, env_vars=env_vars)
        if exec_res.returncode != 0:
            raise RuntimeError(f"aws get credentials error: {exec_res.stderr}")

        return exec_res.stdout

    def update_session_creds(self, credentials):
        # Check whether the specified path exists or not
        isExist = os.path.exists(self.aws_creds_path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(self.aws_creds_path)

        aws_creds_path = self.aws_creds_path + "/credentials"
        file = Path(aws_creds_path)
        if credentials['Credentials']['SessionToken'] in ('', None):
            file_contents = '''
            [unskript]
            aws_access_key_id = %s
            aws_secret_access_key = %s
               ''' % (credentials['Credentials']['AccessKeyId'], credentials['Credentials']['SecretAccessKey'])
        else:
            file_contents = '''
            [unskript]
            aws_access_key_id = %s
            aws_secret_access_key = %s
            aws_session_token = %s
            ''' % (credentials['Credentials']['AccessKeyId'], credentials['Credentials']['SecretAccessKey'], credentials['Credentials']['SessionToken'])
        with open(file, "w") as f:
            f.writelines(file_contents)

    def get_eks_handle(self, cluster_name, region) -> Any:

        eksClient = self.session.client('eks', region_name=region)

        cluster = eksClient.describe_cluster(name=cluster_name)
        cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
        cluster_endpoint = cluster["cluster"]["endpoint"]

        cluster_config = {'apiVersion': 'v1',
                          'clusters': [{'cluster': {'certificate-authority-data': str(cluster_cert),
                                                    'server': str(cluster_endpoint)},
                                        'name': 'kubernetes'}],
                          'contexts': [{'context': {'cluster': 'kubernetes', 'user': 'aws'},
                                        'name': 'aws'}],
                          'current-context': 'aws',
                          'kind': 'Config',
                          'preferences': {},
                          'users': [{'name': 'aws',
                                     'user': {'exec': {'apiVersion': 'client.authentication.k8s.io/v1alpha1',
                                                       'args': ['eks', 'get-token', '--cluster-name', cluster_name],
                                                       'command': 'aws'}}}]}

        config_text = yaml.dump(cluster_config, default_flow_style=False)

        k8shandle = K8Connector().get_handle(data={"kubeconfig": config_text})
        return k8shandle

    def check_aws_cli_command(self, cmd):
        if cmd.startswith("aws") is False:
            raise ValueError("aws cli command does not start with aws")
        return

    def run_aws_cli_command(self, awsCredential, cmd):
        cmd = cmd.strip()
        self.check_aws_cli_command(cmd)
        if isinstance(awsCredential.authentication, AccessKeySchema):
            credentials = {}
            credentials['Credentials'] = {}
            credentials['Credentials']['AccessKeyId'] = awsCredential.authentication.access_key
            credentials['Credentials']['SecretAccessKey'] = awsCredential.authentication.secret_access_key.get_secret_value()
            credentials['Credentials']['SessionToken'] = ''
        else:
            creds = self.get_creds(awsCredential.authentication.role_arn, awsCredential.authentication.role_session_name, awsCredential.authentication.external_id.get_secret_value())
            credentials = json.loads(creds)

        if os.environ.get('UNSKRIPT_MODE') != None:
            self.update_session_creds(credentials)

        env_vars = os.environ.copy()
        # When we are running in the Docker mode, When a credential is
        # Created, we set the UNSKRIPT_AWS_PROFILE and here the check
        # is done if this env variable is set.
        # When we are running in SaaS/onPrem mode, we support aws
        # Assume role, we use the current STS assume role and get the
        # Current Session token/Access key and Secret Key and update
        # Those value in the ~/.aws/credentials file with the `unskript`
        # Profile name.
        if os.environ.get('UNSKRIPT_AWS_PROFILE') != None:
            env_vars['AWS_PROFILE'] = os.environ.get('UNSKRIPT_AWS_PROFILE')
        else:
            env_vars['AWS_PROFILE'] = 'awscreds'

        exec_res = execute_cli_sync(cmd, env_vars=env_vars)
        if exec_res.returncode != 0:
            raise RuntimeError(f"aws cli execution error: {exec_res.stderr}")

        return exec_res

    def get_handle(self, data, credential_id) -> Session:
        try:
            awsCredential = AWSSchema(**data)
        except ValidationError as e:
            raise e
        if isinstance(awsCredential.authentication, AccessKeySchema):
            self.session = Session(
                aws_access_key_id=awsCredential.authentication.access_key,
                aws_secret_access_key=awsCredential.authentication.secret_access_key.get_secret_value())
        else:
            sts_client = client('sts')
            if awsCredential.authentication.external_id.get_secret_value() != '':
                assumed_role_object = sts_client.assume_role(
                    RoleArn=awsCredential.authentication.role_arn,
                    RoleSessionName=awsCredential.authentication.role_session_name,
                    ExternalId=awsCredential.authentication.external_id.get_secret_value())

            else:
                assumed_role_object = sts_client.assume_role(
                    RoleArn=awsCredential.authentication.role_arn,
                    RoleSessionName=awsCredential.authentication.role_session_name)

            credentials = assumed_role_object['Credentials']
            self.session = Session(
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                )
        self.session.unskript_get_eks_handle = self.get_eks_handle
        self.session.aws_cli_command = lambda cmd: self.run_aws_cli_command(awsCredential, cmd)
        self.session.credential_id = credential_id
        # Following additions are for Terraform Support
        # r : repo_path
        # b : branch of code repository
        # c : connector_id
        # d : directory within the repo to run the command from
        # cmd: Terraform command to run
        # args: Terraform command argument
        self.session.sidecar_command = lambda r, b, c, d, cmd, args: urllib3.PoolManager().request(
            'POST',
            self.sidecar_url,
            headers={'Content-Type': 'application/json'},
            body=self.sidecar_params(r, b, c, d, cmd, args))


        return self.session


def aws_get_paginator(aws_handle, obj, content, **kwargs):
    """
    aws paginator to get all res details from given object.
    :param aws_handle: boto3 aws handle.
    :param obj: obj name fetch from.
    :param content: get response from given key.
    :param kwargs: kwargs to pass aws object.
    :return: list of objects.
    """
    # Create a reusable Paginator
    paginator = aws_handle.get_paginator(obj)

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(**kwargs)
    res = []
    for page in page_iterator:
        res.extend(page[content])
    return res
