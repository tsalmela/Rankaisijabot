"""
Tests for Docker container build and startup.

These tests verify that:
- The Docker image builds successfully
- The container starts without crashing
- All dependencies are installed correctly
- The bot module can be imported
- Configuration files are present
"""

import pytest
import docker
import time
import os
import platform


def print_docker_instructions():
    """Print helpful instructions for starting Docker based on the OS."""
    system = platform.system()

    message = """
╔════════════════════════════════════════════════════════════════════════════╗
║                        DOCKER IS NOT RUNNING                               ║
╚════════════════════════════════════════════════════════════════════════════╝

WHY IS DOCKER REQUIRED?
-----------------------
These tests verify that the Rankaisijabot can be built and run as a Docker
container. Docker must be installed and running on your system to execute
these tests.

The tests will:
  • Build a Docker image from the Dockerfile
  • Create and run test containers
  • Verify dependencies and configuration
  • Automatically clean up after testing

HOW TO START DOCKER:
--------------------
"""

    if system == "Windows":
        message += """
🪟 WINDOWS:
  1. Open Docker Desktop application from the Start menu
  2. Wait for the Docker icon in system tray to show "Docker Desktop is running"
  3. Verify by running in a terminal: docker ps

  If Docker Desktop is not installed:
  • Download from: https://docs.docker.com/desktop/install/windows-install/
  • Install and restart your computer
  • Start Docker Desktop
"""
    elif system == "Darwin":  # macOS
        message += """
🍎 macOS:
  1. Open Docker Desktop from Applications folder (or Spotlight: Cmd+Space, type "Docker")
  2. Wait for the Docker icon in menu bar to show "Docker Desktop is running"
  3. Verify by running in terminal: docker ps

  If Docker Desktop is not installed:
  • Download from: https://docs.docker.com/desktop/install/mac-install/
  • Install Docker.dmg
  • Start Docker Desktop
"""
    else:  # Linux
        message += """
🐧 LINUX:
  Start the Docker service:

  • Using systemd:
    sudo systemctl start docker
    sudo systemctl enable docker  # Enable on boot

  • Verify it's running:
    sudo systemctl status docker
    docker ps

  If Docker is not installed:
  • Ubuntu/Debian:
    sudo apt-get update
    sudo apt-get install docker.io

  • Fedora/RHEL:
    sudo dnf install docker

  • Add your user to docker group (to avoid needing sudo):
    sudo usermod -aG docker $USER
    # Log out and back in for this to take effect

  • For detailed installation: https://docs.docker.com/engine/install/
"""

    message += """
AFTER STARTING DOCKER:
----------------------
Run the tests again:
  pytest tests/test_docker_container.py -v

Or run all tests:
  pytest -v

════════════════════════════════════════════════════════════════════════════
"""

    print(message)


@pytest.fixture(scope="module")
def docker_client():
    """Fixture to provide Docker client with helpful error messages."""
    try:
        client = docker.from_env()
        # Verify Docker is accessible
        client.ping()
        print("✓ Docker is running and accessible")
        return client
    except docker.errors.DockerException as e:
        # Print helpful instructions
        print_docker_instructions()

        # Skip tests with a clear message
        pytest.skip(
            f"Docker is not running. See the instructions above to start Docker. "
            f"Error details: {e}"
        )


@pytest.fixture(scope="module")
def built_image(docker_client):
    """Build the Docker image for testing."""
    print("\nBuilding Docker image for testing...")

    # Get the project root directory (parent of tests directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        image, build_logs = docker_client.images.build(
            path=project_root,
            tag="rankaisijabot:test",
            buildargs={"bot_token_arg": "test_token_dummy"},
            rm=True,
            forcerm=True
        )

        # Print build logs for debugging
        for log in build_logs:
            if 'stream' in log:
                print(log['stream'].strip())

        print(f"✓ Image built successfully: {image.id[:12]}")
        yield image

    finally:
        # Cleanup after all tests
        print("\nCleaning up test image...")
        try:
            docker_client.images.remove("rankaisijabot:test", force=True)
            print("✓ Test image removed")
        except docker.errors.ImageNotFound:
            pass
        except Exception as e:
            print(f"Warning: Could not remove test image: {e}")


def test_docker_image_builds_successfully(built_image):
    """Test that the Docker image builds without errors."""
    assert built_image is not None
    assert len(built_image.tags) > 0
    assert any("rankaisijabot:test" in tag for tag in built_image.tags)


