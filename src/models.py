"""Definition of all buttons and switches."""

import os
import random

from dataclasses import dataclass

from src.utils import randomize


@dataclass
class LevelConfig:
    """Configuration for a specific level."""
    n_leds_per_switch: tuple[int, ...]
    shuffle_steps: int = 0

N_LEDS = 10
LEVELS = {
    1: LevelConfig(n_leds_per_switch=(1,)),
    2: LevelConfig(n_leds_per_switch=(1, 2)),
    3: LevelConfig(shuffle_steps=10, n_leds_per_switch=(1, 2)),
    4: LevelConfig(shuffle_steps=0, n_leds_per_switch=(2,)),
    5: LevelConfig(shuffle_steps=10, n_leds_per_switch=(2,)),
    6: LevelConfig(shuffle_steps=0, n_leds_per_switch=(1, 2, 3)),
    7: LevelConfig(shuffle_steps=0, n_leds_per_switch=(2, 3)),
    8: LevelConfig(shuffle_steps=20, n_leds_per_switch=(2, 3)),
    9: LevelConfig(shuffle_steps=20, n_leds_per_switch=(3,)),
    10: LevelConfig(shuffle_steps=50, n_leds_per_switch=(3,)),
}


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
        self.map: dict[int, list[int]] = {}
        self.level = 1

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
        level_config = LEVELS[self.level]

        for led in self.leds:
            led.state = False
        self.map = self.create_puzzle_map(level_config)
        n_steps = level_config.shuffle_steps
        self.take_n_random_steps(n_steps)

        # Reset the switch states back to how they were
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

    def create_puzzle_map(self, level_config: LevelConfig) -> dict[int, list[int]]:
        """Create the random map which links switches with one or more LEDs."""
        switches = self.get_switch_ids()
        led_ids = self.get_led_ids()
        shuffled_leds = randomize(led_ids, level_config.n_leds_per_switch)
        return dict(zip(switches, shuffled_leds))

    def take_step(self, switch_id: int):
        """Take a step in the puzzle by toggling the given Switch."""
        self.toggle_switch(switch_id)
        for led in self.map[switch_id]:
            self.toggle_led(led)

    def take_n_random_steps(self, n: int):
        """Shuffle the puzzle by taking n random steps."""
        for _ in range(n):
            switch_to_toggle = random.randint(0, 9)
            self.take_step(switch_to_toggle)

    def play(self):
        """Play a Puzzle game."""
        # Setup display
        os.system("clear")

        cmd = ""
        choose_level = True

        while cmd != "exit" and not self.is_solved():
            # Select level
            if choose_level:
                cmd = input(
                    f"Level: {self.level}. Choose 'increase', 'decrease', or 'start': "
                )
                os.system("clear")
                if cmd == "increase":
                    self.increase_level()
                elif cmd == "decrease":
                    self.decrease_level()
                elif cmd == "start":
                    choose_level = False
                    self.reset()
                    self.render()
            else:
            # Play
                cmd = input(f"lvl {self.level} - Which switch do you want to toggle? [0-9] ")
                if cmd.isdigit():
                    self.take_step(int(cmd))
                os.system("clear")
                self.render()

        if self.is_solved():
            print("Congratulations, you have solved this puzzle!")

    def is_solved(self) -> bool:
        """Check whether the puzzle is solved or not."""
        return sum(self.get_led_states()) == N_LEDS

    def increase_level(self):
        """Increase the Puzzle's level."""
        self.level = min(self.level + 1, 10)

    def decrease_level(self):
        """Decrease the Puzzle's level."""
        self.level = max(self.level - 1, 1)
