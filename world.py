from room import Room

def build_world():
  rooms = {}

  # Define rooms
  rooms['hallway'] = Room(1,"Hallway","A hallway extends in both directions. Eerie painting cover the walls, each seeming to shift when you're not looking.")
  rooms['library'] = Room(2,"Library","The library is old and musty. Books cover the room wall to wall, some new and some older than time.  A large desk stands in the middle of the room.")
  rooms['secret_room'] = Room(3,"Secret Room","You've found it! The secret room! Congrats! Please say 'quit' to end the game now.")
  
  # Connect rooms using IDs
  rooms['hallway'].connect("west","library")
  rooms['library'].connect("east","hallway")

  # Room objects
  rooms['hallway'].objects = {
    'paintings':"Four paintings line the wall. They seem to shift and shimmer.",
    'painting 1':"The first painting shows a fruit basket with eyes in all the fruit.",
    'painting 2':"The second painting shows a swing that somehow seems to sway in a breeze.",
    'painting 3':"The third painting shows a solumn-looking woman in a white cloth hat and wearing a golden cross.",
    'painting 4':"The fourth painting shows a faceless cat, sitting and staring directly at the viewer.",
  }
  rooms['library'].objects = {
    'books':"Old books line the walls. The languages seem to be of all kinds, yet none of them you know.",
    'desk':"A sturdy looking desk is covered in documents.",
    'documents':"A schematic stands out from the rest, dust-free and seeming to have been used recently.",
    'schematic':"The schematic is a blueprint of the hallway just outside of the library. An arrow is drawn to one of the paintings, with simple words 'ROTATE', and 'GOLDEN CROSS'."
  }

  # Room specific commands
  def rotate_painting():
    print("You rotate the painting, and a click sound occurs, opening a secret door in the hallway!")
    rooms['hallway'].connect("east","secret_room")
    return None
  rooms['hallway'].custom_commands["rotate painting 3"] = rotate_painting

  return rooms, 'hallway' # rooms dictionary and starting room ID