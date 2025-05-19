
class Object:
  def __init__(self, name, description, aliases=[], visible=False, pickupable=False, functions=None):
      self.name = name.lower()
      self.description = description
      self.visible = visible
      self.pickupable = pickupable
      self.aliases = aliases if aliases else []
      self.functions = functions if functions else {}

  def matches(self, input_name):
    input_name = input_name.lower()
    return input_name == self.name or input_name in self.aliases

  def __repr__(self):
    return f"<GameObject: {self.name}>"