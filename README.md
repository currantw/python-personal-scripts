# Python Personal Scripts

Personal Python scripts and utilities.

## Setup

```bash
# Install dependencies
make install-dev

# Run code quality checks
make check-all

# Fix formatting and linting issues
make fix-all

# Run tests (lib/ directory only)
make test-cov
```

## Structure

- `lib/` - Shared library modules (tested with 100% coverage)
- `scripts/` - Executable scripts (not tested)
- `tests/` - Test files for lib/ modules
