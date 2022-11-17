from room import Room
from schedule import Schedule
from outsideTemp import OutsideTemp


class House:
    def __init__(self,name):
        self.name = name
        self.rooms = []
        self.outsideTemp = OutsideTemp()
        self.defaultSchedule = Schedule()
        self.heatingPower =12
        self.defaultSchedule.addToSchedule('08:00',20,'12:00')
        self.defaultSchedule.addToSchedule('14:00',20,'16:00')
        self.defaultSchedule.addToSchedule('17:00',20,'19:00')


    #should add room to house and also should do some of the setup of room
    def addNewRoom(self, roomName):
        for room in self.rooms:
            if roomName == room.name:
                return "Room already exists"
        roomToAdd = Room(roomName,self.outsideTemp)#pass the object outside temp into 
        self.rooms.append(roomToAdd)
        roomToAdd.defaultSchedule = self.defaultSchedule #should automatically give room the default 
        roomToAdd.checkNextSchedule()
        roomToAdd.outsideTemp = self.outsideTemp
        roomToAdd.heatingPower = self.heatingPower


    #add to default schedule
    def addToDefault(self, startTime, desiredTemp, endTime):
        self.schedule.addToSchedule(startTime, desiredTemp, endTime)

    #call outside temp class 
    def checkOutsideTempPeriodically(self):
        self.outsideTemp.setCurrentOutsideTemp()


    

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

myHouse = House('myhouse')
myHouse.defaultSchedule.addToSchedule('08:00',20,'12:00')
myHouse.defaultSchedule.addToSchedule('14:00',20,'12:00')
myHouse.defaultSchedule.addToSchedule('17:00',20,'12:00')
myHouse.defaultSchedule.addToSchedule('23:00',20,'12:00')
myHouse.addNewRoom('bathroom')

