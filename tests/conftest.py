"""
Pytest configuration and fixtures for optimized test execution.

macOS Performance Optimization:
- Tests on macOS run ~3x slower than Linux (36min vs 13min)
- Primary bottleneck: testGeneformerTokenizer (17.5min macOS vs 4min Ubuntu)
- Root cause: TileDB SOMA network I/O inefficiency when querying CellxGene Census

This configuration applies optimizations when running tests locally on macOS.
In CI, these same settings are configured via environment variables in the workflow file.
"""
import os
import platform
import pytest

# Configuration constants for macOS optimization
MACOS_THREAD_LIMIT = 4  # Limit threads to prevent over-subscription on macOS
TILEDB_S3_MAX_PARALLEL_OPS = '16'  # Increase concurrent S3 operations
TILEDB_S3_MULTIPART_PART_SIZE = '52428800'  # 50MB chunks for efficient transfers
TILEDB_S3_REGION = 'us-west-2'  # Explicit region for CellxGene data


@pytest.fixture(scope="session", autouse=True)
def configure_platform_optimizations():
    """
    Configure platform-specific optimizations for test execution.
    This fixture runs once per test session before any tests.
    Uses setdefault to avoid overriding CI-configured environment variables.
    """
    if platform.system() == 'Darwin':  # macOS
        # TileDB S3 Configuration: Optimize network operations for macOS
        os.environ.setdefault('TILEDB_VFS_S3_MAX_PARALLEL_OPS',
                              TILEDB_S3_MAX_PARALLEL_OPS)
        os.environ.setdefault('TILEDB_VFS_S3_MULTIPART_PART_SIZE',
                              TILEDB_S3_MULTIPART_PART_SIZE)
        os.environ.setdefault('TILEDB_VFS_S3_REGION', TILEDB_S3_REGION)
        os.environ.setdefault('TILEDB_VFS_S3_USE_VIRTUAL_ADDRESSING', 'true')

        # NumPy/BLAS Threading: Prevent over-subscription on macOS scheduler
        thread_limit = str(MACOS_THREAD_LIMIT)
        os.environ.setdefault('OMP_NUM_THREADS', thread_limit)
        os.environ.setdefault('OPENBLAS_NUM_THREADS', thread_limit)
        os.environ.setdefault('MKL_NUM_THREADS', thread_limit)
        os.environ.setdefault('VECLIB_MAXIMUM_THREADS', thread_limit)
        os.environ.setdefault('NUMEXPR_NUM_THREADS', thread_limit)

        # Apple Silicon specific optimization
        if platform.machine() == 'arm64':
            os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')


def pytest_configure(config):
    """
    Configure pytest with additional markers and settings.
    """
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')")
