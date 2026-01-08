"""Test helper functions."""

import random

from src.utils import randomize


def test_randomize():
    """Test randomizing a list of integers a single time."""
    test_input = [1, 2, 3, 4, 5]

    random.seed(13)
    target = [2, 1, 4, 5, 3]

    result = randomize(test_input)

    assert result == target
