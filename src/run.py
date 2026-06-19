"""Processes that needs to be run."""

from src.models import PuzzleBase

def main():
    """Main process."""
    # Create a game
    print("hello")
    puzzle = PuzzleBase()
    puzzle.reset()
    puzzle.play()
