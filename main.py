from player import Player
from world import build_world
from command_handler import command_handler

def main():
  player = Player(name="Thorin Oakenshield")
  rooms, starting_room_id = build_world()
  player.location = starting_room_id

  command_handler(player, rooms)




if __name__ == "__main__":
  main()