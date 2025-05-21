# Handles different ways of printing statements (i.e. player, LLM, or both)

# Print locally
def lprint(player, statement):
  if player.type == "Human":
    print(statement)
  elif player.type == "LLM":
    player.add_event_history(statement)

# Print to others
def oprint(player, statement):
  for p in player.party.members:
    if p != player:
      lprint(p, statement)

# Print globally
def gprint(player, statement):
  for p in player.party.members:
    lprint(p, statement)
