class Party:
  def __init__(self):
    self.members = []

  def add_to_party(self, player):
    self.members.append(player)
    player.party = self