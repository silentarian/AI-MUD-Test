# --- command_handler.py ---
from os import wait
from httpx import get
from player import Player
from llm_handler import add_event_history, get_ai_response, pprint
from time import sleep


PLAYER_TYPE = 'LLM' # human or LLM

COMMAND_ALIASES = {
    "n": "move", "north": "move",
    "s": "move", "south": "move",
    "e": "move", "east": "move",
    "w": "move", "west": "move",
    "go": "move",
    "look": "look", "l": "look",
    "attack": "attack", "a": "attack",
    "quit": "quit", "exit": "quit"
}

DIRECTION_ALIASES = {
    "n": "north", "north": "north",
    "s": "south", "south": "south",
    "e": "east",  "east": "east",
    "w": "west",  "west": "west"
}

def handle_move(player, arg, rooms):
    direction = DIRECTION_ALIASES.get(arg, arg)
    player.move(direction, rooms)

def handle_look(player, arg, rooms):
    if arg:
        if arg.split(' ')[0] == "at":
            arg = arg[3:]
        if arg in rooms[player.location].objects:
            pprint(f"You look at {arg}.")
            pprint(rooms[player.location].objects[arg])
        elif arg in rooms[player.location].exits:
            pprint(f"You peer {arg} to see: " + rooms[player.location].exits[arg])
        else:
            pprint("You don't see that here.")
    else:
        rooms[player.location].display()

def handle_quit(*_):
    print("Thanks for playing!")
    return True

def handle_say(player, args, rooms):
    pprint(f"Sylara says: {args}")

def command_handler(player: Player, rooms):
    rooms[player.location].display()

    # Command dispatch table
    command_map = {
        "move": handle_move,
        "look": handle_look,
        "quit": handle_quit,
        "say": handle_say,
    }

    while True:
        if PLAYER_TYPE == 'human':
            user_input = input("> ").strip().lower()
        elif PLAYER_TYPE == 'LLM':
            user_input = get_ai_response(player, rooms)
            print("Sylara input: " + user_input)
        else:
            print("Error! User type not defined in command_handler")
            break

        if not user_input:
            continue

        # Check for room-specific custom command first
        if user_input in rooms[player.location].custom_commands:
            rooms[player.location].custom_commands[user_input]()
            #result = rooms[player.location].custom_commands[user_input]()
            #print(result() if callable(result) else result)
            continue

        # Parse input into command and argument
        if " " in user_input:
            verb, arg = user_input.split(" ", 1)
        else:
            verb, arg = user_input, ""

        # Normalize command
        command = COMMAND_ALIASES.get(verb, verb)

        # If the player typed just a direction (e.g. "n"), use it as the arg too
        if command == "move" and not arg:
            arg = verb

        # Dispatch if available
        handler = command_map.get(command)
        if handler:
            should_quit = handler(player, arg, rooms)
            if should_quit:
                break      

        else:
            pprint("Command not recognized.")

        if PLAYER_TYPE == 'LLM':
            sleep(4)

        print()


