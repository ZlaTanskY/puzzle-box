"""Tests for all models."""

import pytest

from src.models import Button, Switch


def test_switch_init():
    """Test initializing a Switch."""
    switch = Switch(id=0, state=True)
    assert switch.id == 0
    assert switch.state == True
