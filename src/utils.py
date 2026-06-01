"""Helper functions used through the project."""

import random
import time

def randomize(ids: list[int], n_leds: tuple[int, ...]) -> list[int]:
    """Randomize the sequence of a list of integers.

    Args:
        ids (list[int]): The original list of ids to be shuffled randomly
        n_leds (tuple[int, ...]): The amount of leds that can be linked with
            a switch. If this is a tuple of for example (1, 2), this means that
            some switches can be linked with one LED and other with two.
    """
    # Define basic shuffle
    random.shuffle(ids)
    led_map = []

    for enum, _ in enumerate(ids):
        n_links = random.choice(n_leds)
        current_map = [ids[enum]]
        if n_links > 1:
            # add another link that is not same as the current one
            current_map += random.sample(list(set(ids) - set([ids[enum]])), k=n_links-1)
        led_map.append(current_map)
    return led_map


def randomize_pico(ids: list[int], n_leds: tuple[int, ...]) -> list[int]:
    """Randomize the sequence of a list of integers on pico.

    Args:
        ids (list[int]): The original list of ids to be shuffled randomly
        n_leds (tuple[int, ...]): The amount of leds that can be linked with
            a switch. If this is a tuple of for example (1, 2), this means that
            some switches can be linked with one LED and other with two.
    """
    random.seed(time.ticks_us())
    # Define basic shuffle
    ids = list(ids)
    shuffle(ids)
    led_map = []

    for enum, _ in enumerate(ids):
        n_links = random.choice(n_leds)
        current_map = [ids[enum]]
        if n_links > 1:
            # add another link that is not same as the current one
            current_map += random.sample(list(set(ids) - set([ids[enum]])), k=n_links-1)
        led_map.append(current_map)
    return led_map


def shuffle(lst):
    for i in range(len(lst)):
        j = random.randrange(i, len(lst))
        lst[i], lst[j] = lst[j], lst[i]