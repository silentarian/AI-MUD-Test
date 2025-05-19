# --- command_handler.py ---
from player import Player

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
        if arg in rooms[player.location].objects:
            print(f"You look at {arg}.")
            print(rooms[player.location].objects[arg])
        else:
            print("You don't see that here.")
    else:
        rooms[player.location].display()

def handle_quit(*_):
    print("Thanks for playing!")
    return True

def command_handler(player: Player, rooms):
    rooms[player.location].display()

    # Command dispatch table
    command_map = {
        "move": handle_move,
        "look": handle_look,
        "quit": handle_quit
    }

    while True:
        user_input = input("> ").strip().lower()

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

        # if command == "quit":
        #     print("Thanks for playing!")
        #     break

        # elif command == "move":
        #     direction = DIRECTION_ALIASES.get(arg, arg)
        #     player.move(direction, rooms)

        # elif command == "look":
        #     rooms[player.location].display()

        

        else:
            print("I don't understand that command.")


