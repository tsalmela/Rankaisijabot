# Docker Container Testing Guide

This guide explains how to test the Rankaisijabot Docker container.

## Prerequisites

1. **Docker must be installed and running** on your system
   - The tests will automatically check if Docker is running
   - If Docker is not running, you'll see helpful instructions on how to start it
2. **Python development dependencies** must be installed:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Running Docker Container Tests

### Run all Docker tests

```bash
pytest tests/test_docker_container.py -v
```

### Run a specific test

```bash
pytest tests/test_docker_container.py::test_docker_image_builds_successfully -v
```

### Run with detailed output

```bash
pytest tests/test_docker_container.py -v -s
```

The `-s` flag shows print statements, which is useful for seeing build progress and test details.

## What the Tests Verify

The Docker container tests verify that:

1. **Image builds successfully** - The Dockerfile creates a valid image
2. **Python version is correct** - Python 3.9 is installed
3. **Dependencies are installed** - All required packages (discord.py, pyyaml, yfinance, etc.) are present
4. **Bot module imports** - The bot code can be imported without errors
5. **Config file exists** - The config.yml file is copied to the container
6. **All cogs are loadable** - Each cog defined in config.yml can be loaded
7. **Working directory is correct** - Container uses /bot as working directory
8. **Environment variables work** - BOT_TOKEN can be passed and accessed
9. **Container starts without crashing** - The container runs without immediate errors

## Test Output

Successful test output will look like:

```
tests/test_docker_container.py::test_docker_image_builds_successfully PASSED
tests/test_docker_container.py::test_python_version_correct PASSED
tests/test_docker_container.py::test_bot_dependencies_installed PASSED
tests/test_docker_container.py::test_bot_module_imports PASSED
tests/test_docker_container.py::test_config_file_exists PASSED
tests/test_docker_container.py::test_all_cogs_loadable PASSED
tests/test_docker_container.py::test_workdir_is_correct PASSED
tests/test_docker_container.py::test_bot_token_env_var PASSED
tests/test_docker_container.py::test_container_starts_without_immediate_crash PASSED
```

## Troubleshooting

### Docker daemon not running

If Docker is not running, the tests will automatically display platform-specific instructions:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                        DOCKER IS NOT RUNNING                               ║
╚════════════════════════════════════════════════════════════════════════════╝

WHY IS DOCKER REQUIRED?
-----------------------
These tests verify that the Rankaisijabot can be built and run as a Docker
container...

HOW TO START DOCKER:
--------------------
[Platform-specific instructions will be shown here]
```

The instructions are automatically tailored to your operating system (Windows, macOS, or Linux).

### Permission errors

On Linux, you may need to run Docker commands with sudo or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
Then log out and log back in.

### Image build failures

If the image fails to build:
1. Check that all files exist (config.yml, requirements.txt, etc.)
2. Verify your Dockerfile syntax
3. Make sure you have internet connectivity (for downloading packages)
4. Check the build logs in the test output for specific errors

### Tests are slow

The first run will be slower as it builds the Docker image. Subsequent runs use cached layers and are faster. The test suite automatically cleans up the test image after completion.

## Integration with CI/CD

These tests can be integrated into GitHub Actions or other CI/CD systems. Example workflow:

```yaml
name: Docker Tests

on: [push, pull_request]

jobs:
  docker-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run Docker container tests
        run: pytest tests/test_docker_container.py -v
```

## Manual Testing

You can also manually test the container:

```bash
# Build the image
docker build -t rankaisijabot:manual-test --build-arg bot_token_arg=your_token .

# Run the container
docker run -e BOT_TOKEN=your_actual_token rankaisijabot:manual-test

# Test with a simple command
docker run --rm -e BOT_TOKEN=test rankaisijabot:manual-test python3 -c "import bot; print('OK')"
```
