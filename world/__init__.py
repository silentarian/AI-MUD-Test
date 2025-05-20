from .rooms import create_rooms
from .objects import populate_objects
from .puzzles import setup_puzzles

def build_world():
  rooms = create_rooms()
  populate_objects(rooms)
  setup_puzzles(rooms)
  return rooms, "hallway"