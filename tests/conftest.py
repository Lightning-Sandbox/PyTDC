# -*- coding: utf-8 -*-
"""
Pytest configuration and fixtures for TDC tests.

This conftest.py ensures shared directories are cleaned before test execution
to prevent race conditions and shared state issues in parallel testing.
"""

import os
import shutil

import pytest


@pytest.fixture(scope="session", autouse=True)
def cleanup_shared_directories():
    """
    Clean up shared ./data and ./oracle directories before test session starts.
    
    This fixture runs automatically before any tests to ensure a clean state,
    preventing race conditions when tests run in parallel with pytest-xdist.
    """
    # Clean up before tests start
    for directory in ["data", "oracle"]:
        dir_path = os.path.join(os.getcwd(), directory)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    # Let tests run
    yield
    
    # Optional: Clean up after tests complete
    # Commented out to allow inspection of test artifacts
    # for directory in ["data", "oracle"]:
    #     dir_path = os.path.join(os.getcwd(), directory)
    #     if os.path.exists(dir_path):
    #         shutil.rmtree(dir_path)
