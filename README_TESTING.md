# Testing Guide for Rankaisijabot

This document explains how to run tests for the Rankaisijabot Discord bot.

## Test Structure

The test suite is organized into two main categories:

### 1. Resource Validation Tests (`test_resources.py`)
These tests verify the integrity of bot resources:
- ✅ All images referenced in cogs exist
- ✅ All images in `/images` folder are used (no orphaned files)
- ✅ All cogs can be imported without errors
- ✅ Image files have valid formats (png, jpg, jpeg, gif, webp)
- ✅ All cogs have required `async def setup()` function

### 2. Command Smoke Tests (`test_commands.py`)
These tests verify that commands execute without errors:
- ✅ Each command can be invoked with mocked Discord context
- ✅ Commands send expected responses
- ✅ Image commands reference correct files
- ✅ Commands with parameters work correctly

## Installation

### Install Production Dependencies
```bash
pip install -r requirements.txt
```

### Install Development/Testing Dependencies
```bash
pip install -r requirements-dev.txt
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
# Resource validation only
pytest tests/test_resources.py

# Command tests only
pytest tests/test_commands.py
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=bot --cov-report=term
```

### Run and Show Image Usage Report
```bash
pytest tests/test_resources.py::TestImageReferenceCoverage::test_print_image_usage_report -v -s
```

### Run Specific Test Class or Function
```bash
# Run all tests in a specific class
pytest tests/test_commands.py::TestMiscGamesCog

# Run a specific test function
pytest tests/test_commands.py::TestMiscGamesCog::test_ror_command
```

## Understanding Test Output

### Resource Validation Tests
If these tests fail, it usually means:
- **Unused images**: You have image files that aren't referenced in any cog
- **Broken references**: A cog references an image that doesn't exist
- **Import errors**: A cog file has syntax errors or missing dependencies

### Command Smoke Tests
If these tests fail, it usually means:
- **Command execution error**: The command logic has a bug
- **Missing mock**: The test needs additional mocking for external dependencies
- **API changes**: Discord.py API might have changed

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Push to `main`/`master` branch
- Pull requests to `main`/`master` branch
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)

See `.github/workflows/tests.yml` for CI configuration.

## Adding New Tests

### When Adding a New Command:
1. Add the image file to `/images` directory
2. Add the command to a cog in `/bot/cogs`
3. Add a test function in `tests/test_commands.py`

Example:
```python
@pytest.mark.asyncio
async def test_new_command(self):
    """Test that new command sends the correct image file."""
    Cog = load_cog_class("misc_games")
    bot = MockBot()
    cog = Cog(bot)
    ctx = MockContext()

    with patch("discord.File") as mock_file:
        await cog.new_command(cog, ctx)

        mock_file.assert_called_once_with("images/new_image.png")
        ctx.send.assert_called_once()
```

### When Adding a New Cog:
1. Create the cog file in `/bot/cogs`
2. Ensure it has `async def setup(bot)` function
3. Add test class in `tests/test_commands.py`

## Troubleshooting

### Import Errors
If you get import errors when running tests:
```bash
# Make sure you're in the project root directory
cd /path/to/Rankaisijabot

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### AsyncIO Errors
If you get asyncio-related errors:
```bash
# Make sure pytest-asyncio is installed
pip install pytest-asyncio>=0.21.0
```

### Mock Errors
If Discord mocking fails:
```bash
# Ensure you have the correct discord.py version
pip install "discord.py<=2.0"
```

## Test Coverage Goals

- **Resource Tests**: 100% coverage of all images and cogs
- **Command Tests**: At least one test per command
- **Overall Code Coverage**: Aim for >70% coverage of bot code

## Best Practices

1. **Keep tests fast**: Mock external dependencies (Discord API, yfinance, etc.)
2. **Test behavior, not implementation**: Focus on what commands do, not how
3. **Use descriptive test names**: Test name should explain what it verifies
4. **Keep tests independent**: Each test should work in isolation
5. **Update tests with code changes**: When you modify a command, update its tests

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [discord.py documentation](https://discordpy.readthedocs.io/)
