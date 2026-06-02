"""Definition of all buttons and switches to be used on the Pico.

These are separate because this is run using MicroPython.
The imports will not work using Python.
"""

import time

from picozero import LED, Button, Switch

from src.models import PuzzleBase


LED_PINS = tuple(range(0, 10))
SWITCH_PINS = tuple(range(10, 20))
BUTTON_PINS = (20, 21, 22)

# Inputs are polled rather than interrupt-driven. Driving an LED pin from
# inside an IRQ-scheduled callback couples glitches back onto the switch
# lines; with the scheduler locked those glitch IRQs overflow the
# micropython.schedule queue (EventFailedScheduleQueueFull). Polling never
# calls schedule() on an edge, so a coupled glitch is just read as a
# momentary level and filtered out by the debounce below.
DEBOUNCE_MS = 50
POLL_INTERVAL_MS = 5

# Button roles within BUTTON_PINS.
BTN_INCREASE = 0
BTN_DECREASE = 1
BTN_SELECT = 2

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
        self.choose_level = False

        # Debounce state for polled inputs: the last accepted (stable) reading,
        # the current candidate reading, and the tick at which the candidate
        # was first seen. A candidate is accepted only once it has persisted
        # for DEBOUNCE_MS, which filters out coupled glitches.
        self._btn_accepted = [False] * len(self.buttons)
        self._btn_candidate = [False] * len(self.buttons)
        self._btn_since = [0] * len(self.buttons)
        self._sw_accepted = [False] * len(self.switches)
        self._sw_candidate = [False] * len(self.switches)
        self._sw_since = [0] * len(self.switches)

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
            self.poll_inputs()
            if self.is_solved() and not self.choose_level and not self.completed:
                self.completed = True
                self.congratulations()
                print("Done celebrating")
                self.reset()
            time.sleep_ms(POLL_INTERVAL_MS)

    def poll_inputs(self):
        """Read inputs and act on debounced state changes.

        Replaces picozero's interrupt callbacks: an edge never schedules a
        callback, so it cannot overflow the micropython schedule queue.
        """
        # SELECT toggles between the level-select and play stages in both
        # stages. Acting on it ends the iteration because it rebuilds the
        # input layout.
        if self._button_pressed(BTN_SELECT):
            self.toggle_stage()
            return

        if self.choose_level:
            if self._button_pressed(BTN_INCREASE):
                self.increase_level()
            if self._button_pressed(BTN_DECREASE):
                self.decrease_level()
        else:
            for enum in range(len(self.switches)):
                if self._switch_changed(enum):
                    self.take_step(enum + 10)

    def _debounce(self, raw, idx, accepted, candidate, since):
        """Return True when `raw` becomes the new debounced state for `idx`."""
        if raw != accepted[idx]:
            if raw != candidate[idx]:
                candidate[idx] = raw
                since[idx] = time.ticks_ms()
            elif time.ticks_diff(time.ticks_ms(), since[idx]) >= DEBOUNCE_MS:
                accepted[idx] = raw
                return True
        else:
            candidate[idx] = raw
        return False

    def _button_pressed(self, idx) -> bool:
        """Return True on a debounced press (inactive -> active) of a button."""
        raw = self.buttons[idx].is_active
        changed = self._debounce(
            raw, idx, self._btn_accepted, self._btn_candidate, self._btn_since
        )
        return changed and self._btn_accepted[idx]

    def _switch_changed(self, idx) -> bool:
        """Return True on any debounced change of a switch's position."""
        raw = self.switches[idx].is_active
        return self._debounce(
            raw, idx, self._sw_accepted, self._sw_candidate, self._sw_since
        )

    def _snapshot_switches(self):
        """Baseline switch readings so entering play doesn't fire a phantom step."""
        for enum, switch in enumerate(self.switches):
            state = switch.is_active
            self._sw_accepted[enum] = state
            self._sw_candidate[enum] = state

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
        """Switch the game into the level-select stage.

        Inputs are polled (see :meth:`poll_inputs`), so no GPIO callbacks are
        registered here; this only sets up the display.
        """
        self.is_playing = False
        self.turn_off_leds()
        self.blink_level()

    def activate_play_stage(self):
        """Switch the game into the play stage.

        Inputs are polled (see :meth:`poll_inputs`), so no GPIO callbacks are
        registered; we just build the puzzle and baseline the switches.
        """
        self.reset()
        self._snapshot_switches()

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
