from object import Object

def populate_objects(rooms):
  rooms["hallway"].objects = [
    Object("Paintings","Four paintings line the wall. They seem to shift and shimmer."),
    Object("Painting 1","Painting 1 shows a fruit basket with eyes in all the fruit.",aliases=['painting1','paintings 1','painting one','painting']),
    Object("Painting 2","Painting 2 shows a swing that somehow seems to sway in a breeze.",aliases=['painting2','paintings 2','painting two']),
    Object("Painting 3","Painting 3 shows a solemn-looking woman in a white cloth hat and wearing a golden cross.",aliases=['painting3','paintings3','painting three']),
    Object("Painting 4","Painting 4 shows a faceless cat, sitting and staring directly at the viewer.",aliases=['painting4','paintings 4','painting four']),
  ]
  
  rooms['library'].objects = [
    Object("Books","Old books line the walls. The languages seem to be of all kinds, yet none of them you know.",["old books","shelves","shelf"]),
    Object("Desk","A sturdy looking desk is covered in documents.",["sturdy desk", "sturdy looking desk"]),
    Object("Documents","A schematic stands out from the rest, dust-free and seeming to have been used recently."),
    Object("Schematics","The schematic is a blueprint of the hallway just outside of the library. Some notes are written over the hallway: 'ROTATE', and 'GOLDEN CROSS'.",["schematic","blueprint"]),
  ]