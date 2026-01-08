"""Tests for all models."""

import random

from pytest_mock import MockerFixture

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


def test_get_switch_ids():
    """Test getting the switch_ids."""
    puzzle = Puzzle()
    target = list(range(10))

    result = puzzle.get_switch_ids()

    assert result == target


def test_get_led_ids():
    """Test getting the switch_ids."""
    puzzle = Puzzle()
    target = list(range(10))

    result = puzzle.get_led_ids()

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


def test_puzzle_reset(mocker: MockerFixture):
    """Test resetting an existing Puzzle."""
    puzzle = Puzzle()
    mock_take_steps = mocker.patch.object(puzzle, "take_n_random_steps")
    puzzle.toggle_led(2)
    # Resetting a puzzle should not reset switches as it is a hardware input
    puzzle.toggle_switch(2)

    # Check if setup is correct
    assert sum(puzzle.get_led_states()) == 1

    puzzle.reset()

    assert sum(puzzle.get_led_states()) == 0
    assert sum(puzzle.get_switch_states()) == 1
    mock_take_steps.assert_called_once()


def test_get_display():
    """Test constructing the display of a puzzle."""
    puzzle = Puzzle()

    target = (
        """LEDs:     0 0 0 0 0 0 0 0 0 0\n"""
        """Switches: 0 0 0 0 0 0 0 0 0 0"""
    )

    result = puzzle.get_display()

    assert result == target


def test_create_puzzle_map():
    """Test creating the random map between switches and LEDs."""
    puzzle = Puzzle()

    random.seed(13)
    target_1 = {0: 3, 1: 0, 2: 7, 3: 8, 4: 6, 5: 1, 6: 5, 7: 2, 8: 9, 9: 4}
    target_2 = {0: 8, 1: 6, 2: 4, 3: 7, 4: 0, 5: 9, 6: 5, 7: 3, 8: 1, 9: 2}

    result_1 = puzzle.create_puzzle_map()

    assert result_1 == target_1

    result_2 = puzzle.create_puzzle_map()

    assert result_2 == target_2


def test_take_step():
    """Test taking a step by toggling one switch."""
    puzzle = Puzzle()
    puzzle.map = dict(zip(range(10), range(9, 0, -1)))

    assert sum(puzzle.get_led_states()) == 0

    puzzle.take_step(0)
    assert sum(puzzle.get_led_states()) == 1
    assert puzzle.get_led_states()[-1] == 1


def test_puzzle_is_solved():
    """Test checking if a puzzle is solved."""
    puzzle = Puzzle()

    # The puzzle should not be solved from the start
    assert not puzzle.is_solved()

    for led in puzzle.leds:
        led.state = True

    assert puzzle.is_solved()
