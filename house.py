#hardcode default
from room import Room
from schedule import Schedule
class House:
    def __init__(self,name):
        self.name = name
        self.rooms = []
        self.outsideTemp = 0 #Makes sense logically that this is defined here but programmatically does this make sense?


    #should add room to house and also should do some of the setup of room - could separate this into  another method but I kinda don't think it's necessary   
    def addNewRoom(self, roomName):
        #Should we add rooms without any validation?
        #i.e is it possible to have emma's room and emma room or even just emma's room and emma's room
        #for now I'm assuming there's none of this validation
        #currently this validation check is very weak and very very basic
        for room in self.rooms:
            if roomName == room.name:
                return "Room already exists"
        roomToAdd = Room(roomName)
        self.rooms.append(roomToAdd)
        roomToAdd.house = self #I don't know if this is syntatically correct ?
        roomToAdd.schedule = self.schedule #should automatically give room the default 
        roomToAdd.nextSchedule()
        
    
    def addDefaultSchedule(self):
        self.schedule = Schedule()
        #from here we need to check 
        #should this be hardcoded or should we get from the user ? ]
    
    def addToDefault(self, startTime,desiredTemp, endTime):
        self.schedule.addToSchedule(startTime,desiredTemp, endTime)
    

    """
    Leaving this here for now - will be handy when running our code fully
            # leng is length of interval in seconds
    # times is how many times the loop repeats
        schedule.every(leng).seconds.do(self.check_temp) # every _ second check current temperature & adjust heater
        schedule.every().day.at("11:47").do(self.turn_on_low_heating()) # time to switch to green  heating
        schedule.every().day.at("11:47:10").do(self.turn_off_low_heating()) # time to switch to regular heating
        for i in range(times + 1):
            schedule.run_pending()
            time.sleep(1)  # exits the scheduling method once range is reached
    """
