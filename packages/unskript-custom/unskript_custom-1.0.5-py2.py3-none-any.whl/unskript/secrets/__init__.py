# pylint: skip-file
#
##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

"""
Following variables need to be defined.
"""
ENV_MODE_LOCAL = "ENV_MODE_LOCAL"
ENV_MODE_AWS = "ENV_MODE_AWS"
ENV_MODE_GCP = "ENV_MODE_GCP"
ENV_MODE_PRIVATE_CLOUD = "ENV_MODE_PRIVATE_CLOUD"
ENV_MODE_UNSKRIPT_HOSTED = "ENV_MODE_UNSKRIPT_HOSTED"
ENV_MODE = "ENV_MODE"
SECRET_STORE_TYPE_AWS = "SECRET_STORE_TYPE_AWS"
SECRET_STORE_TYPE_GCP = "SECRET_STORE_TYPE_GCP"
SECRET_STORE_TYPE_REDIS = "SECRET_STORE_TYPE_REDIS"
SECRET_STORE_TYPE_VAULT = "SECRET_STORE_TYPE_VAULT"
SECRET_STORE_TYPE = "SECRET_STORE_TYPE"

class Secrets():
    """
    Create an object of the appropriate type, be it AWS, GCP or local.
    Environment specific details will be part of the kwargs. For eg, AWS_REGION, AWS_SECRET_PREFIX, etc.
    """
    def __init__(self, input_dict):
        envType = input_dict.get(ENV_MODE)
        secretStoreType = input_dict.get(SECRET_STORE_TYPE)
        try:
            if secretStoreType == SECRET_STORE_TYPE_AWS:
                from unskript.secrets.aws_secret import AWSSecret
                self.secretStore = AWSSecret(input_dict=input_dict)
            elif secretStoreType == SECRET_STORE_TYPE_GCP:
                from unskript.secrets.gcp_secret import GCPSecret
                self.secretStore = GCPSecret(input_dict=input_dict)
            elif secretStoreType == SECRET_STORE_TYPE_REDIS:
                from unskript.secrets.redis_secret import RedisSecret
                self.secretStore = RedisSecret(input_dict=input_dict)
            elif secretStoreType == SECRET_STORE_TYPE_VAULT:
                from unskript.secrets.vault_secret import VaultSecret
                self.secretStore = VaultSecret(input_dict=input_dict)
            elif envType == ENV_MODE_LOCAL:
                from unskript.secrets.metadata_secret import MetadataSecretStore
                self.secretStore = MetadataSecretStore(input_dict=input_dict)
            else:
                raise Exception("Unsupported secret store type %s", secretStoreType)
        except Exception as e:
            raise e

class SecretsStore():
    """
    Create an object of the appropriate type, be it AWS, GCP or local.
    Environment specific details will be part of the kwargs. For eg, AWS_REGION, AWS_SECRET_PREFIX, etc.
    """
    def __init__(self, envType, secretStoreType, cfg):
        self.envType = envType
        try:
            if secretStoreType == SECRET_STORE_TYPE_AWS:
                from unskript.secrets.aws_secret import AWSSecret
                self.secretStore = AWSSecret(input_dict=cfg)
            elif secretStoreType == SECRET_STORE_TYPE_GCP:
                from unskript.secrets.gcp_secret import GCPSecret
                self.secretStore = GCPSecret(input_dict=cfg)
            elif secretStoreType == SECRET_STORE_TYPE_REDIS:
                from unskript.secrets.redis_secret import RedisSecret
                self.secretStore = RedisSecret(input_dict=cfg)
            elif secretStoreType == SECRET_STORE_TYPE_VAULT:
                from unskript.secrets.vault_secret import VaultSecret
                self.secretStore = VaultSecret(input_dict=cfg)
            elif envType == ENV_MODE_LOCAL:
                from unskript.secrets.metadata_secret import MetadataSecretStore
                self.secretStore = MetadataSecretStore(input_dict=cfg)
            else:
                raise Exception("Unsupported secret store type %s", secretStoreType)
        except Exception as e:
            raise e

    def get_secret(self, type, id):
        return self.secretStore.get_secret(type, id)

    def get_secret_by_name(self, name):
        return self.secretStore.get_secret(name)
