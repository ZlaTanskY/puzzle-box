"""Process to be run on Pico."""

from src.models_pico import Puzzle

from picozero import LED, Button, Switch, pico_led

def main():
    """Main process."""
    # Create a game
    print("Creating a Puzzle")
    puzzle = Puzzle()
    print("Playing the puzzle")
    puzzle.play()

# pico_led.on()
# led = LED(15, pwm=False, initial_value=True)

# def led_toggle():
#     print("Led is toggled")
#     pico_led.toggle()
#     led.toggle()

# button = Button(14)
# button.when_activated = led_toggle

if __name__ == "__main__":

    # while 1:
    #     pass
    main()
