import sys
sys.path.insert(0, "src")
from room import Room
from schedule import Schedule
from outsideTemp import OutsideTemp
from datetime import datetime


class House:
    def __init__(self):
        self.rooms = []
        self.outsideTemp = OutsideTemp()
        self.defaultSchedule = Schedule()

        self.heatingPower = None  # kWh of the heater provided by the user
        self.monthlyEnergyLimit = None # user sets limit of energy kWh used in a month
        self.monthlyEnergy = 0 # power used in month in kWh
        self.energyHoursGuage = 0 # how much longer (in hrs) heating be kept on based on current heater settings
        self.monthlyEnergyExceeded = False
        self.pastMonthStats = {"January": None, "February": None, "March": None, "April": None, "May": None,
                               "June": None, "July": None, "August": None, "September": None, "October": None,
                               "November": None, "December": None}  # record of the last 12 months of stats
        self.defaultSchedule.addToSchedule('00:00',15,'06:59')
        self.defaultSchedule.addToSchedule('07:00',21,'09:00')
        self.defaultSchedule.addToSchedule('17:00',22,'22:00')

    def getRoom(self, room_id):
        for room in self.rooms:
            if room.id == room_id:
                return room
    
    def deleteRoom(self, room_id):
        room = self.getRoom(room_id)
        self.rooms.remove(room)

    def getAllRooms(self):
        for room in self.rooms:
            print(room.id)
            
    # called when user sets up monthly stats settings (user requirements ID 9-11)
    def setHeatingPower(self, power):
        self.heatingPower = power

        for room in self.rooms:
            room.heatingPower = power

    # called when user sets up monthly stats settings (user requirements ID 9-11)
    def setMonthlyEnergyLimit(self, limit):
        self.monthlyEnergyLimit = limit
    
    def getMonthlyEnergyLimit(self):
        return self.monthlyEnergyLimit

    # getter methods for monthly stats
    def getMonthlyEnergy(self):
        if self.monthlyEnergy == 0:
            return "No data yet"
        else:
            return self.monthlyEnergy

    def getEnergyHoursGuage(self):
        if self.energyHoursGuage == 0:
            return "No data yet"
        else:
            return self.energyHoursGuage

    def getMonthlyEnergyExceeded(self):
        if self.monthlyEnergyExceeded is False:
            return "Not exceeded"
        else:
            return "Exceeded"

    def getPastMonthStats(self):
        return self.pastMonthStats

    # called every 30 minutes to calculate the total energy used and update the energy guage
    def calculateEnergyUse(self):
        if self.heatingPower is not None:
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
            if self.monthlyEnergy > self.monthlyEnergyLimit:
                self.monthlyEnergyExceeded = True

    # needs to be called at end of month to reset monthly statistics and add last month's stats to stat array
    def resetNewMonthEnergyStats(self):
        pastMonth = datetime.now().strftime("%B")
        self.pastMonthStats[pastMonth] = self.monthlyEnergy
        for room in self.rooms:
            room.thermostat.currentEnergy = 0  # reset all room's energy stat to zero
        self.monthlyEnergy = 0  # reset month energy stat to zero
        self.energyHoursGuage = 0  # reset guage to zero
        self.monthlyEnergyExceeded = False  # reset measure to False

    #should add room to house and also should do some of the setup of room
    def addNewRoom(self, room_id):
        for room in self.rooms:
            if room_id == room.id:
                return "Room already exists"
        roomToAdd = Room(room_id,self.outsideTemp)#pass the object outside temp into 
        self.rooms.append(roomToAdd)
        roomToAdd.defaultSchedule = self.defaultSchedule #should automatically give room the default
        roomToAdd.heatingPower = self.heatingPower

    #add to default schedule
    def addToDefault(self, startTime, desiredTemp, endTime):
        self.schedule.addToSchedule(startTime, desiredTemp, endTime)

    #call outside temp class 
    def checkOutsideTempPeriodically(self):
        self.outsideTemp.setCurrentOutsideTemp()
