import shlex
from .models import Cord, Weapon


class ParserService:
    required_keys = {"name", "hello", "hp", "coords"}

    @staticmethod
    def parse_addmob(line: str):
        tokens = shlex.split(line)
        params = {"name": tokens[0]}
        i = 1
        token_length = len(tokens)
        while i < token_length:
            if tokens[i] == "hello":
                if i + 1 < token_length:
                    params["hello"] = tokens[i + 1]
                i += 2
            elif tokens[i] == "hp":
                if i + 1 < len(tokens) and tokens[i + 1].isdigit() and int(tokens[i + 1]) > 0:
                    params["hp"] = int(tokens[i + 1])
                i += 2
            elif tokens[i] == "coords":
                if i + 2 < len(tokens) and tokens[i + 1].isdigit() and tokens[i + 2].isdigit():
                    params["coords"] = Cord(int(tokens[i + 1]), int(tokens[i + 2])).to_dict()
                i += 3
            else:
                i += 1

        return params if not (ParserService.required_keys - params.keys()) else None

    @staticmethod
    def parse_attack(line):
        tokens = shlex.split(line)
        if len(tokens) == 0:
            print("Invalid command")
        else:
            if len(tokens) == 3 and tokens[1] == "with":
                weapon_name = tokens[2].upper()
            else:
                weapon_name = Weapon.SWORD.name

            if any(weapon_name == i.name for i in Weapon):
                return tokens[0], Weapon[weapon_name].value
            else:
                print("Unknown weapon")
        return -1
