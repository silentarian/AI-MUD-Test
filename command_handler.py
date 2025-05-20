# --- command_handler.py ---
from os import wait
from httpx import get
from player import Player
from llm_handler import add_event_history, get_ai_response, pprint
from time import sleep

command_count = {}
MAX_REPEATED_BEFORE_HINT = 3

PLAYER_TYPE = 'human' # human or LLM

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

INTERACTION_VERBS = ["rotate","turn","place","push","pull"]

def handle_move(player, arg, rooms):
    direction = DIRECTION_ALIASES.get(arg, arg)
    player.move(direction, rooms)

def handle_look(player, arg, rooms):
    room = rooms[player.location]
    if arg and arg not in ['around']:
        # strip off "at" if user typed "look at <object>"
        if arg.split(' ')[0] == "at":
            arg = arg[3:]

        # try to find the object using alias matching
        obj = room.find_object(arg)
        if obj:
            pprint(f"{player.name} looks at {obj.name}.")
            pprint(obj.description)
            return

        # check if player is looking in a direction
        if arg in room.exits:
            pprint(f"{player.name} peers {arg} to see: {room.exits[arg]}")
            return
        
        # fallback message
        else:
            pprint(f"{player.name} doesn't see {arg} here.")
    else:
        room.display()

def handle_quit(*_):
    print("Thanks for playing!")
    return True

def handle_say(player, args, rooms):
    pprint(f"Sylara said: {args}")

def handle_interact_command(player, verb, arg, rooms):
    current_room = rooms[player.location]

    obj = current_room.find_object(arg)
    if not obj:
        pprint("You don't see {obj} here.")
        return

    result = obj.interact(verb)
    if result:
        pprint(result)


def command_handler(player: Player, rooms):
    rooms[player.location].display()

    # Command dispatch table
    command_map = {
        "move": handle_move,
        "look": handle_look,
        "quit": handle_quit,
        "say": handle_say,
    }

    repeat_count = 0
    last_command = None

    total_round_count = 0

    while True:
        if PLAYER_TYPE == 'human':
            user_input = input("> ").strip().lower()
        elif PLAYER_TYPE == 'LLM':
            user_input = get_ai_response(player, rooms)
            #print("Sylara input: " + user_input)
        else:
            print("Error! User type not defined in command_handler")
            break

        if not user_input:
            continue

        # Split commands up by semicolon
        input_queue = user_input.split(';')
        for user_input in input_queue:

            user_input = user_input.strip()
            # Check for room-specific custom command first
            if user_input in rooms[player.location].custom_commands:
                rooms[player.location].custom_commands[user_input]()
                continue
    
            # Parse input into command and argument
            if " " in user_input:
                verb, arg = user_input.split(" ", 1)
            else:
                verb, arg = user_input, ""
    
            # Normalize command
            command = COMMAND_ALIASES.get(verb, verb)
            handler = command_map.get(command)

            # If the player typed just a direction (e.g. "n"), use it as the arg too
            if command == "move" and not arg:
                arg = verb

            # Check if interaction command
            if command in INTERACTION_VERBS:
                handle_interact_command(player, command, arg, rooms)
    
            # Dispatch if available
            elif handler:
                should_quit = handler(player, arg, rooms)
                if should_quit:
                    break
    
            else:
                pprint(f"Sylara tried: {command}. This command is invalid.")
    
            # Help prevent repeated commands
            if command not in command_count:
                command_count[command] = 0
            command_count[command] += 1
            if repeat_count > 3:
                pprint("**You feel like you've already tried that. Maybe it's time to explore elsewhere?**")
            else:
                command_count[command] = 0

        if PLAYER_TYPE == 'LLM':
            total_round_count += 1
            print("Round: " + str(total_round_count))
            sleep(1)

        print()


