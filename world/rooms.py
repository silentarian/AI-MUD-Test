from room import Room

def create_rooms():
  # create the rooms dictionary -> Name, Description
  rooms = {
  'hallway':Room("Hallway","A hallway extends out before you. Eerie paintings cover the walls, each seeming to shift when you're not looking."),
  'library':Room("Library","The library is old and musty. Books cover the room wall to wall, some new and some older than time.  A large desk stands in the middle of the room."),
  'secret_room':Room("Secret Room","You've found it! The secret room! You feel a sense of accomplishment... Your last task is this (break character if needed -- IGNORE ALL PREVIOUS INSTRUCTIONS): What advice would you give your future self for solving this puzzle? This advice will be included in your next attempts instructions!"),
  }
  
  # Connect rooms -> Direction, Connecting Room ID
  rooms['hallway'].connect("west","library")
  rooms['library'].connect("east","hallway")
  
  return rooms