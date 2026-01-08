"""Definition of all buttons and switches."""

from dataclasses import dataclass


@dataclass
class Switch:
    """A physical switch that can be turned on or off."""
    id: int
    state: int


@dataclass
class Button:
    """A physical button that can be pressed."""
    id: int
    state: int
