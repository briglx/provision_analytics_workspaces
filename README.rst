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

.. |screenshot-pipeline| image:: https://raw.github.com/briglx/provision_analytics_workspaces/master/docs/Architecture.png

