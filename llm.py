from player import Player
import openai
import os

openai.api_key = os.environ['MY_KEY']

MAX_EVENTS = 50

SYSTEM_PROMPT = """
You are playing as one member of your party. Work together but act and speak according to your personality!
Be sure to talk to your fellow team members. Engage in meaningful dialogue. Occasionally use each others' names when talking.
You can see what other players are doing, but not what they see or think. Be sure to communicate what's important.

Use only valid in-game commands:
- say <message> — Speak aloud without affecting the world
- look <object or direction> <number if needed> — Examine something in the world
- go <direction> — Move in a direction (like north, west, east, etc.) - Note that this will move the whole party, not just you.
- Custom commands may appear during the game (e.g., rotate painting 3). Use only those you've discovered through clues.

**Command rules:**
- You may issue **up to two commands per turn**, separated by a **semicolon (;)**.
  - One must be a `say` command.
  - The other must be an **action** (`look`, `go`, or custom).
- **Do not use colons (:) after commands.** For example, write `say This looks strange.` — not `say: This looks strange.`
- Do not narrate or invent room or object descriptions. Describe only what is seen through commands.
- Never repeat the same command more than twice. If nothing changes, try something else.
- Never use vague directions (e.g., "go secret door") — only cardinal directions like `go east`.
- Communicate your thoughts when appropriate by using `say`.

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

class LLM(Player):
  def __init__(self, name, personality):
    super().__init__(name=name,type="LLM")
    self.personality = personality
    self.history = []
    self.instructions = f"Your name is {self.name}. Your personality is: {self.personality}."
    self.instructions += SYSTEM_PROMPT

  def add_event_history(self, event):
    self.history.append(event)
    if len(self.history) > MAX_EVENTS:
      self.history = self.history[-MAX_EVENTS:]

  def build_prompt(self, rooms):
    room = rooms[self.location]

    user_prompt = f"""
    **Current Room**
    Room: {room.name}
    Room description: {room.description}
    Exits: {','.join(room.exits)}

    **Event History**
    """
    user_prompt += '\n'.join(self.history)

    return user_prompt

  def query_llm(self,prompt:str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o", # gpt-4o ; gpt-4o-mini ; gpt-4.1-nano ; gpt-4.1-mini
        messages=[
          {"role": "system", "content": self.instructions},
          {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

  def get_response(self, rooms):
    prompt = self.build_prompt(rooms)
    response = self.query_llm(prompt)
    return response
      