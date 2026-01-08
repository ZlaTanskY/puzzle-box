"""Tests for all models."""

from src.models import Puzzle


def test_puzzle_init():
    """Test initializing a Puzzle instance."""
    puzzle = Puzzle()
    assert len(puzzle.leds) == 10
    assert len(puzzle.switches) == 10


def test_get_puzzle_led_states():
    """Test getting the Puzzle's LED states."""
    puzzle = Puzzle()
    target = [False] * 10

    result = puzzle.get_led_states()

    assert result == target


def test_get_switch_states():
    """Test getting the Puzzle's Switch states."""
    puzzle = Puzzle()
    target = [False] * 10

    result = puzzle.get_switch_states()

    assert result == target


def test_toggle_led():
    """Test toggling a LED."""
    puzzle = Puzzle()
    puzzle.toggle_led(2)

    result = puzzle.get_led_states()

    assert sum(result) == 1
    assert result[2] is True


def test_toggle_switch():
    """Test toggling a Switch."""
    puzzle = Puzzle()
    puzzle.toggle_switch(2)

    result = puzzle.get_switch_states()

    assert sum(result) == 1
    assert result[2] is True


def test_puzzle_reset():
    """Test resetting an existing Puzzle."""
    puzzle = Puzzle()
    puzzle.toggle_led(2)
    # Resetting a puzzle should not reset switches as it is a hardware input
    puzzle.toggle_switch(2)

    # Check if setup is correct
    assert sum(puzzle.get_led_states()) == 1

    puzzle.reset()

    assert sum(puzzle.get_led_states()) == 0
    assert sum(puzzle.get_switch_states()) == 1


def test_get_display():
    """Test constructing the display of a puzzle."""
    puzzle = Puzzle()

    target = (
        """LEDs:     0 0 0 0 0 0 0 0 0 0\n"""
        """Switches: 0 0 0 0 0 0 0 0 0 0"""
    )

    result = puzzle.get_display()

    assert result == target
