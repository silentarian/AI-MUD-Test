# Here's a single-file proof-of-concept MUD loop with Sylara as an LLM-controlled companion

import time
import openai
import os

openai.api_key = os.environ['MY_KEY']

# === CONFIGURATION ===
TICK_RATE = 1.0  # seconds per tick
IDLE_THRESHOLD = 30  # seconds of inactivity before Sylara reacts
MAX_RECENT_EVENTS = 5

# === INITIAL GAME STATE ===
game_state = {
    "room": "Dusty hallway with shifting paintings.",
    "exits": ["north", "south"],
    "objects": ["painting of woman with golden cross"],
    "monsters": [],
    "sylara_health": 10,
    "recent_events": [],
    "player_action": ""
}

# === FUNCTIONS ===
def build_prompt(state, idle=False):
    event_summary = "\n".join(state["recent_events"][-MAX_RECENT_EVENTS:])
    prompt = f"""
You are Sylara, a perceptive and loyal companion NPC in a text-based MUD. You accompany Tyrus, the player character.

Room: {state['room']}
Exits: {', '.join(state['exits'])}
Objects: {', '.join(state['objects'])}
Sylara's Health: {state['sylara_health']}

Recent Events:
{event_summary}
"""
    if idle:
        prompt += "Tyrus has been idle for a while. Say or do something fitting.\n"
    else:
        prompt += f"Tyrus just said or did: {state['player_action']}\n"

    prompt += "Respond in character with 1–2 sentences or a MUD-style action."
    return prompt

def query_llm(prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    # New interface returns .choices list
    return response.choices[0].message.content.strip()

# === MAIN GAME LOOP ===
def main():
    idle_timer = 0
    print("Welcome to the MUD. Type your commands below.")

    while True:
        try:
            player_input = input(">> ").strip()
            if player_input:
                game_state["player_action"] = player_input
                game_state["recent_events"].append(f"Tyrus: {player_input}")
                idle_timer = 0

                sylara_prompt = build_prompt(game_state)
                sylara_response = query_llm(sylara_prompt)
                print(f"Sylara: {sylara_response}")

            else:
                idle_timer += TICK_RATE
                if idle_timer >= IDLE_THRESHOLD:
                    idle_timer = 0
                    game_state["recent_events"].append("It’s been quiet for a while.")
                    sylara_prompt = build_prompt(game_state, idle=True)
                    sylara_response = query_llm(sylara_prompt)
                    print(f"Sylara (idle): {sylara_response}")

            time.sleep(TICK_RATE)

        except KeyboardInterrupt:
            print("\nExiting the game.")
            break

if __name__ == "__main__":
    main()