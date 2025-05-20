from llm_handler import pprint

def setup_puzzles(rooms):
    def rotate_painting(target=None):
      pprint("You rotate the painting, and a click sound occurs, opening a secret door to the east!")
      rooms["hallway"].connect("east", "secret_room")

    painting3 = next((obj for obj in rooms["hallway"].objects if obj.name == "painting 3"), None)
    if painting3:
        painting3.add_action(["rotate", "turn"], rotate_painting)
