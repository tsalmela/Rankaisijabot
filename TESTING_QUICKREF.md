# Testing Quick Reference

## Installation
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run Tests

### Simple Commands
```bash
# All tests
pytest

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Using run_tests.py
```bash
# All tests
python run_tests.py

# Resource validation only
python run_tests.py --resources

# Command tests only
python run_tests.py --commands

# With coverage
python run_tests.py --coverage

# Image usage report
python run_tests.py --report
```

### Specific Tests
```bash
# One file
pytest tests/test_resources.py

# One class
pytest tests/test_commands.py::TestMiscGamesCog

# One test
pytest tests/test_commands.py::TestMiscGamesCog::test_ror_command
```

## Coverage
```bash
# Terminal report
pytest --cov=bot --cov-report=term

# HTML report (opens in browser)
pytest --cov=bot --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

## What Each Test Does

### Resource Tests (`test_resources.py`)
- ✅ Checks all images exist and are used
- ✅ Checks all cogs can be imported
- ✅ Validates file structure
- 📊 Shows image-to-cog mapping

### Command Tests (`test_commands.py`)
- ✅ Tests each command runs without errors
- ✅ Verifies correct images are sent
- ✅ Uses mocked Discord (no real bot needed)

## Common Scenarios

### Before Committing
```bash
pytest -v
```

### Adding New Image Command
1. Add image to `/images`
2. Add command to cog
3. Run: `python run_tests.py --report`
4. Add test to `tests/test_commands.py`
5. Run: `pytest -v`

### Finding Unused Images
```bash
python run_tests.py --report
```

### Checking Coverage
```bash
python run_tests.py --coverage
```

## Test Files
- `tests/test_resources.py` - Image & import validation
- `tests/test_commands.py` - Command execution tests
- `pytest.ini` - Pytest configuration
- `.github/workflows/tests.yml` - CI/CD config

## Documentation
- `README_TESTING.md` - Full testing guide
- `TESTING_SUMMARY.md` - Overview of test suite
- `TESTING_QUICKREF.md` - This file

## Troubleshooting

### Tests Won't Run
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Check Python version (need 3.8+)
python --version
```

### Import Errors
```bash
# Run from project root
cd /path/to/Rankaisijabot
pytest
```

### AsyncIO Errors
```bash
pip install --upgrade pytest-asyncio
```

## CI/CD
- Tests run automatically on push to main
- Tests run on all pull requests
- Tested on Python 3.8, 3.9, 3.10, 3.11
- See `.github/workflows/tests.yml`
