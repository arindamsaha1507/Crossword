"""Module for Word class."""

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Direction of a word in the crossword puzzle."""

    ACROSS = 1
    DOWN = 2


@dataclass
class Position:
    """Position of a word in the crossword puzzle."""

    row: int
    col: int


@dataclass
class Word:
    """A word in the crossword puzzle."""

    position: Position
    direction: Direction
    word: str
    clue: str
    number: int

    @property
    def length(self) -> int:
        """Length of the word."""
        return len(self.word)

    @property
    def end_position(self) -> Position:
        """End position of the word."""
        if self.direction == Direction.ACROSS:
            return Position(self.position.row, self.position.col + self.length - 1)
        return Position(self.position.row + self.length - 1, self.position.col)

    def intersects(self, other: "Word") -> bool:
        """Check if two words intersect."""
        if self.direction == other.direction:
            return False
        if (
            self.position.row <= other.position.row <= self.end_position.row
            and other.position.col <= self.position.col <= other.end_position.col
        ):
            return True
        if (
            other.position.row <= self.position.row <= other.end_position.row
            and self.position.col <= other.position.col <= self.end_position.col
        ):
            return True
        return False

    def get_intersection(self, other: "Word") -> Position:
        """Get the intersection position of two words."""
        if self.direction == Direction.ACROSS:
            return Position(other.position.row, self.position.col)
        return Position(self.position.row, other.position.col)

    def get_intersection_letter(self, other: "Word") -> str:
        """Get the intersection letter of two words."""
        intersection = self.get_intersection(other)
        if self.direction == Direction.ACROSS:
            return other.word[intersection.col - other.position.col]
        return other.word[intersection.row - other.position.row]

    @property
    def display_clue(self) -> str:
        """Display the clue of the word."""
        return f":bulb: {self.number}. {self.clue} ({self.length})"

    @property
    def cells(self) -> list[Position]:
        """Get the cells of the word."""
        if self.direction == Direction.ACROSS:
            return [
                Position(self.position.row, self.position.col + i)
                for i in range(self.length)
            ]
        return [
            Position(self.position.row + i, self.position.col)
            for i in range(self.length)
        ]

    def __hash__(self) -> int:
        return self.number

    def __eq__(self, other: "Word") -> bool:
        return self.position == other.position and self.direction == other.direction
