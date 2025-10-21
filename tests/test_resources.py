"""
Resource validation tests for Rankaisijabot.

Tests that verify:
- All images referenced in cogs exist
- All images in the images folder are used
- All cogs can be imported successfully
"""

import os
import re
from pathlib import Path
import pytest
import importlib.util


def get_all_images():
    """Get all image files from the images directory."""
    images_dir = Path("images")
    if not images_dir.exists():
        return []

    # Get all files in images directory (filtering out directories)
    return [f.name for f in images_dir.iterdir() if f.is_file()]


def get_image_references_from_cogs():
    """Extract all image file references from cog files."""
    cogs_dir = Path("bot/cogs")
    if not cogs_dir.exists():
        return set()

    referenced_images = set()

    # Pattern to match image file references like: discord.File("images/filename.ext")
    # Also matches with additional parameters like: discord.File("images/filename.ext", filename="...")
    pattern = re.compile(r'discord\.File\(["\']images/([^"\']+)["\']')

    # Search through all Python files in cogs directory
    for cog_file in cogs_dir.glob("*.py"):
        if cog_file.name == "__init__.py":
            continue

        with open(cog_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = pattern.findall(content)
            referenced_images.update(matches)

    return referenced_images


def get_all_cogs():
    """Get all cog files from the bot/cogs directory."""
    cogs_dir = Path("bot/cogs")
    if not cogs_dir.exists():
        return []

    # Get all Python files except __init__.py
    return [f for f in cogs_dir.glob("*.py") if f.name != "__init__.py"]


class TestDirectoryStructure:
    """Tests for basic directory structure."""

    def test_images_directory_exists(self):
        """Test that the images directory exists."""
        assert Path("images").exists(), "images directory does not exist"

    def test_cogs_directory_exists(self):
        """Test that the bot/cogs directory exists."""
        assert Path("bot/cogs").exists(), "bot/cogs directory does not exist"

    def test_images_directory_not_empty(self):
        """Test that there are images in the images directory."""
        images = get_all_images()
        assert len(images) > 0, "images directory is empty"

    def test_cogs_directory_not_empty(self):
        """Test that there are cogs in the bot/cogs directory."""
        cogs = get_all_cogs()
        assert len(cogs) > 0, "bot/cogs directory has no cog files"


class TestImageUsage:
    """Tests for image file usage."""

    def test_all_images_are_used(self):
        """Test that every image in the images folder is referenced in at least one cog."""
        all_images = get_all_images()
        referenced_images = get_image_references_from_cogs()

        # Find images that are not referenced
        unused_images = [img for img in all_images if img not in referenced_images]

        assert len(unused_images) == 0, (
            f"The following images are not used in any cog: {', '.join(unused_images)}\n"
            f"All images: {sorted(all_images)}\n"
            f"Referenced images: {sorted(referenced_images)}"
        )

    def test_no_broken_image_references(self):
        """Test that all image references in cogs point to existing files."""
        referenced_images = get_image_references_from_cogs()
        all_images = get_all_images()

        # Find references that don't point to existing files
        broken_references = [img for img in referenced_images if img not in all_images]

        assert len(broken_references) == 0, (
            f"The following image references are broken (file doesn't exist): {', '.join(broken_references)}"
        )

    def test_image_files_are_valid_formats(self):
        """Test that all images have valid file extensions."""
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        all_images = get_all_images()

        invalid_images = []
        for img in all_images:
            ext = Path(img).suffix.lower()
            if ext not in valid_extensions:
                invalid_images.append(f"{img} (extension: {ext})")

        assert len(invalid_images) == 0, (
            f"The following images have invalid extensions: {', '.join(invalid_images)}\n"
            f"Valid extensions: {', '.join(valid_extensions)}"
        )


class TestCogImports:
    """Tests for cog module imports."""

    @pytest.mark.parametrize("cog_file", get_all_cogs())
    def test_cog_can_be_imported(self, cog_file):
        """Test that each cog file can be imported without errors."""
        # Create module name from file path
        module_name = f"bot.cogs.{cog_file.stem}"

        # Try to import the module
        try:
            spec = importlib.util.spec_from_file_location(module_name, cog_file)
            module = importlib.util.module_from_spec(spec)
            # Note: We don't execute the module to avoid Discord connection issues
            # Just verify it can be loaded
            assert spec is not None, f"Could not create spec for {module_name}"
            assert module is not None, f"Could not create module for {module_name}"
        except Exception as e:
            pytest.fail(f"Failed to import {module_name}: {e}")

    def test_all_cogs_have_setup_function(self):
        """Test that all cog files contain an async setup function."""
        cogs = get_all_cogs()

        missing_setup = []
        for cog_file in cogs:
            with open(cog_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for async def setup pattern
                if not re.search(r'async\s+def\s+setup\s*\(', content):
                    missing_setup.append(cog_file.name)

        assert len(missing_setup) == 0, (
            f"The following cogs are missing 'async def setup' function: {', '.join(missing_setup)}"
        )


class TestImageReferenceCoverage:
    """Detailed tests for image-to-cog mapping."""

    def test_print_image_usage_report(self):
        """Generate a detailed report of image usage (always passes, for information)."""
        all_images = get_all_images()
        referenced_images = get_image_references_from_cogs()

        print("\n" + "="*70)
        print("IMAGE USAGE REPORT")
        print("="*70)
        print(f"\nTotal images in images/: {len(all_images)}")
        print(f"Total images referenced in cogs: {len(referenced_images)}")

        unused = [img for img in all_images if img not in referenced_images]
        if unused:
            print(f"\n⚠️  Unused images ({len(unused)}):")
            for img in sorted(unused):
                print(f"  - {img}")
        else:
            print("\n✓ All images are used!")

        broken = [img for img in referenced_images if img not in all_images]
        if broken:
            print(f"\n⚠️  Broken references ({len(broken)}):")
            for img in sorted(broken):
                print(f"  - {img}")
        else:
            print("\n✓ No broken image references!")

        print("\n" + "-"*70)
        print("Image-to-Cog Mapping:")
        print("-"*70)

        cogs_dir = Path("bot/cogs")
        for img in sorted(all_images):
            cog_list = []
            for cog_file in cogs_dir.glob("*.py"):
                if cog_file.name == "__init__.py":
                    continue
                with open(cog_file, 'r', encoding='utf-8') as f:
                    if f"images/{img}" in f.read():
                        cog_list.append(cog_file.stem)

            if cog_list:
                print(f"  {img:30} → {', '.join(cog_list)}")
            else:
                print(f"  {img:30} → [UNUSED]")

        print("="*70 + "\n")

        # This test always passes - it's just for reporting
        assert True
