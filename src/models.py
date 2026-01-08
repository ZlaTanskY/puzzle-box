"""Definition of all buttons and switches."""

import os
import random

from dataclasses import dataclass

from src.utils import randomize


N_LEDS = 10


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
        self.leds = [LED(id=i, state=False) for i in range(N_LEDS)]
        self.switches = [Switch(id=i, state=False) for i in range(N_LEDS)]
        self.map = {}

    def get_led_states(self) -> list[bool]:
        """Get the states of all the Puzzle's LEDs."""
        return [led.state for led in self.leds]

    def get_switch_states(self) -> list[bool]:
        """Get the states of all the Puzzle's Switches."""
        return [switch.state for switch in self.switches]

    def get_switch_ids(self) -> list[int]:
        """Get the states of all the Puzzle's Switches."""
        return [switch.id for switch in self.switches]

    def get_led_ids(self) -> list[int]:
        """Get the states of all the Puzzle's LEDs."""
        return [led.id for led in self.leds]

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
        original_switch_states = self.get_switch_states()

        for led in self.leds:
            led.state = False
        self.map = self.create_puzzle_map()
        n_steps = 10  # TODO: This should be based on difficulty
        self.take_n_random_steps(n_steps)

        # Reset the switch states back to how they were
        # Currently this is just a reset to False
        # TODO: Change to get input from Pico board
        for enum, switch in enumerate(self.switches):
            switch.state = original_switch_states[enum]

    def get_display(self) -> str:
        """Construct the display of the Puzzle."""
        led_states = [str(int(led)) for led in self.get_led_states()]
        switch_states = [str(int(switch)) for switch in self.get_switch_states()]
        display = "LEDs:     " + " ".join(led_states) + "\nSwitches: " + " ".join(switch_states)
        return display

    def render(self):
        """Render the current state of the Puzzle."""
        print(self.get_display())

    def create_puzzle_map(self) -> dict[int, int]:
        """Create the random map which links switches with one or more LEDs."""
        switches = self.get_switch_ids()
        led_ids = self.get_led_ids()
        shuffled_leds = randomize(led_ids)
        return dict(zip(switches, shuffled_leds))

    def take_step(self, switch_id: int):
        """Take a step in the puzzle by toggling the given Switch."""
        self.toggle_switch(switch_id)
        self.toggle_led(self.map[switch_id])

    def take_n_random_steps(self, n: int):
        """Shuffle the puzzle by taking n random steps."""
        for _ in range(n):
            switch_to_toggle = random.randint(0, 9)
            self.take_step(switch_to_toggle)

    def play(self):
        """Play a Puzzle game."""
        # Setup display
        os.system("clear")
        self.render()

        switch_id = ""

        while switch_id != "exit" and not self.is_solved():
            switch_id = input("Which switch do you want to toggle? [0-9]")
            if switch_id.isdigit():
                self.take_step(int(switch_id))

            os.system("clear")
            self.render()

        if self.is_solved():
            print("Congratulations, you have solved this puzzle!")

    def is_solved(self) -> bool:
        """Check whether the puzzle is solved or not."""
        return sum(self.get_led_states()) == N_LEDS
