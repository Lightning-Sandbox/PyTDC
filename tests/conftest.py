"""
Pytest configuration and fixtures for optimized test execution.
"""
import os
import platform
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_platform_optimizations():
    """
    Configure platform-specific optimizations for test execution.
    This fixture runs once per test session before any tests.
    """
    if platform.system() == 'Darwin':  # macOS
        # Optimize TileDB S3 operations for macOS
        os.environ.setdefault('TILEDB_VFS_S3_MAX_PARALLEL_OPS', '16')
        os.environ.setdefault('TILEDB_VFS_S3_MULTIPART_PART_SIZE', '52428800')  # 50MB
        os.environ.setdefault('TILEDB_VFS_S3_REGION', 'us-west-2')
        os.environ.setdefault('TILEDB_VFS_S3_USE_VIRTUAL_ADDRESSING', 'true')
        
        # Optimize NumPy/BLAS threading for macOS
        os.environ.setdefault('OMP_NUM_THREADS', '4')
        os.environ.setdefault('OPENBLAS_NUM_THREADS', '4')
        os.environ.setdefault('MKL_NUM_THREADS', '4')
        os.environ.setdefault('VECLIB_MAXIMUM_THREADS', '4')
        os.environ.setdefault('NUMEXPR_NUM_THREADS', '4')
        
        # Optimize for Apple Silicon if available
        if platform.machine() == 'arm64':
            os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')


def pytest_configure(config):
    """
    Configure pytest with additional markers and settings.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
