##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import yaml
import os
import tempfile

from pydantic import ValidationError
from kubernetes import config

from unskript.connectors.schema.k8 import K8Schema
from unskript.connectors.interface import ConnectorInterface
from unskript.legos.utils import identify_cloud_provider, is_creds_file_empty

from subprocess import PIPE, run


class K8Connector(ConnectorInterface):

    def k8s_cli_cmd(self, cmd: str, name: str):

        cmd = cmd.strip()
        if cmd.startswith("kubectl") is False:
            raise ValueError("command does not start with kubectl")

        # reject if the command has specified another kubeconfig
        if cmd.find("--kubeconfig=") != -1:
            raise ValueError("command specifies kubeconfig in addition to selected credential")

        # if its an exec command then make sure tty is not stdin
        if cmd.strip('kubectl').strip().startswith("exec") is True:
            if cmd.find(" -it") != -1 or cmd.find(" -t") != -1 or cmd.find("-tty=false") != -1:
                raise ValueError("command contains -it which needs a tty")
        return f"export KUBECONFIG={name} ; {cmd}"

    def get_handle(self, data):
        try:
            k8Credential = K8Schema(**data)
        except ValidationError as e:
            raise e

        yamlDict = yaml.load(k8Credential.kubeconfig, Loader=yaml.FullLoader)

        # fill in default namespace if unspecified
        for c in yamlDict.get('contexts'):
            if c.get('context') is None:
                continue
            if c.get('context').get('namespace') is None:
                c['context']['namespace'] = 'default'

        # Throw a warning to migrate to aws cli instead of aws-iam-authenticator
        for u in yamlDict.get('users'):
            if u.get('user') is None:
                continue
            if u.get('user').get('exec') is None:
                continue
            if u.get('user').get('exec').get('command') is None:
                continue
            if u.get('user').get('exec').get('command') == "aws-iam-authenticator":
                print(f'WARNING: Please use aws cli instead of aws-iam-authenticator as aws-iam-authenticator slows down kubectl commands')
        
        # We need to check if the K8S credential depends on any Cloud provider 
        # like EKS, GCP credential to be programmed first. If we detect any such
        # dependency, we throw a warning and proceed with executation (which may result in unexpected result).
        
        csp = identify_cloud_provider(yamlDict)
        if csp != None: 
            if is_creds_file_empty(csp) == True:
                print(f"ERROR: Given Kubernetes Configuration depends on Cloud Provider {csp} Credential to be programmed first!")
            else:
                # This means we are good to go
                pass 
        
        handler, name = tempfile.mkstemp()
        os.write(handler, str.encode(yaml.safe_dump(yamlDict)))
        os.close(handler)

        k8Client = config.new_client_from_config(config_file=name)
        k8Client.run_native_cmd = lambda cmd: run(self.k8s_cli_cmd(
            cmd, name), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        return k8Client
