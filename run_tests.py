#!/usr/bin/env python3
"""
Test runner for EasyJournal.

This script runs all the tests for the EasyJournal application.
"""

import unittest
import sys
import os


def run_tests():
    """Run all tests in the tests directory."""
    # Discover all tests in the tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')

    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # Return the number of failures and errors
    return len(result.failures) + len(result.errors)


if __name__ == '__main__':
    # Make sure uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    # Run the tests and use the result as exit code
    sys.exit(run_tests())