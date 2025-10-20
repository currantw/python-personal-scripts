# Python Personal Scripts

Python scripts and utilities for everyday tasks and automation.

## Setup

### Prerequisites

- Python 3.12+
- Virtual environment (recommended)

### Installation

1. Clone and navigate to the project:

```bash
git clone https://github.com/currantw/python-personal-scripts
cd python-personal-scripts
```

1. Set up a virtual environment:

**On macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

1. Install dependencies:

```bash
make install      # Production only
make install-dev  # With development tools
```

## Development

This project uses modern Python tooling for fast and consistent code quality
checks.

Code quality tools:

- **Ruff**: Fast code formatter, import sorter, and linter
- **mypy**: Type checker
- **markdownlint**: Markdown linter
- **pre-commit**: Git hooks

### Commands

```bash
# Checking (read-only)
make check-format # Check code formatting
make check-lint   # Check Python and Markdown linting
make check-type   # Run type checker
make check-all    # Run all checks

# Fixing (read/write)
make fix-format  # Format code with ruff
make fix-lint    # Run linters with auto-fix (Python + Markdown)
make fix-all     # Apply all auto-fixes (format + lint)

# Testing
make test        # Run tests (lib/ directory only)
make test-cov    # Run tests with coverage (lib/ directory only)

# Utilities
make all         # Run all checks and tests with coverage
make clean       # Clean cache files
make help        # See all commands
```

Pre-commit hooks run automatically on commit. To run manually:

```bash
make pre-commit
```

### Project Structure

- `lib/` - Shared library modules
- `scripts/` - Executable scripts
- `tests/` - Test files

### CI/CD

The project uses GitHub Actions for continuous integration. The workflow runs
the same commands as local development:

- **Code Quality**: `make check` (format check, linting, type checking)
- **Testing**: `make test-cov` (tests with coverage reporting)

This ensures consistency between local development and CI environments.

### Configuration Files

- `.gitignore`: Files and directories to ignore in version control
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `Makefile`: Convenient commands for development tasks
- `pyproject.toml`: Main configuration file for tools and project metadata
- `requirements-dev.txt`: Development dependencies
- `requirements.txt`: Production dependencies
