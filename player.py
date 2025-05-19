# --- player.py ---

from entity import Entity
from llm_handler import pprint
import random

class Player(Entity):
    def __init__(self, name):
        super().__init__(name, hp=100, attack_power=10)
        self.stats = {
            "str": 10, "dex": 10, "con": 10,
            "int": 10, "wis": 10, "cha": 10
        }
        self.inventory = []
        self.location = None
        self.targets = []  # List of Monster objects

    def move(self, direction, rooms):
        current_room = rooms[self.location]
        next_room_id = current_room.get_exit(direction)
        if next_room_id and next_room_id in rooms:
            self.location = next_room_id
            pprint(f"You move {direction}.")
            rooms[self.location].display()
        else:
            pprint("You can't go that way.")

    def attack_target(self):
        if not self.targets:
            return

        # Only attack targets in the same room
        valid_targets = [m for m in self.targets if m.is_alive() and m.location == self.location]

        if not valid_targets:
            pprint(f"{self.name} has no valid targets in the room. Combat paused.")
            self.in_combat = False
            return

        self.in_combat = True  # Reaffirm combat is ongoing
        target = random.choice(valid_targets)
        pprint(f"{self.name} attacks {target.name}!")
        target.take_damage(self.attack_power)
