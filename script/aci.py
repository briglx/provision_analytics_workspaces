#!/usr/bin/python
"""Main script for provision analytics workspaces."""
import argparse
import logging
import os
import sys
from collections import namedtuple

from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
    Container,
    ContainerGroup,
    ContainerGroupRestartPolicy,
    EnvironmentVariable,
    OperatingSystemTypes,
    ResourceRequests,
    ResourceRequirements,
)
from msrest.authentication import BasicTokenAuthentication

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def run_task_based_container(
    aci_client,
    resource_group,
    container_group_name,
    container_name,
    container_image_name,
    start_command_line=None,
):
    """Creates a container group with a single task-based container who's
       restart policy is 'Never'. If specified, the container runs a custom
       command line at startup.

    Arguments:
        aci_client {azure.mgmt.containerinstance.ContainerInstanceManagementClient}
                    -- An authenticated container instance management client.
        resource_group {azure.mgmt.resource.resources.models.ResourceGroup}
                    -- The resource group in which to create the container group.
        container_group_name {str}
                    -- The name of the container group to create.
        container_name {str}
                    -- The name of the container to create.
        container_image_name {str}
                    -- The container image name and tag, for example:
                       microsoft\aci-helloworld:latest
        start_command_line {str}
                    -- The command line that should be executed when the
                       container starts. This value can be None.
    """
    # If a start command wasn't specified, use a default
    if start_command_line is None:
        start_command_line = "-c default/path/from/function"

    # Configure some environment variables in the container which the
    # wordcount.py or other script can read to modify its behavior.
    env_var_1 = EnvironmentVariable(
        name="STORAGE_CONNECTION_STRING", value="path/from/function/enviro"
    )
    env_var_2 = EnvironmentVariable(name="MinLength", value="8")

    logging.info(
        f"Creating container group '{container_group_name}' with start command '{start_command_line}'"
    )

    # Configure the container
    container_resource_requests = ResourceRequests(memory_in_gb=1.5, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests
    )
    container = Container(
        name=container_name,
        image=container_image_name,
        resources=container_resource_requirements,
        command=start_command_line.split(),
        environment_variables=[env_var_1, env_var_2],
    )

    # Configure the container group
    group = ContainerGroup(
        location=resource_group.location,
        containers=[container],
        os_type=OperatingSystemTypes.linux,
        restart_policy=ContainerGroupRestartPolicy.never,
    )

    # Create the container group
    result = aci_client.container_groups.begin_create_or_update(
        resource_group.name, container_group_name, group
    )

    # Wait for the container create operation to complete. The operation is
    # "done" when the container group provisioning state is one of:
    # Succeeded, Canceled, Failed
    while result.done() is False:
        sys.stdout.write(".")
        time.sleep(1)

    # Get the provisioning state of the container group.
    container_group = aci_client.container_groups.get(
        resource_group.name, container_group_name
    )

    if str(container_group.provisioning_state).lower() == "succeeded":
        logging.info(
            f"\nCreation of container group '{container_group_name}' succeeded."
        )
    else:
        logging.info(
            f"\nCreation of container group '{container_group_name}' failed. Provisioning state is: {container_group.provisioning_state}"
        )


def main():

    # Retrieve the IDs and secret to use with ClientSecretCredential
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    container_rg_location = os.environ.get("SCRIPT_CONTAINER_RG_LOCATION")
    container_rg_name = os.environ.get("SCRIPT_CONTAINER_RG_NAME")
    container_group_name = os.environ.get("SCRIPT_CONTAINER_GROUP_NAME")
    container_name = os.environ.get("SCRIPT_CONTAINER_NAME")
    container_image_name = os.environ.get("SCRIPT_CONTAINER_IMAGE_NAME")

    if not subscription_id:
        raise ValueError(
            "Parameter subscription_id is required."
            "Have you set the AZURE_SUBSCRIPTION_ID env variable?"
        )

    if not tenant_id:
        raise ValueError(
            "Parameter tenant_id is required."
            "Have you set the AZURE_TENANT_ID env variable?"
        )

    if not client_id:
        raise ValueError(
            "Parameter client_id is required."
            "Have you set the AZURE_CLIENT_ID env variable?"
        )

    if not client_secret:
        raise ValueError(
            "Parameter client_secret is required."
            "Have you set the AZURE_CLIENT_SECRET env variable?"
        )

    if not container_rg_location:
        raise ValueError(
            "Parameter container_rg_location is required."
            "Have you set the SCRIPT_CONTAINER_RG_LOCATION env variable?"
        )

    if not container_rg_name:
        raise ValueError(
            "Parameter container_rg_name is required."
            "Have you set the SCRIPT_CONTAINER_RG_NAME env variable?"
        )

    if not container_group_name:
        raise ValueError(
            "Parameter container_group_name is required."
            "Have you set the SCRIPT_CONTAINER_GROUP_NAME env variable?"
        )

    if not container_name:
        raise ValueError(
            "Parameter container_name is required."
            "Have you set the SCRIPT_CONTAINER_NAME env variable?"
        )

    if not container_image_name:
        raise ValueError(
            "Parameter container_image_name is required."
            "Have you set the SCRIPT_CONTAINER_IMAGE_NAME env variable?"
        )

    credential = DefaultAzureCredential(
        exclude_cli_credential=True,
        exclude_visual_studio_code_credential=True,
        exclude_shared_token_cache_credential=True,
        exclude_interactive_browser_credential=True,
    )

    ResourceGroup = namedtuple("ResourceGroup", "location name")
    resource_group = ResourceGroup(container_rg_location, container_rg_name)

    credential = DefaultAzureCredential(
        exclude_cli_credential=True,
        exclude_visual_studio_code_credential=True,
        exclude_shared_token_cache_credential=True,
        exclude_interactive_browser_credential=True,
    )

    aci_client = ContainerInstanceManagementClient(credential, subscription_id)

    run_task_based_container(
        aci_client,
        resource_group,
        container_group_name,
        container_name,
        container_image_name,
    )


if __name__ == "__main__":
    logging.info("Starting script")

    # parser = argparse.ArgumentParser(
    #     description="Create Container Instance.",
    #     add_help=True,
    # )
    # parser.add_argument(
    #     "--connection_string",
    #     "-c",
    #     help="Storage Account Connection String",
    # )

    # args = parser.parse_args()

    # connection_string = args.connection_string or os.environ.get(
    #     "STORAGE_CONNECTION_STRING"
    # )

    main()
