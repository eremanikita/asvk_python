from cowsay import list_cows


class Cow:
    """Extra cows."""

    custom_cows = {
        "jgsbat": """    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\\/o\\/o\\/'.   `(
      ) .' . \\====/ . '. (
       )  / <<    >> \\  (
        '-._/``  ``\\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))"""
    }


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

    def __add__(self, other):
        """Modify a cord object to a specific direction."""
        return Cord((self.x + other.x) % 10, (self.y + other.y) % 10)

    def __str__(self):
        """Return a string representation of the Cord instance."""
        return f"({self.x}, {self.y})"


class Mob:
    """Class representing a game's mob."""

    def __init__(self, message, name, hp):
        """Create a mob object."""
        self.message = message
        self.name = name
        self.hp = hp

    def get_damage(self, hp):
        """Damage the mob.

        return remained hp and got damage
        """
        damage_value = min(hp, self.hp)
        self.hp -= damage_value
        return self.hp, damage_value

    @staticmethod
    def check_name(name):
        """Check if mob name is correct."""
        return name in list_cows() or name in Cow.custom_cows


class Field:
    """Field class representing a game field."""

    def __init__(self):
        """Initialize a Field instance."""
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, cord, name, message, hp):
        """Add a mob to the provided cell if the monster info is correct."""
        if Mob.check_name(name):
            self.field[cord.x][cord.y] = Mob(message, name, hp)
            return self.field[cord.x][cord.y]
        return None

    def get_monster(self, cord) -> Mob | None:
        """Get a monster object in the provided cell."""
        return self.field[cord.x][cord.y]

    def del_mob(self, cord):
        """Delete mob from a field cell."""
        self.field[cord.x][cord.y] = None

    def check_cell(self, cord: Cord):
        """Check cell if there is a mob in the cell."""
        return not self.get_monster(cord) is None


class Player:
    """Class representing a user's player in the game."""

    def __init__(self, player_id):
        """Create a player object."""
        self.id = player_id
        self.cord = Cord()

    def move(self, direction: Cord):
        """Move the player to the specified cell."""
        self.cord = self.cord + direction
        return self.cord
