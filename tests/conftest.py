"""
Pytest configuration file.
Handles test fixtures and setup/teardown for proper test isolation.
"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


@pytest.fixture(autouse=True)
def reset_modules():
    """
    Reset module state between tests to prevent cross-contamination.
    This ensures test_api.py mocks don't affect test_cache.py.
    """
    # Store original modules
    original_modules = {}
    modules_to_reset = ['cache', 'db']

    for module in modules_to_reset:
        if module in sys.modules:
            original_modules[module] = sys.modules[module]

    yield

    # Cleanup is handled by pytest automatically
    # Each test file will re-import as needed
