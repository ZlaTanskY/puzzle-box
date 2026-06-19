"""Tests for all models."""

import random

from pytest_mock import MockerFixture

from src.models import LEVELS, PuzzleBase


def test_puzzle_init():
    """Test initializing a PuzzleBase instance."""
    puzzle = PuzzleBase()
    assert len(puzzle.leds) == 10
    assert len(puzzle.switches) == 10
    assert puzzle.level == 1


def test_get_puzzle_led_states():
    """Test getting the PuzzleBase's LED states."""
    puzzle = PuzzleBase()
    target = [False] * 10

    result = puzzle.get_led_states()

    assert result == target


def test_get_switch_states():
    """Test getting the PuzzleBase's Switch states."""
    puzzle = PuzzleBase()
    target = [False] * 10

    result = puzzle.get_switch_states()

    assert result == target


def test_get_switch_ids():
    """Test getting the switch_ids."""
    puzzle = PuzzleBase()
    target = list(range(10))

    result = puzzle.get_switch_ids()

    assert result == target


def test_get_led_ids():
    """Test getting the switch_ids."""
    puzzle = PuzzleBase()
    target = list(range(10))

    result = puzzle.get_led_ids()

    assert result == target


def test_toggle_led():
    """Test toggling a LED."""
    puzzle = PuzzleBase()
    puzzle.toggle_led(2)

    result = puzzle.get_led_states()

    assert sum(result) == 1
    assert result[2] is True


def test_toggle_switch():
    """Test toggling a Switch."""
    puzzle = PuzzleBase()
    puzzle.toggle_switch(2)

    result = puzzle.get_switch_states()

    assert sum(result) == 1
    assert result[2] is True


def test_puzzle_reset(mocker: MockerFixture):
    """Test resetting an existing PuzzleBase."""
    puzzle = PuzzleBase()
    mock_take_steps = mocker.patch.object(puzzle, "take_n_random_steps")
    puzzle.toggle_led(2)
    # Resetting a puzzle should not reset switches as it is a hardware input
    puzzle.toggle_switch(2)

    # Check if setup is correct
    assert sum(puzzle.get_led_states()) == 1

    puzzle.reset()

    assert sum(puzzle.get_led_states()) == 10
    assert sum(puzzle.get_switch_states()) == 1
    mock_take_steps.assert_called_once()


def test_get_display():
    """Test constructing the display of a puzzle."""
    puzzle = PuzzleBase()

    target = (
        """LEDs:     0 0 0 0 0 0 0 0 0 0\n"""
        """Switches: 0 0 0 0 0 0 0 0 0 0"""
    )

    result = puzzle.get_display()

    assert result == target


def test_create_puzzle_map():
    """Test creating the random map between switches and LEDs."""
    puzzle = PuzzleBase()
    level_config = LEVELS[1]

    random.seed(13)
    target_1 = {0: [3], 1: [0], 2: [7], 3: [8], 4: [6], 5: [1], 6: [5], 7: [2], 8: [9], 9: [4]}
    target_2 = {0: [6], 1: [0], 2: [8], 3: [2], 4: [9], 5: [3], 6: [5], 7: [7], 8: [4], 9: [1]}

    result_1 = puzzle.create_puzzle_map(level_config)

    assert result_1 == target_1

    result_2 = puzzle.create_puzzle_map(level_config)

    print(result_2)
    assert result_2 == target_2


def test_take_step():
    """Test taking a step by toggling one switch."""
    puzzle = PuzzleBase()
    led_map = [[4], [1], [8], [9, 1], [7, 3], [2], [6, 3], [3], [10, 8], [5, 3]]
    puzzle.map = dict(zip(range(10), led_map))

    assert sum(puzzle.get_led_states()) == 0

    puzzle.take_step(0)
    assert sum(puzzle.get_led_states()) == 1
    assert puzzle.get_led_states()[4] == 1

    puzzle.take_step(3)
    assert sum(puzzle.get_led_states()) == 3
    assert puzzle.get_led_states()[9] == 1
    assert puzzle.get_led_states()[1] == 1


def test_puzzle_is_solved():
    """Test checking if a puzzle is solved."""
    puzzle = PuzzleBase()

    # The puzzle should not be solved from the start
    assert not puzzle.is_solved()

    for led in puzzle.leds:
        led.value = True

    assert puzzle.is_solved()


def test_increase_level():
    """Test increasing the level of the puzzle."""
    puzzle = PuzzleBase()

    assert puzzle.level == 1

    puzzle.increase_level()

    assert puzzle.level == 2


def test_increase_level_max_10():
    """Test increasing the level of the puzzle does not go higher than 10."""
    puzzle = PuzzleBase()
    puzzle.level = 10

    puzzle.increase_level()

    assert puzzle.level == 10


def test_decrease_level():
    """Test decreasing the level of the puzzle."""
    puzzle = PuzzleBase()

    puzzle.level = 5

    puzzle.decrease_level()

    assert puzzle.level == 4


def test_decrease_level_minimum_1():
    """Test decreasing the level of the puzzle does not go lower than 1."""
    puzzle = PuzzleBase()
    puzzle.level = 1

    puzzle.decrease_level()

    assert puzzle.level == 1
