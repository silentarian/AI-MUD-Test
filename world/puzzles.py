from print_commands import pprint

def setup_puzzles(rooms):
    # Hallway puzzle to open secret door
    def rotate_painting(target=None):
        pprint("You rotate the painting, and a click sound occurs, opening a secret door to the east!")
        rooms["hallway"].connect("east", "secret_room")

    painting = next((obj for obj in rooms["hallway"].objects if obj.name == "painting 3"), None)
    if painting:
        painting.add_action(["rotate", "turn"], rotate_painting)

