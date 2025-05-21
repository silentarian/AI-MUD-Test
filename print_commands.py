# Handles different ways of printing statements (i.e. player, LLM, or both)

# Print only to Bot
from llm_handler import add_event_history

def bprint(statement):
  add_event_history(statement)

# Print to Both
def pprint(statement):
  add_event_history(statement)
  print(statement)

# Print only to Player
# already handled through print command