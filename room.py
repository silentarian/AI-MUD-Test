from llm_handler import pprint

class Room:
  def __init__(self, room_id, name, description):
    self.id = room_id
    self.name = name
    self.description = description
    self.exits = {} # direction -> room_id
    self.objects = {} # object_name -> description
    self.custom_commands = {} # command string -> function or result string

  def connect(self, direction, room_id):
    self.exits[direction] = room_id

  def get_exit(self, direction):
    return self.exits.get(direction, None)

  def display(self):
    print(f"\n{self.name}")
    print(self.description)
    print("Exits: " + ", ".join(self.exits.keys()))

  def handle_custom_command(self, command):
    return self.custom_commands.get(command.lower(), None)
