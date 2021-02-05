#!/usr/bin/python
"""Main script for provision analytics workspaces."""
import argparse
import logging
import os
import sys

from azure.storage.filedatalake import FileSystemClient

# pylint: disable=W0621

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def create_directories(connection_string, file_system_name):
    """Create File System Directories."""
    file_system = FileSystemClient.from_connection_string(
        connection_string, file_system_name=file_system_name
    )


def main(connection_string):
    """Provision analytics resources."""
    print(f"connection string: {connection_string}")

    if not connection_string:
        raise ValueError("Parameter connection_string is required.")


if __name__ == "__main__":
    logging.info("Starting script")

    parser = argparse.ArgumentParser(
        description="Provision Analytics Workspaces.",
        add_help=True,
    )
    parser.add_argument(
        "--connection_string",
        "-c",
        help="Storage Account Connection String",
    )

    args = parser.parse_args()

    connection_string = args.connection_string or os.environ.get(
        "STORAGE_CONNECTION_STRING"
    )

    main(connection_string)
