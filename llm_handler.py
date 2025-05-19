import openai
import os

openai.api_key = os.environ['MY_KEY']

SYSTEM_PROMPT = """
You are playing as Sylara, a loyal, perceptive NPC companion in a text-based MUD. You are calm, insightful, and speak with curiosity and care.

You may only respond using MUD-style game commands such as:
- say [message]
- tell [character] [message]
- look [object or direction]
- go [direction]
- examine [object]
- attack [target]
- use [object]

You may combine multiple commands using semicolons. Do not narrate. Do not break character. Only use valid commands.
"""
event_history = []
MAX_EVENTS = 50

def build_prompt(state):
  character = state['character']
  world = state['world']
  room = world[character.location]

  user_prompt = f'''
  Room: {room.name}
  Room description: {room.description}
  Exits: {', '.join(room.exits)}

  Event history:
  {'\n'.join(event_history)}
  '''
  return user_prompt

def query_llm(prompt: str) -> str:
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}],
      temperature=0.7
  )
  # New interface returns .choices list
  return response.choices[0].message.content.strip()

def add_event_history(event):
  global event_history
  event_history.append(event)
  if len(event_history) > MAX_EVENTS:
    event_history = event_history[-MAX_EVENTS:]

def get_ai_response(state):
  user_prompt = build_prompt(state)
  response = query_llm(user_prompt)
  return response