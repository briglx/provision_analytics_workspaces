#!/usr/bin/python
"""Main script for provision analytics workspaces."""
import logging

_LOGGER = logging.getLogger(__name__)

def configure_logger():
    """Configure logger"""
    _LOGGER.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)

if __name__ == "__main__":
    configure_logger()
    _LOGGER.info("starting")

    print("hello world")

    _LOGGER.info("done")
