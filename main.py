from player import Player
from party import Party
from world import build_world
from command_handler import process_command
from llm import LLM
from time import sleep

PLAYER_INPUT = False

def main():
  Tyrus = Player(name="Tyrus")
  Sylara = LLM(name="Sylara",personality="You are direct and sharp, and catch details that others tend to miss.")
  Caelum = LLM(name="Caelum",personality="You are typically aloof, often getting distracted and talking about larger things instead of focusing on details.")
  party = Party()
  party.add_to_party(Tyrus)
  party.add_to_party(Sylara)
  party.add_to_party(Caelum)
  
  rooms, starting_room_id = build_world()
  for player in party.members:
    player.location = starting_room_id

  # display initial room state, using just one player since this is a global print
  rooms[starting_room_id].display(party.members[0])
  print()

  turn_id = 0
  while True:
    player = party.members[turn_id]
    if player.type == 'Human' and PLAYER_INPUT:
      user_input = input("> ").strip().lower()
      for i in user_input.split(';'):
        output = process_command(player, i, rooms)
        # if output:
        #   print(output)
        #   print()
    elif player.type == "LLM":
      user_input = player.get_response(rooms)
      for i in user_input.split(';'):
        output = process_command(player, i, rooms)
        sleep(2)
        # if output:
        #   bprint(output)
        #   print(output)
        #   sleep(2)

      
    turn_id = turn_id + 1 if turn_id + 1 < len(party.members) else 0
    

if __name__ == "__main__":
  main()