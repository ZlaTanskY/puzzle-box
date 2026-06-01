"""Definition of all buttons and switches to be used on the Pico.

These are separate because this is run using MicroPython.
The imports will not work using Python.
"""

from picozero import LED, Button, Switch

from src.models import PuzzleBase


LED_PINS = tuple(range(0, 10))
SWITCH_PINS = tuple(range(10, 20))
BUTTON_PINS = (20, 21, 22)

class Puzzle(PuzzleBase):
    """Puzzle to be integrated in the Pico microchip."""

    def __init__(self):  # pylint: disable=super-init-not-called
        """Initialize a Puzzle."""
        self.leds = [LED(pin, pwm=False) for pin in LED_PINS]
        self.switches = [Switch(pin, bounce_time=0.1) for pin in SWITCH_PINS]
        self.buttons = [Button(pin) for pin in BUTTON_PINS]
        self.map: dict[int, list[int]] = {}
        self.level = 1
        self.completed = False
        self.is_playing = False
        self.last_state = {}

        # The SELECT button remains the same throughout the game
        button_select = self.buttons[2]
        button_select.when_pressed = self.toggle_stage

        self.choose_level = False

    def reset(self):
        """Reset the puzzle while suppressing solved-detection."""
        self.is_playing = False
        super().reset()
        self.is_playing = True

    def is_solved(self) -> bool:
        """Return True only while the puzzle is in active play."""
        if not self.is_playing:
            return False
        return super().is_solved()

    def take_step(self, switch_id):
        """Take a step in the puzzle by toggling the given Switch."""
        for led in self.map[switch_id]:
            self.toggle_led(led)

    def toggle_led(self, led_id: int):
        """Toggle the state of a given LED id."""
        self.leds[led_id].toggle()

    def get_switch_ids(self) -> tuple[int]:
        """Get the states of all the Puzzle's Switches."""
        return SWITCH_PINS

    def get_led_ids(self) -> tuple[int]:
        """Get the states of all the Puzzle's LEDs."""
        return LED_PINS

    def play(self):
        """Play the game in the microchip."""
        self.toggle_stage()
        while True:
            if self.is_solved() and not self.choose_level and not self.completed:
                self.completed = True
                self.congratulations()
                print("Done celebrating")
                self.reset()

    def toggle_stage(self):
        """Toggle between stages.

        There are two options:
        - Level select stage
        - Play stage
        """
        if self.choose_level:
            print("Now playing the stage")
            self.activate_play_stage()
        else:
            print("Now selecting the level")
            self.activate_level_select_stage()
        self.choose_level = not self.choose_level

    def activate_level_select_stage(self):
        """Activate the correct GPIO necessary to select a level."""
        self.is_playing = False
        self.turn_off_leds()
        self.blink_level()

        # Deactivate switches
        for switch in self.switches:
            switch.when_activated = self.nothing
            switch.when_deactivated = self.nothing

        # Activate buttons
        button_increase_level = self.buttons[0]
        button_increase_level.when_pressed = self.increase_level
        button_decrease_level = self.buttons[1]
        button_decrease_level.when_pressed = self.decrease_level

    def activate_play_stage(self):
        """Activate the correct GPIO necessary to play the puzzle."""
        self.reset()

        # Activate switches
        for enum, switch in enumerate(self.switches):
            # Micro implementation of partial as 
            # it is not available in MicroPython
            def make_step(e):
                def step():
                    self.take_step(e)
                return step
            
            def make_step_v2(e):
                def step():
                    current = self.switches[e].active_state
                    previous = self.last_state.get(e)

                    # ignore repeated identical events
                    if previous == current:
                        return

                    self.last_state[e] = current

                    # only act on real transition
                    self.take_step(e + 10)

                return step

            # TODO: Refactor this
            step = make_step(enum + 10)
            # step = make_step_v2(enum)
            switch.when_activated = step
            switch.when_deactivated = step

        # Deactivate some buttons
        button_increase_level = self.buttons[0]
        button_increase_level.when_pressed = self.nothing
        button_decrease_level = self.buttons[1]
        button_decrease_level.when_pressed = self.nothing

    def nothing(self):
        """Empty callback"""

    def congratulations(self):
        """Blink some LEDs after finishing the puzzle."""
        print("Gratz, you won")
        self.turn_off_leds()
        # for led in self.leds:
        #     led.blink(n=5)

    def blink_level(self):
        """Blink LEDs based on the current level."""
        # This is needed to turn off leds of higher levels when decreasing
        # the level
        self.turn_off_leds()

        for led in range(self.level):
            self.leds[led].on()

        # The final LED should be blinking
        self.leds[led].blink()

    def increase_level(self):
        """Increase the Puzzle's level."""
        super().increase_level()
        self.blink_level()

    def decrease_level(self):
        """Decrease the Puzzle's level."""
        super().decrease_level()
        self.blink_level()
