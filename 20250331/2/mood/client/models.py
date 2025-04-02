from enum import Enum


class Cows:
    """Available extra cows."""

    custom_cows = ["jgsbat"]


class Cord:
    """Class representing a mob or player's position."""

    def __init__(self, x=0, y=0):
        """Create a cord object."""
        self.x: int = x
        self.y: int = y

    def to_dict(self):
        """Return a dictionary representation of the Cord instance."""
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        """Create a cord from a dictionary with x, y fields."""
        return cls(**data)

    def __str__(self):
        """Return a string representation of the Cord instance."""
        return f"({self.x}, {self.y})"


class Direction(Enum):
    """Available directions."""

    UP = Cord(0, -1)
    DOWN = Cord(0, 1)
    RIGHT = Cord(1, 0)
    LEFT = Cord(-1, 0)


class Weapon(Enum):
    """Available weapons."""

    SWORD = 10
    SPEAR = 15
    AXE = 20
