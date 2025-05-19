import openai
import os

openai.api_key = os.environ['MY_KEY']

SYSTEM_PROMPT = """
You are playing as Sylara, a player in a text-based MUD. You are calm, insightful, and speak with curiosity and care. You will be acting on your own in this game.
Your goal is to reach the exit.

You may only respond using MUD-style game commands such as:
- say <message>: say something out loud, but does not interact with the world
- look <object or direction> <number, if more than one of that object>: look at an object more closely
- go <direction>: move in the direction of an exit

(Do not include <> marks in your response.)
(Use singular form for numbered items: e.g. look object 1, NOT look objects 1)

Exits for your room are given in the user prompt. You are also given an event history to provide you with context of what has happened in recent history.
Do not repeat the same action over and over gain. There is no point.
The event history is just for context and problem solving. You will need to return to previous rooms to find items you've looked at before.

Some rooms have special commands which you will have to discover for yourself.
Do not narrate. Do not break character. Only use valid commands. Use only one command at a time. You cannot use two commands in the same line.
You are encouraged to speak out loud to express your thoughts to yourself.

Saying something only does that. You will have to interact with the world through other commands. When in doubt, explore around to see if you learn anything new.
Do NOT create your own descriptions for rooms. The world is created, and you are a player in the world. Only use commands like shown above.
"""

event_history = []
MAX_EVENTS = 100

def build_prompt(player, rooms):
  room = rooms[player.location]

  user_prompt = f"""
  Room: {room.name}
  Room description: {room.description}
  Exits: {', '.join(room.exits)}

  Event history:
  """
  user_prompt += '\n'.join(event_history)
  
  return user_prompt

def query_llm(prompt: str) -> str:
  response = openai.chat.completions.create(
      model="gpt-4o", # gpt-4.1-nano ; gpt-4o
      messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}],
      temperature=0.7
  )
  # print("SYSTEM PROMPT: " + SYSTEM_PROMPT)
  # print()
  # print("USER PROMPT: " + prompt)
  # New interface returns .choices list
  print("Running LLM...")
  return response.choices[0].message.content.strip()

def add_event_history(event):
  global event_history
  event_history.append(event)
  if len(event_history) > MAX_EVENTS:
    event_history = event_history[-MAX_EVENTS:]

def get_ai_response(player, rooms):
  user_prompt = build_prompt(player, rooms)
  response = query_llm(user_prompt)
  return response

def pprint(statement):
  add_event_history(statement)
  print(statement)