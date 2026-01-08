"""Definition of all buttons and switches."""

import os
from dataclasses import dataclass


@dataclass
class Switch:
    """A physical switch that can be turned on or off."""
    id: int
    state: bool


@dataclass
class Button:
    """A physical button that can be pressed."""
    id: int
    state: bool


@ dataclass
class LED:
    """A physical LED that can be turned on."""
    id: int
    state: bool


class Puzzle:
    """Puzzle that contains all hardware, logic and difficulty."""

    def __init__(self):
        """Initialize a Puzzle instance."""
        self.leds = [LED(id=i, state=False) for i in range(10)]
        self.switches = [Switch(id=i, state=False) for i in range(10)]

    def get_led_states(self) -> list[bool]:
        """Get the states of all the Puzzle's LEDs."""
        return [led.state for led in self.leds]

    def get_switch_states(self) -> list[bool]:
        """Get the states of all the Puzzle's Switches."""
        return [switch.state for switch in self.switches]

    def toggle_led(self, led_id: int):
        """Toggle the state of a given LED id."""
        self.leds[led_id].state = not self.leds[led_id].state

    def toggle_switch(self, switch_id: int):
        """Toggle the state of a given Switch id."""
        self.switches[switch_id].state = not self.switches[switch_id].state

    def reset(self):
        """Reset the current Puzzle.

        Actions taken in this method:
        - All LEDs are turned OFF.
        """
        for led in self.leds:
            led.state = False

    def get_display(self) -> str:
        """Construct the display of the Puzzle."""
        led_states = [str(int(led)) for led in self.get_led_states()]
        switch_states = [str(int(switch)) for switch in self.get_switch_states()]
        display = "LEDs:     " + " ".join(led_states) + "\nSwitches: " + " ".join(switch_states)
        return display

    def render(self):
        """Render the current state of the Puzzle."""
        print(self.get_display())

    def play(self):
        """Play a Puzzle game."""
        # Setup display
        os.system("clear")
        self.render()

        while (switch_id := input("Which switch do you want to toggle? [0-9]")) != "exit":
            if switch_id.isdigit():
                # For now just toggle the same LED as Switch id
                self.toggle_switch(int(switch_id))
                self.toggle_led(int(switch_id))

            os.system("clear")
            self.render()
