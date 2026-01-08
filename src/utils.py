"""Helper functions used through the project."""

import random

def randomize(ids: list[int]) -> list[int]:
    """Randomize the sequence of a list of integers.

    Args:
        ids (list[int]): The original list of ids to be shuffled randomly
    """
    random.shuffle(ids)
    return ids
