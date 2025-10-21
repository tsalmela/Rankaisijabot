#!/usr/bin/env python3
"""
Convenience script for running Rankaisijabot tests.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --resources  # Run only resource validation tests
    python run_tests.py --commands   # Run only command tests
    python run_tests.py --coverage   # Run with coverage report
    python run_tests.py --report     # Show image usage report
"""

import sys
import subprocess


def run_command(cmd):
    """Run a shell command and return the result."""
    print(f"\n{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    print('='*70)
    result = subprocess.run(cmd)
    return result.returncode


def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        return 0

    if '--resources' in args:
        return run_command(['pytest', 'tests/test_resources.py', '-v'])

    if '--commands' in args:
        return run_command(['pytest', 'tests/test_commands.py', '-v'])

    if '--coverage' in args:
        return run_command([
            'pytest', 'tests/',
            '--cov=bot',
            '--cov-report=term',
            '--cov-report=html',
            '-v'
        ])

    if '--report' in args:
        return run_command([
            'pytest',
            'tests/test_resources.py::TestImageReferenceCoverage::test_print_image_usage_report',
            '-v', '-s'
        ])

    # Default: run all tests
    return run_command(['pytest', 'tests/', '-v'])


if __name__ == '__main__':
    sys.exit(main())
