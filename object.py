
class Object:
  def __init__(self, name, description, aliases=[], visible=False, pickupable=False, functions=None):
      self.name = name.lower()
      self.description = description
      self.visible = visible
      self.pickupable = pickupable
      self.aliases = aliases if aliases else []
      self.verbs = {} # verb -> function (e.g. "rotate": self.rotate_painting)

  def matches(self, input_name):
    input_name = input_name.lower()
    return input_name == self.name or input_name in self.aliases

  def __repr__(self):
    return f"<GameObject: {self.name}>"

  def add_action(self, verbs, function):
    if isinstance(verbs, str):
      verbs = [verbs]
    for verb in verbs:
      self.verbs[verb] = function

  def interact(self, verb, target=None):
    if verb in self.verbs:
      return self.verbs[verb](target)
    return f"You can't {verb} {self.name}."

