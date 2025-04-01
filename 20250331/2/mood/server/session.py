from .models import Field, Cord, Mob, Player

class GameSession:
    monsters = set()
    users = dict()

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()

    def get_current_monster(self, cord: Cord) -> Mob | None:
        return self.field.get_monster(cord)

    def get_monsters(self):
        return self.monsters

    def add_mob(self, cord: Cord, name: str, message: str, hp: int):
        if not (answer := self.field.add_mob(cord, name, message, hp)) is None:
            self.monsters.add(answer)
        return {"monster": answer, "coords": cord}

    def add_player(self, player_id):
        player = Player(player_id)
        self.users[player_id] = player

    def del_player(self, player_id):
        del self.users[player_id]

    def encounter(self, cord: Cord):
        if self.field.check_cell(cord):
            return self.field.get_monster(cord).name, self.field.get_monster(cord).message

    def move_player(self, player_id, direction: Cord):
        player = self.users[player_id]
        current_cord = player.move(direction)
        if response_monster := self.encounter(player.cord):
            return {"coords": current_cord.to_dict(), "name": response_monster[0], "message": response_monster[1]}
        else:
            return {"coords": current_cord.to_dict(), "name": None, "message": None}

    def attack_monster(self, player_id, name: str, damage: int):
        player = self.users[player_id]
        if self.field.check_cell(player.cord) and (
                monster := self.field.get_monster(player.cord)) and monster.name == name:
            hp_value, damage_value = monster.get_damage(damage)
            if hp_value == 0:
                self.field.del_mob(player.cord)
                self.monsters.remove(monster)
            return {"hp_remain": hp_value, "damage": damage_value, "name": name}
        else:
            return None
