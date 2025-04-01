from cowsay import list_cows

class Cow:
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
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __add__(self, other):
        return Cord((self.x + other.x) % 10, (self.y + other.y) % 10)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Mob:
    def __init__(self, message, name, hp):
        self.message = message
        self.name = name
        self.hp = hp

    def get_damage(self, hp):
        damage_value = min(hp, self.hp)
        self.hp -= damage_value
        return self.hp, damage_value

    @staticmethod
    def check_name(name):
        return name in list_cows() or name in Cow.custom_cows


class Field:
    def __init__(self):
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, cord, name, message, hp):
        if Mob.check_name(name):
            self.field[cord.x][cord.y] = Mob(message, name, hp)
            return self.field[cord.x][cord.y]
        return None

    def get_monster(self, cord) -> Mob | None:
        return self.field[cord.x][cord.y]

    def del_mob(self, cord):
        self.field[cord.x][cord.y] = None

    def check_cell(self, cord: Cord):
        return not self.get_monster(cord) is None


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cord = Cord()

    def move(self, direction: Cord):
        self.cord = self.cord + direction
        return self.cord
