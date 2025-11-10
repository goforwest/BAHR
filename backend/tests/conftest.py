"""
Pytest configuration and shared fixtures for integration tests.
"""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session.
    
    This fixture ensures async tests can run properly.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Mark configuration
def pytest_configure(config):
    """
    Register custom pytest markers.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
