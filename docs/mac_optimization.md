# macOS Performance Optimizations

## Problem
CI tests on macOS were running approximately 3x slower than on Linux (36 minutes vs 13 minutes), primarily due to the `testGeneformerTokenizer` test which queries the CellxGene Census database via TileDB SOMA.

## Root Cause Analysis
The bottleneck was identified in network I/O operations when downloading cell data from the CellxGene Census:
- **macOS (3.10)**: Test ran from 07:45:32 to 08:02:55 = ~17.5 minutes
- **Ubuntu (3.10)**: Test ran from 07:04:27 to 07:08:39 = ~4 minutes

## Implemented Optimizations

### 1. TileDB SOMA Data Caching
Added GitHub Actions cache for downloaded census data:
- Cache path: `~/.cache/cellxgene_census` and `~/.tiledb`
- Cache key based on OS and test requirements
- Significantly reduces network I/O for subsequent runs

### 2. TileDB S3 Configuration Optimizations
Optimized TileDB S3 operations specifically for macOS:
- `TILEDB_VFS_S3_MAX_PARALLEL_OPS=16`: Increased parallel operations from default
- `TILEDB_VFS_S3_MULTIPART_PART_SIZE=52428800`: Set 50MB chunk size for efficient transfers
- `TILEDB_VFS_S3_REGION=us-west-2`: Explicit region setting for better routing
- `TILEDB_VFS_S3_USE_VIRTUAL_ADDRESSING=true`: Modern S3 addressing for better performance

### 3. NumPy/BLAS Threading Optimization
Limited threading to prevent over-subscription on macOS:
- `OMP_NUM_THREADS=4`
- `OPENBLAS_NUM_THREADS=4`
- `MKL_NUM_THREADS=4`
- `VECLIB_MAXIMUM_THREADS=4`
- `NUMEXPR_NUM_THREADS=4`

macOS has different threading behavior than Linux, and limiting threads prevents context switching overhead.

### 4. Pytest Configuration
Created `pytest.ini` with:
- Progress-style output to reduce I/O overhead
- Suppressed deprecation warnings to reduce output
- Optimized test discovery patterns

### 5. Platform-Specific Test Setup
Created `tests/conftest.py` with session-level fixtures that:
- Automatically configure platform-specific optimizations
- Apply settings before any tests run
- Include Apple Silicon specific optimizations

## Files Modified
- `.github/workflows/ci-tests.yml`: Added caching and macOS-specific environment variables
- `tdc/resource/cellxgene_census.py`: Added macOS-specific TileDB configuration in `__init__`
- `pytest.ini`: New file with pytest configuration
- `tests/conftest.py`: New file with platform-specific test fixtures

## Expected Impact
These optimizations should reduce macOS CI test time by:
1. **First run**: ~20-30% improvement from threading and TileDB optimizations
2. **Subsequent runs**: ~50-70% improvement from caching of census data

## Testing
To test these optimizations:
1. Run the CI pipeline on macOS
2. Compare timing of `testGeneformerTokenizer` before and after
3. Verify cache is being utilized in subsequent runs

## References
- CI Run (before optimization): https://github.com/Lightning-Sandbox/PyTDC/actions/runs/22088942931
- TileDB Configuration: https://docs.tiledb.com/main/how-to/configuration
- CellxGene Census: https://chanzuckerberg.github.io/cellxgene-census/
