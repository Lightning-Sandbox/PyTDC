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

    With pytest-xdist, session-scoped fixtures run once per worker process,
    but since all workers share the same working directory, we need to be
    careful about race conditions. The --dist=loadfile strategy helps by
    grouping tests by file to the same worker.
    """
    # Get the root directory where tests are run from
    root_dir = os.getcwd()

    # Clean up before tests start
    for directory in ["data", "oracle"]:
        dir_path = os.path.join(root_dir, directory)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
            except FileNotFoundError:
                # Directory was removed by another worker between check and removal
                # This is okay, we just want to ensure it's clean
                pass

    # Let tests run
    yield

    # Optional: Clean up after tests complete
    # Commented out to allow inspection of test artifacts
    # for directory in ["data", "oracle"]:
    #     dir_path = os.path.join(root_dir, directory)
    #     if os.path.exists(dir_path):
    #         try:
    #             shutil.rmtree(dir_path)
    #         except FileNotFoundError:
    #             pass
