"""
Pytest configuration and fixtures for optimized test execution.
"""
import pytest


def pytest_configure(config):
    """
    Configure pytest with additional markers and settings.
    """
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')")
