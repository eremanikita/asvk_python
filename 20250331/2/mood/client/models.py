from enum import Enum


class Cows:
    custom_cows = ["jgsbat"]


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Direction(Enum):
    UP = Cord(0, -1)
    DOWN = Cord(0, 1)
    RIGHT = Cord(1, 0)
    LEFT = Cord(-1, 0)


class Weapon(Enum):
    SWORD = 10
    SPEAR = 15
    AXE = 20