def test_python_version_correct(docker_client, built_image):
    """Test that the correct Python version is installed."""
    container = docker_client.containers.run(
        built_image.id,
        command=["--version"],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False  # Don't auto-remove so we can get logs
    )

    try:
        # Wait for container to finish
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "Python 3.9" in logs
        print(f"✓ Python version: {logs.strip()}")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_bot_dependencies_installed(docker_client, built_image):
    """Test that all required Python packages are installed."""
    test_imports = [
        "import discord",
        "import yaml",
        "import yfinance",
        "import aiohttp",
        "print('All dependencies OK')"
    ]

    container = docker_client.containers.run(
        built_image.id,
        command=["-c", "; ".join(test_imports)],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "All dependencies OK" in logs
        print("✓ All dependencies installed correctly")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_bot_module_imports(docker_client, built_image):
    """Test that the bot module can be imported without errors."""
    container = docker_client.containers.run(
        built_image.id,
        command=["-c", "from bot.rankaisija import Rankaisija; print('Bot module OK')"],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "Bot module OK" in logs
        print("✓ Bot module imports successfully")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_config_file_exists(docker_client, built_image):
    """Test that config.yml is copied to the container."""
    container = docker_client.containers.run(
        built_image.id,
        command=[
            "-c",
            "import os; assert os.path.exists('/bot/config.yml'), 'Config not found'; print('Config OK')"
        ],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "Config OK" in logs
        print("✓ Config file present in container")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_all_cogs_loadable(docker_client, built_image):
    """Test that all cogs defined in config can be loaded."""
    test_code = """
import os
import yaml

# Register the !ENV constructor to handle environment variables in YAML
def _env_var_constructor(loader, node):
    default = None
    if node.id == "scalar":
        value = loader.construct_scalar(node)
        key = str(value)
    else:
        value = loader.construct_sequence(node)
        if len(value) >= 2:
            default = value[1]
            key = value[0]
        else:
            key = value[0]
    return os.getenv(key, default)

yaml.SafeLoader.add_constructor("!ENV", _env_var_constructor)

with open('/bot/config.yml') as f:
    config = yaml.safe_load(f)
    cogs = config['cogs']['cogs']
    print(f'Found {len(cogs)} cogs to test')
    for cog in cogs:
        try:
            exec(f'from bot.cogs.{cog} import setup')
            print(f'✓ Cog {cog} loadable')
        except Exception as e:
            print(f'✗ Cog {cog} failed: {e}')
            raise
print('All cogs OK')
"""

    container = docker_client.containers.run(
        built_image.id,
        command=["-c", test_code],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=15)
        logs = container.logs().decode('utf-8')
        print(f"\n{logs}")
        assert "All cogs OK" in logs
        print("✓ All cogs are loadable")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_workdir_is_correct(docker_client, built_image):
    """Test that the working directory is set correctly."""
    container = docker_client.containers.run(
        built_image.id,
        command=["-c", "import os; print(os.getcwd())"],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8').strip()
        assert logs == "/bot"
        print(f"✓ Working directory: {logs}")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_bot_token_env_var(docker_client, built_image):
    """Test that BOT_TOKEN environment variable is accessible."""
    container = docker_client.containers.run(
        built_image.id,
        command=[
            "-c",
            "import os; token = os.getenv('BOT_TOKEN'); "
            "assert token == 'test_token_123', f'Token is {token}'; "
            "print('Token env var OK')"
        ],
        environment={"BOT_TOKEN": "test_token_123"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "Token env var OK" in logs
        print("✓ BOT_TOKEN environment variable accessible")
    finally:
        try:
            container.remove(force=True)
        except:
            pass


def test_container_starts_without_immediate_crash(docker_client, built_image):
    """
    Test that container doesn't crash immediately.
    Note: The bot will fail to connect without a valid token,
    but it should at least start and attempt to run.
    """
    container = docker_client.containers.run(
        built_image.id,
        command=["-c", "import bot; print('Import successful')"],
        environment={"BOT_TOKEN": "test_token"},
        detach=True,
        remove=False
    )

    try:
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        assert "Import successful" in logs
        print("✓ Container starts without immediate crash")
    finally:
        try:
            container.remove(force=True)
        except:
            pass
