from cowsay import cowsay


class Mob:
    def __init__(self, message, name):
        self.message = message
        self.name = name

    def say(self):
        print(cowsay(self.message, cow=self.name))


class Field:
    def __init__(self):
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, cord, name, message):
        self.field[cord.x][cord.y] = Mob(message, name)
        print(f"Added monster {name} to ({cord.x}, {cord.y}) saying {message}")


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Player:
    def __init__(self):
        self.cord = Cord()

    def move(self, direction):
        match direction:
            case "up":
                self.cord = Cord(self.cord.x, (self.cord.y - 1) % 10)
            case "down":
                self.cord = Cord(self.cord.x, (self.cord.y + 1) % 10)
            case "left":
                self.cord = Cord((self.cord.x - 1) % 10, self.cord.y)
            case "right":
                self.cord = Cord((self.cord.x + 1) % 10, self.cord.y)
        print(f"Moved to {self.cord}")


class Game:
    def __init__(self):
        self.field = Field()
        self.player = Player()

    def add_mob(self, cord, name, message):
        self.field.add_mob(cord, name, message)

    def encounter(self):
        if self.field.field[self.player.cord.x][self.player.cord.y] is not None:
            self.field.field[self.player.cord.x][self.player.cord.y].say()

    def move_player(self, direction):
        self.player.move(direction)
        self.encounter()


def main():
    game = Game()
    while line := input():
        args = line.split()
        match args[0]:
            case "up" | "down" | "left" | "right" as direction:
                game.move_player(direction)
            case "addmob":
                if len(args[1:]) != 4:
                    print("Invalid arguments")
                else:
                    name, x, y, message = args[1:]
                    game.add_mob(Cord(int(x), int(y)), name, message)
            case _:
                print("Invalid command")


if __name__ == "__main__":
    main()
