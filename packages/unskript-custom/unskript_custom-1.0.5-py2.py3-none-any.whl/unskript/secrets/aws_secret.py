##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import json
import boto3
from botocore.exceptions import ClientError
import base64

from unskript.secrets.interface import SecretInterface

# AWS Specific variables
AWS_REGION = "AWS_REGION"
AWS_SECRET_PREFIX = "AWS_SECRET_PREFIX"

class AWSSecret(SecretInterface):
    session = boto3.session.Session()
    def __init__(self, input_dict):
        self.client = self.session.client(
            service_name='secretsmanager',
            region_name=input_dict.get(AWS_REGION))
        self.region = input_dict.get(AWS_REGION)
        self.secretPrefix = input_dict.get(AWS_SECRET_PREFIX)

    def get_secret(self, connectorType:str, key:str)->str:
        """
            Create the key based on how its stored in the secret store.
        """
        key = self.create_key(connectorType, key)
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=key
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + key + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            elif e.response['Error']['Code'] == 'DecryptionFailure':
                print("The requested secret can't be decrypted using the provided KMS key:", e)
            elif e.response['Error']['Code'] == 'InternalServiceError':
                print("An error occurred on service side:", e)
            raise(e)
        else:
            #Secrets are base64 encoded
            base64_bytes = get_secret_value_response['SecretString'].encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            text_secret_data = json.loads(message_bytes.decode('ascii'))
            return text_secret_data
    """
    Creates the key based
    """
    def create_key(self, connectorType:str, key:str)->str:
            separator = "/"
            secretKeys = (self.secretPrefix, connectorType, key)
            return separator.join(secretKeys)
