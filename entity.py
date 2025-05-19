class Entity:
  def __init__(self, name, hp, attack_power):
      self.name = name
      self.hp = hp
      self.attack_power = attack_power
      self.in_combat = False
      self.next_attack_tick = None

  def is_alive(self):
      return self.hp > 0

  def take_damage(self, amount):
      self.hp -= amount
      print(f"{self.name} takes {amount} damage! (HP: {self.hp})")
      if self.hp <= 0:
          self.on_death()

  def on_death(self):
      print(f"{self.name} has died.")
      self.in_combat = False
      self.next_attack_tick = None