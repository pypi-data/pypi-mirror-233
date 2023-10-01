##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials
from msrestazure.azure_cloud import AZURE_US_GOV_CLOUD, AZURE_CHINA_CLOUD, \
    AZURE_GERMAN_CLOUD, AZURE_PUBLIC_CLOUD
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.azure import AzureSchema
from unskript.connectors.schema.azure import ServicePrincipalCredentialsSchema, UserPassCredentialsSchema


class AzureConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            azureCredential = AzureSchema(**data)
        except ValidationError as e:
            raise e
        if isinstance(azureCredential.authentication, ServicePrincipalCredentialsSchema):
            credentials = ServicePrincipalCredentials(tenant=azureCredential.authentication.tenant_id,
                                                      client_id=azureCredential.authentication.client_id,
                                                      secret=azureCredential.authentication.client_secret.get_secret_value())
            return credentials
        elif isinstance(azureCredential.authentication, UserPassCredentialsSchema):
            #ByDefault env would be AZURE_PUBLIC_CLOUD only
            cloud_environment = AZURE_PUBLIC_CLOUD
            if azureCredential.authentication.cloud_environment != None:
                if azureCredential.authentication.cloud_environment == "AZURE_US_GOV_CLOUD":
                    cloud_environment = AZURE_US_GOV_CLOUD
                elif azureCredential.authentication.cloud_environment == "AZURE_CHINA_CLOUD":
                    cloud_environment = AZURE_CHINA_CLOUD
                elif azureCredential.authentication.cloud_environment == "AZURE_GERMAN_CLOUD":
                    cloud_environment = AZURE_GERMAN_CLOUD

            credentials = UserPassCredentials(username=azureCredential.authentication.username,
                                              password=azureCredential.authentication.password.get_secret_value(),
                                              cloud_environment=cloud_environment)


            return credentials
        else:
            return "Failed to authenticate with provided credentials. Some attributes were missing. Credentials must " \
                   "include client_id, secret and tenant or username and password."
