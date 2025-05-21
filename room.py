from print_commands import gprint

class Room:
  def __init__(self, name, description):
      self.name = name
      self.description = description
      self.exits = {}
      self.objects = []  # Now a list of GameObjects
      self.custom_commands = {}

  def connect(self, direction, room_id):
      self.exits[direction] = room_id

  def get_exit(self, direction):
      return self.exits.get(direction, None)

  def display(self, player):
      gprint(player, f"\n{self.name}")
      gprint(player, self.description)
      gprint(player, "Exits: " + ", ".join(self.exits.keys()))
      visible_objects = [obj.name for obj in self.objects if obj.visible]
      if visible_objects:
          gprint(player, "You see: " + ", ".join(visible_objects))

  def find_object(self, name):
      for obj in self.objects:
          if obj.matches(name):
              return obj
      return None

  def handle_custom_command(self, command):
      return self.custom_commands.get(command.lower(), None)