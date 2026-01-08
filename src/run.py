"""Processes that needs to be run."""

from src.models import Puzzle

def main():
    """Main process."""
    # Create a game
    puzzle = Puzzle()
    puzzle.reset()
    puzzle.play()
