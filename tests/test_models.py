"""Tests for all models."""

from src.models import Switch


def test_switch_init():
    """Test initializing a Switch."""
    switch = Switch(id=0, state=True)
    assert switch.id == 0
    assert switch.state is True
