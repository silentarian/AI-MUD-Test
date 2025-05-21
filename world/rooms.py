from room import Room

def create_rooms():
  # create the rooms dictionary -> Name, Description
  rooms = {
  'hallway':Room("Hallway","A hallway extends out before you. Eerie paintings cover the walls, each seeming to shift when you're not looking."),
  'library':Room("Library","The library is old and musty. Books cover the room wall to wall, some new and some older than time.  A large desk stands in the middle of the room."),
  'secret_room':Room("Secret Room","You've found it! The secret room! You feel a sense of accomplishment. There is nothing else to do other than type 'quit'"),
  }
  
  # Connect rooms -> Direction, Connecting Room ID
  rooms['hallway'].connect("west","library")
  rooms['library'].connect("east","hallway")
  
  return rooms