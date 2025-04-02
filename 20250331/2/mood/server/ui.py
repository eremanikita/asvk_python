from io import StringIO
from cowsay import cowsay, list_cows, read_dot_cow
from .models import Cord, Cow


class UIResponse:
    """Service to provide UI responses for client."""

    @staticmethod
    def move_response(params):
        """Compile response from the provided move params."""
        answer = ""
        answer += f"Moved to {Cord.from_dict(params["coords"])}\n"
        name, message = params["name"], params["message"]
        if name:
            if name in list_cows():
                return cowsay(message, cow=name)
            else:
                return cowsay(message, cowfile=read_dot_cow(StringIO(Cow.custom_cows[name])))
        return answer

    @staticmethod
    def addmob_response(params):
        """Compile response from the provided addmob params."""
        monster, cord = params["monster"], params["coords"]
        if monster:
            return f"Added monster {monster.name} to {cord} saying {monster.message}\n"
        return "Cannot add unknown monster\n"

    @staticmethod
    def attack_response(params):
        """Compile response from the provided attack params."""
        if params:
            answer = f"Attacked {params["name"]}, damage {params["damage"]} hp\n"
            if params["hp_remain"] == 0:
                answer += f"{params["name"]} died\n"
            else:
                answer += f"{params["name"]} now has {params['hp_remain']}\n"
            return answer
        else:
            return "No monster here"


async def send_notifications(users, message, exception: str):
    """Async function to send notifications all users except one."""
    for queue in users.keys():
        if queue != exception:
            await users[queue].put(message)
