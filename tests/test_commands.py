"""
Command smoke tests for Rankaisijabot.

Tests that verify each command can execute without errors using mocked Discord context.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import importlib


class MockContext:
    """Mock Discord context for testing commands."""

    def __init__(self):
        self.send = AsyncMock()
        self.author = MagicMock()
        self.author.name = "TestUser"
        self.author.id = 12345
        self.channel = MagicMock()
        self.guild = MagicMock()
        self.message = MagicMock()


class MockBot:
    """Mock Discord bot for testing cogs."""

    def __init__(self):
        self.user = MagicMock()
        self.add_cog = AsyncMock()


def load_cog_class(cog_name):
    """Dynamically load a cog class by name."""
    module_path = f"bot.cogs.{cog_name}"
    try:
        module = importlib.import_module(module_path)
        # Find the Cog class in the module (usually named after the file with capitalization)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, '__mro__'):
                # Check if it's a commands.Cog subclass
                if any('Cog' in str(base) for base in attr.__mro__):
                    return attr
        raise AttributeError(f"No Cog class found in {module_path}")
    except ImportError as e:
        pytest.skip(f"Could not import cog {cog_name}: {e}")


class TestGeneralCog:
    """Tests for general.py cog commands."""

    @pytest.mark.asyncio
    async def test_info_command(self):
        """Test that info command sends embed with rankaisija.jpg thumbnail."""
        Cog = load_cog_class("general")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file, patch("discord.Embed") as mock_embed:
            await cog.info(cog, ctx)

            # Verify discord.File was called with rankaisija.jpg
            mock_file.assert_called_once_with("images/rankaisija.jpg", filename="rankaisija.jpg")

            # Verify embed was created
            mock_embed.assert_called_once()

            # Verify send was called
            ctx.send.assert_called_once()


class TestDotaCog:
    """Tests for dota.py cog commands."""

    @pytest.mark.asyncio
    async def test_ukkoja_command(self):
        """Test that ukkoja command sends the correct image file."""
        Cog = load_cog_class("dota")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.ukkoja(cog, ctx)

            # Verify discord.File was called with correct image
            mock_file.assert_called_once_with("images/dota_ukkoja.png")
            ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_ei_command(self):
        """Test that ei command sends the correct image file."""
        Cog = load_cog_class("dota")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.ei(cog, ctx)

            mock_file.assert_called_once_with("images/ei.png")
            ctx.send.assert_called_once()


class TestGhostCog:
    """Tests for ghost.py cog commands."""

    @pytest.mark.asyncio
    async def test_ghost_command(self):
        """Test that ghost command sends the correct image file."""
        Cog = load_cog_class("ghost")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.ghost(cog, ctx)

            mock_file.assert_called_once_with("images/ghost_tampere.jpg")
            # Command sends image first, then a message about the event date
            assert ctx.send.call_count == 2


class TestMiscCog:
    """Tests for misc.py cog commands."""

    @pytest.mark.asyncio
    async def test_rakyta_command(self):
        """Test that rakyta command sends the correct image file."""
        Cog = load_cog_class("misc")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.rakyta(cog, ctx)

            mock_file.assert_called_once_with("images/rakyta.jpg")
            ctx.send.assert_called_once()


class TestMiscGamesCog:
    """Tests for misc_games.py cog commands."""

    @pytest.mark.asyncio
    async def test_ror_command(self):
        """Test that ror command sends the correct image file."""
        Cog = load_cog_class("misc_games")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.ror(cog, ctx)

            mock_file.assert_called_once_with("images/ror.png")
            ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_hon_command(self):
        """Test that hon command sends the correct image file."""
        Cog = load_cog_class("misc_games")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.hon(cog, ctx)

            mock_file.assert_called_once_with("images/hon.png")
            ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_eft_command(self):
        """Test that eft command sends the correct image file."""
        Cog = load_cog_class("misc_games")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.eft(cog, ctx)

            mock_file.assert_called_once_with("images/eft.png")
            ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_darktide_command(self):
        """Test that darktide command sends the correct image file."""
        Cog = load_cog_class("misc_games")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.darktide(cog, ctx)

            mock_file.assert_called_once_with("images/darktide.png")
            ctx.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_fellowship_command(self):
        """Test that fellowship command sends the correct image file."""
        Cog = load_cog_class("misc_games")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        with patch("discord.File") as mock_file:
            await cog.fellowship(cog, ctx)

            mock_file.assert_called_once_with("images/fellowship.png")
            ctx.send.assert_called_once()


class TestHelloCog:
    """Tests for hello.py cog commands."""

    @pytest.mark.asyncio
    async def test_hello_command(self):
        """Test that hello command executes without errors."""
        Cog = load_cog_class("hello")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        await cog.hello(cog, ctx)

        # Verify send was called
        ctx.send.assert_called_once()


class TestRollerCog:
    """Tests for roller.py cog commands."""

    @pytest.mark.asyncio
    async def test_roll_command_no_args(self):
        """Test that roll command works without arguments."""
        Cog = load_cog_class("roller")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        await cog.dice(cog, ctx)

        # Verify send was called
        ctx.send.assert_called()

    @pytest.mark.asyncio
    async def test_roll_command_with_dice(self):
        """Test that roll command works with dice notation."""
        Cog = load_cog_class("roller")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        await cog.dice(cog, ctx, roll_string="2d6")

        # Verify send was called
        ctx.send.assert_called()

    @pytest.mark.asyncio
    async def test_number_command(self):
        """Test that number command executes without errors."""
        Cog = load_cog_class("roller")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        # Test with a specific range
        await cog.roll(cog, ctx, rollRangeEnd=100)

        # Verify send was called
        ctx.send.assert_called()


class TestRankaisumethoditCog:
    """Tests for rankaisumetodit.py cog commands."""

    @pytest.mark.asyncio
    async def test_metodi_command(self):
        """Test that metodi command executes without errors."""
        Cog = load_cog_class("rankaisumetodit")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        await cog.rankaise(cog, ctx)

        # Verify send was called
        ctx.send.assert_called_once()


class TestStockCog:
    """Tests for stock.py cog commands."""

    @pytest.mark.asyncio
    async def test_price_command_no_args(self):
        """Test that price command handles missing arguments gracefully."""
        Cog = load_cog_class("stock")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        # Should send an error message about missing stock argument
        await cog.price(cog, ctx)
        ctx.send.assert_called()

    @pytest.mark.asyncio
    async def test_price_command_with_ticker(self):
        """Test that price command works with a ticker symbol."""
        Cog = load_cog_class("stock")
        bot = MockBot()
        cog = Cog(bot)
        ctx = MockContext()

        # Mock the yfinance API call
        with patch("yfinance.Ticker") as mock_ticker:
            mock_info = {
                "shortName": "Test Stock",
                "symbol": "TEST",
                "ask": 100.0,
                "bid": 99.5,
                "currency": "USD"
            }
            mock_ticker.return_value.info = mock_info

            await cog.price(cog, ctx, stock="TEST")

            # Verify send was called
            ctx.send.assert_called()
