"""Definition of all buttons and switches."""

import os
import random

from src.utils import randomize, randomize_pico


class LevelConfig:
    """Configuration for a specific level."""

    def __init__(
            self, n_leds_per_switch: tuple[int, ...], shuffle_steps: int = 0
        ):
        """Initialize a LevelConfig instance."""
        self.n_leds_per_switch = n_leds_per_switch
        self.shuffle_steps = shuffle_steps


N_LEDS = 10
LEVELS = {
    1: LevelConfig(shuffle_steps=1, n_leds_per_switch=(1,)),
    2: LevelConfig(shuffle_steps=10, n_leds_per_switch=(1, 2)),
    3: LevelConfig(shuffle_steps=20, n_leds_per_switch=(1, 2)),
    4: LevelConfig(shuffle_steps=10, n_leds_per_switch=(2,)),
    5: LevelConfig(shuffle_steps=20, n_leds_per_switch=(2,)),
    6: LevelConfig(shuffle_steps=10, n_leds_per_switch=(1, 2, 3)),
    7: LevelConfig(shuffle_steps=10, n_leds_per_switch=(2, 3)),
    8: LevelConfig(shuffle_steps=20, n_leds_per_switch=(2, 3)),
    9: LevelConfig(shuffle_steps=20, n_leds_per_switch=(3,)),
    10: LevelConfig(shuffle_steps=50, n_leds_per_switch=(3,)),
}


class Switch:
    """A physical switch that can be turned on or off."""
    id: int
    active_state: bool

    def __init__(self, id: int, active_state: bool):
        """Initialize a Switch instance."""
        self.id = id
        self.active_state = active_state


class Button:
    """A physical button that can be pressed."""

    def __init__(self, id: int, state: bool):
        """Initialize a Button instance."""
        self.id = id
        self.state = state


class LEDSimulation:
    """A physical LED that can be turned on."""

    def __init__(self, id: int, value: bool | int):
        """Initialize a LEDSimulation instance."""
        self.id = id
        self.value = value


class PuzzleBase:
    """PuzzleBase that contains all hardware, logic and difficulty.

    This game will be playable in Python, but no on the microchip.
    """

    def __init__(self, simulation: bool):
        """Initialize a PuzzleBase instance."""
        self.leds = [LEDSimulation(id=i, value=False) for i in range(N_LEDS)]
        self.switches = [Switch(id=i, active_state=False) for i in range(N_LEDS)]
        self.map: dict[int, list[int]] = {}
        self.level = 1
        self.completed = False
        self.simulation = simulation

    def get_led_states(self) -> list[bool | int]:
        """Get the states of all the PuzzleBase's LEDs."""
        return [led.value for led in self.leds]

    def get_switch_states(self) -> list[bool]:
        """Get the states of all the PuzzleBase's Switches."""
        return [switch.active_state for switch in self.switches]

    def get_switch_ids(self) -> list[int]:
        """Get the states of all the PuzzleBase's Switches."""
        return [switch.id for switch in self.switches]

    def get_led_ids(self) -> list[int]:
        """Get the states of all the PuzzleBase's LEDs."""
        return [led.id for led in self.leds]

    def toggle_led(self, led_id: int):
        """Toggle the state of a given LED id."""
        self.leds[led_id].value = not self.leds[led_id].value

    def toggle_switch(self, switch_id: int):
        """Toggle the state of a given Switch id."""
        self.switches[switch_id].active_state = not self.switches[switch_id].active_state

    def reset(self):
        """Reset the current PuzzleBase.

        Actions taken in this method:
        - All LEDs are turned OFF.
        """
        print("RESETTING")
        self.completed = False
        level_config = LEVELS[self.level]

        self.turn_on_leds()

        self.map = self.create_puzzle_map(level_config)
        n_steps = level_config.shuffle_steps
        self.take_n_random_steps(n_steps)

    def turn_off_leds(self):
        """Turn off all LEDS."""
        for led in self.leds:
            led.value = 0

    def turn_on_leds(self):
        """Turn on all LEDS."""
        for led in self.leds:
            led.value = 1

    def get_display(self) -> str:
        """Construct the display of the PuzzleBase."""
        led_states = [str(int(led)) for led in self.get_led_states()]
        switch_states = [str(int(switch)) for switch in self.get_switch_states()]
        display = "LEDs:     " + " ".join(led_states) + "\nSwitches: " + " ".join(switch_states)
        return display

    def render(self):
        """Render the current state of the PuzzleBase."""
        print(self.get_display())

    def create_puzzle_map(self, level_config: LevelConfig) -> dict[int, list[int]]:
        """Create the random map which links switches with one or more LEDs."""
        switches = self.get_switch_ids()
        led_ids = self.get_led_ids()
        # TODO: Refactor this
        shuffled_leds = randomize_pico(led_ids, level_config.n_leds_per_switch)
        return dict(zip(switches, shuffled_leds))

    def take_step(self, switch_id: int):
        """Take a step in the puzzle by toggling the given Switch."""
        self.toggle_switch(switch_id)
        for led in self.map[switch_id]:
            self.toggle_led(led)

    def take_n_random_steps(self, n: int):
        """Shuffle the puzzle by taking n random steps."""
        for _ in range(n):
            # TODO: Refactor this hardcoded thing
            if self.simulation:
                switch_to_toggle = random.randint(0, 9)
            else:
                switch_to_toggle = random.randint(10, 19)
            self.take_step(switch_to_toggle)

    def play(self):
        """Play a PuzzleBase game."""
        # Setup display
        os.system("clear")

        cmd = ""
        choose_level = True

        while cmd != "exit":
            if self.is_solved():
                print("Congratulations, you have solved this puzzle!")
                print("A new game will start")
                choose_level = True

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

    def is_solved(self) -> bool:
        """Check whether the puzzle is solved or not."""
        return sum(self.get_led_states()) == N_LEDS

    def increase_level(self):
        """Increase the PuzzleBase's level."""
        self.level = min(self.level + 1, 10)

    def decrease_level(self):
        """Decrease the PuzzleBase's level."""
        self.level = max(self.level - 1, 1)
