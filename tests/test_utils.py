"""Test helper functions."""

import random

from src.utils import randomize


def test_randomize():
    """Test randomizing a list of integers a single time."""
    test_input = [1, 2, 3, 4, 5]

    random.seed(13)
    target = [[2], [1], [4], [5], [3]]

    result = randomize(test_input, (1,))

    assert result == target

def test_randomize_two_links():
    """Test randomizing links between a switch and two leds."""
    test_input = [1, 2, 3]

    random.seed(13)
    target = [[1, 2], [3, 1], [2, 1]]

    result = randomize(test_input, (2,))

    assert result == target

def test_randomize_multiple_links():
    """Test randomizing links between switches and possibly multiple leds."""
    test_input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    random.seed(13)
    target = [[4], [1], [8], [9, 1], [7, 3], [2], [6, 3], [3], [10, 8], [5, 3]]

    result = randomize(test_input, (1, 2))

    assert result == target
