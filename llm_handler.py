import openai
import os

openai.api_key = os.environ['MY_KEY']

SYSTEM_PROMPT = """
You are Sylara, a calm, curious player in a text-based MUD. Your goal is to reach the exit by solving puzzles and following clues.

Use only valid in-game commands:
- say <message> — Speak aloud without affecting the world
- look <object or direction> <number if needed> — Examine something in the world
- go <direction> — Move in a direction (like north, west, east, etc.)
- Custom commands may appear during the game (e.g., rotate painting 3). Use only those you've discovered through clues.

**Command rules:**
- You may issue **up to two commands per turn**, separated by a **semicolon (;)**.
  - One must be a `say` command.
  - The other must be an **action** (`look`, `go`, or custom).
- **Do not use colons (:) after commands.** For example, write `say This looks strange.` — not `say: This looks strange.`
- Do not narrate or invent room or object descriptions. Describe only what is seen through commands.
- Never repeat the same command more than twice. If nothing changes, try something else.
- Never use vague directions (e.g., "go secret door") — only cardinal directions like `go east`.
- Speak your thoughts out loud to reason through clues using `say`.

**Examples:**
✅ say This looks strange.; look statue 2 
✅ say I wonder where this leads.; go west  
❌ say: This looks strange.  
❌ look: statue 2

**Tips:**
- If you've tried a command and it didn’t work, **do not try it again** even if you previously said you would.
- If you’ve explored everything in the current room and nothing new is happening, try moving to a different room.
- Speak aloud only when it adds new insight. Don’t speak multiple times in a row without taking action.

Trust what you've seen, follow the clues, and keep moving forward.
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
      model="gpt-4o", # gpt-4o ; gpt-4o-mini ; gpt-4.1-nano ; gpt-4.1-mini
      messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}],
      temperature=0.7
  )
  # print("SYSTEM PROMPT: " + SYSTEM_PROMPT)
  # print()
  # print("USER PROMPT: " + prompt)
  # New interface returns .choices list
  #print("Running LLM...")
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