from player import Player
from party import Party
from print_commands import bprint
from world import build_world
from command_handler import process_command
from llm_handler import get_ai_response


def main():
  Tyrus = Player(name="Tyrus",type="Human")
  Sylara = Player(name="Sylara",type="LLM")
  party = Party()
  party.add_to_party(Tyrus)
  party.add_to_party(Sylara)
  
  rooms, starting_room_id = build_world()
  for player in party.members:
    player.location = starting_room_id

  rooms[starting_room_id].display()
  print()

  turn_id = 0
  while True:
    player = party.members[turn_id]
    if player.type == 'Human':
      user_input = input("> ").strip().lower()
      for i in user_input.split(';'):
        output = process_command(player, i, rooms)
        if output:
          print(output)
          print()
    elif player.type == "LLM":
      user_input = get_ai_response(player, rooms)
      for i in user_input.split(';'):
        output = process_command(player, i, rooms)
        if output:
          bprint(output)
          print()
    else:
      print("Error! User type not defined!")
      break

    if not user_input:
      continue
      
    turn_id = turn_id + 1 if turn_id + 1 < len(party.members) else 0
    

if __name__ == "__main__":
  main()