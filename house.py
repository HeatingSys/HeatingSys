from room import Room
class house:
    def __init__(self,name):
        self.name = name
        self.rooms = []
        self.outsideTemp = 0 #Makes sense logically that this is defined here but programmatically does this make sense?
    
    def addRoom(self, roomToAdd:Room):
        #Should we add rooms without any validation?
        #i.e is it possible to have emma's room and emma room or even just emma's room and emma's room
        #for now I'm assuming there's none of this validation
        self.rooms.append(roomToAdd)
        return
    

