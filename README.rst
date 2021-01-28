**********************************
Azure Provision Analytics Workspaces
**********************************

This project demonstrates how to provision analytics workspaces on Azure using several technologies:

- Python Azure API
- Docker Images
- Azure Container Instances
- Azure Container Registry
- Azure Functions


|screenshot-pipeline|


Setup
=====

Create a resource group for this project

.. code-block:: bash

    az group create --name provisionAnalyticsWorkspaces --location eastus

Create a Private Docker Reposity in Azure

.. code-block:: bash
    az acr create --resource-group provisionAnalyticsWorkspaces --name pawContainerRegistry --sku Basic

Take note of `loginServer` in the output, which is the fully qualified registry name (all lowercase). Throughout the rest of this document `<registry-name>` is a placeholder for the container registry name, and `<login-server>` is a placeholder for the registry's login server name.

Create a Service Principal on Azure (Pull Images).

The solution uses a service principal to pull images from the Private Docker Repository created

Create the service principal and save the secrets

.. code-block:: bash
    az ad sp create-for-rbac --name sp_paw_test_container_repo --skip-assignment --sdk-auth > local-sp.json

Notice the username and password are saved to the file `local-sp.json`

Next we have to assign the `Azure Container Registry Pull` role-assignment to the new service principal

.. code-block:: bash

    $SERVICE_PRINCIPAL_ID = "service_principal_clientId>"
    $ACR_REGISTRY_NAME = "<registry_name>"
    $ACR_REGISTRY_ID = az acr show --name $ACR_REGISTRY_NAME  --query id --output tsv

    # Create the role assignment
    az role assignment create --assignee $SERVICE_PRINCIPAL_ID --scope $ACR_REGISTRY_ID --role acrpull

    # Show the role assignment
    az role assignment list --assignee $SERVICE_PRINCIPAL_ID

Create Azure Container Instance

Copy the file `deploy-aci-example.yaml` as `deploy-aci.yaml`

Edit the file `deploy-aci.yaml` and update with the correct values:

- image: the full name of the image 
- username: the service principal clientId
- password: the service principal clientSecret

.. code-block:: bash

    az container create --resource-group provisionAnalyticsWorkspaces --file deploy-aci.yaml





Development
===========

Style Guidelines
----------------

This project enforces quite strict `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 (Docstring Conventions) <https://www.python.org/dev/peps/pep-0257/>`_ compliance on all code submitted.

We use `Black <https://github.com/psf/black>`_ for uncompromised code formatting.

Summary of the most relevant points:

 - Comments should be full sentences and end with a period.
 - `Imports <https://www.python.org/dev/peps/pep-0008/#imports>`_  should be ordered.
 - Constants and the content of lists and dictionaries should be in alphabetical order.
 - It is advisable to adjust IDE or editor settings to match those requirements.

Ordering of imports
-------------------

Instead of ordering the imports manually, use `isort <https://github.com/timothycrosley/isort>`_.

.. code-block:: bash

    pip3 install isort
    isort -rc .

Use new style string formatting
-------------------------------

Prefer `f-strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`_ over ``%`` or ``str.format``.

.. code-block:: python

    #New
    f"{some_value} {some_other_value}"
    # Old, wrong
    "{} {}".format("New", "style")
    "%s %s" % ("Old", "style")

One exception is for logging which uses the percentage formatting. This is to avoid formatting the log message when it is suppressed.

.. code-block:: python

    _LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)


Testing
--------
You'll need to install the test dependencies into your Python environment:

.. code-block:: bash

    pip3 install -r requirements_dev.txt

Now that you have all test dependencies installed, you can run tests on the project:

.. code-block:: bash

    isort -rc .
    codespell  --skip="./.*,*.csv,*.json,*.pyc,./docs/_build/*,./htmlcov/*"
    black script
    flake8 script
    pylint script
    pydocstyle script

Build Docker Images
-------------------

Build and run your image.

Run Docker Image locally
.. code-block:: bash

    > docker build --pull --rm -f "dockerfile" -t provisionanalyticsworkspaces:latest "."
    > docker run --rm -it provisionanalyticsworkspaces:latest

    #If you want to see STDOUT use 
    > docker run --rm -a STDOUT provisionanalyticsworkspaces:latest



Tag for remote registry

.. code-block:: bash
    docker tag provisionanalyticsworkspaces:latest $ACR_REGISTRY_NAME.azurecr.io/provisionanalyticsworkspaces:v1

    az acr login --name $ACR_REGISTRY_NAME
    docker push $ACR_REGISTRY_NAME.azurecr.io/provisionanalyticsworkspaces:v4


Run the new image on Azure Container Instance


References
==========
- Create Container Registry https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli
- Create Azure Container Instance https://docs.microsoft.com/en-us/azure/container-instances/container-instances-multi-container-yaml

.. |screenshot-pipeline| image:: https://raw.github.com/briglx/provision_analytics_workspaces/master/docs/Architecture.png

