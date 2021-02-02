"""Function to start Container Instance."""
import datetime
import os
import json
import logging
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
import azure.functions as func


def get_container_client(azure_auth):
    """Get Container Client."""
    if azure_auth is not None:
        logging.info("Authenticating Azure using credentials")
        auth_config_dict = json.loads(azure_auth)
        client = get_client_from_json_dict(
            ContainerInstanceManagementClient, auth_config_dict
        )
    else:
        logging.error(
            "\nFailed to authenticate to Azure. Have you set the"
            " AZURE_AUTH environment variable?\n"
        )
    return client


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Start the container."""
    logging.info('Python HTTP trigger function processed a request.')

    cur_time = datetime.datetime.utcnow()
    cur_time = cur_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
    utc_timestamp = cur_time.isoformat()

    logging.info(f'Python HTTP trigger time is {utc_timestamp}.')

    
    azure_auth = os.environ.get("AZURE_AUTH")
    container_rg_name = os.environ.get("CONTAINER_RG")
    container_group_name = os.environ.get("CONTAINER_GROUP_NAME")

    if not azure_auth:
        raise ValueError(
            "Parameter azure_auth is required. "
            "Have you set the AZURE_AUTH environment variable?"
        )
    if not container_rg_name:
        raise ValueError(
            "Parameter rg_name is required."
            "Have you set the CONTAINER_RG env variable?"
        )
    if not container_group_name:
        raise ValueError(
            "Parameter container_group_name is required. "
            "Have you set the CONTAINER_GROUP_NAME env variable?"
        )


    logging.info(f"Starting container {container_group_name} in {container_rg_name}")
    
    # Get client
    aci_client = get_container_client(azure_auth)

    
    logging.info("starting container")
    aci_client.container_groups.start(container_rg_name, container_group_name)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
