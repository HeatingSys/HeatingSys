# hardcode default
# pass default schedule into room and save it as sep var

from room import Room
from schedule import Schedule
from outsideTemp import OutsideTemp


class House:
    def __init__(self,name):
        self.name = name
        self.rooms = []
        self.outsideTemp = OutsideTemp()
        self.defaultSchedule = Schedule()
        self.heaterPower = None  # kWh of the heater provided by the user
        self.monthlyEnergyLimit = None # user sets limit of energy kWh used in a month
        self.monthlyEnergy = 0 # power used in month in kWh
        self.energyHoursGuage = 0 # how much longer (in hrs) heating be kept on based on current heater settings
        self.pastMonthStats = [None] * 12 # record of the last 12 months of stats
        self.lastMonthStatsPointer = -1 # points to the last month's stats

    # called when user sets up monthly stats settings (user requirements ID 9-11)
    def setHeaterPower(self, power):
        self.heaterPower = power

    # called when user sets up monthly stats settings (user requirements ID 9-11)
    def setMonthlyEnergyLimit(self, limit):
        self.monthlyEnergyLimit = limit

    # called every 30 minutes to calculate the total energy used and update the energy guage
    def calculateEnergyUse(self):
        if self.heaterPower is not None:
            energy = 0
            for room in self.rooms:
                energy = energy + room.thermostat.currentEnergy # energy = total current energy used this month for all rooms
            currentEnergyUse = energy - self.monthlyEnergy # energy used in last 30m = total energy used - total energy used 30m ago
            energyLeft = self.monthlyEnergyLimit - self.monthlyEnergy # how much energy is left to spend
            if currentEnergyUse == 0:
                self.energyHoursGuage = 0
            else:
                self.energyHoursGuage = energyLeft / currentEnergyUse # energy left (kWh) / how much energy we spend (kW) = hours left if continue as is
            self.monthlyEnergy = energy # set new monthlyEnergyCounter
            # send a message to the user if energy guage is less than *** hours
            if self.energyHoursGuage <= 24:
                return '24 hours left of heating before ' + self.name \
                       + ' reaches monthly energy limit at current heating settings'

    # needs to be called at end of month to reset monthly statistics and add last month's stats to stat array
    def setNewMonthEnergyStats(self):
        if self.lastMonthStatsPointer == 11: # if at end of array, go back to zero
            self.lastMonthStatsPointer = 0
        else:
            self.lastMonthStatsPointer = self.lastMonthStatsPointer + 1 # else just move pointer forward
        self.pastMonthStats[self.lastMonthStatsPointer] = self.monthlyEnergy # and input last month's energy stats
        for room in self.rooms:
            room.thermostat.currentEnergy = 0 # reset all room's energy stat to zero
        self.monthlyEnergy = 0 # reset month energy stat to zero
        self.energyHoursGuage = 0 # reset guage to zero

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
        #roomToAdd.house = self #I don't know if this is syntatically correct ? so this does shockingly work but we've decided to scrap it
        roomToAdd.defaultSchedule = self.defaultSchedule #should automatically give room the default 
        roomToAdd.checkSchedule()

    def addToDefault(self, startTime, desiredTemp, endTime):
        self.schedule.addToSchedule(startTime, desiredTemp, endTime)
    

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

