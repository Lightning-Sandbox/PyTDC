"""
Pytest configuration and fixtures for optimized test execution.
"""
import os
import platform

# Configuration constants for macOS optimization
MACOS_THREAD_LIMIT = 4
TILEDB_S3_MAX_PARALLEL_OPS = '16'
TILEDB_S3_MULTIPART_PART_SIZE = '52428800'  # 50MB
TILEDB_S3_REGION = 'us-west-2'

# Apply macOS optimizations at module import time (before test collection)
# This ensures environment variables are set before test modules import
# numpy/torch/tiledb, which initialize BLAS thread pools and TileDB config
if platform.system() == 'Darwin':  # macOS
    # Optimize TileDB S3 operations for macOS
    os.environ.setdefault('TILEDB_VFS_S3_MAX_PARALLEL_OPS',
                          TILEDB_S3_MAX_PARALLEL_OPS)
    os.environ.setdefault('TILEDB_VFS_S3_MULTIPART_PART_SIZE',
                          TILEDB_S3_MULTIPART_PART_SIZE)
    os.environ.setdefault('TILEDB_VFS_S3_REGION', TILEDB_S3_REGION)
    os.environ.setdefault('TILEDB_VFS_S3_USE_VIRTUAL_ADDRESSING', 'true')

    # Optimize NumPy/BLAS threading for macOS
    thread_limit = str(MACOS_THREAD_LIMIT)
    os.environ.setdefault('OMP_NUM_THREADS', thread_limit)
    os.environ.setdefault('OPENBLAS_NUM_THREADS', thread_limit)
    os.environ.setdefault('MKL_NUM_THREADS', thread_limit)
    os.environ.setdefault('VECLIB_MAXIMUM_THREADS', thread_limit)
    os.environ.setdefault('NUMEXPR_NUM_THREADS', thread_limit)

    # Optimize for Apple Silicon if available
    if platform.machine() == 'arm64':
        os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')
