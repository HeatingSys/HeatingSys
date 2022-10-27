# Basic structure of room for history 3 
#import schedule
#**Need to add more checks for whether schduele exists throughout the code 

import time
from heater import thermostat
from schedule import Schedule
class Room:
    def __init__(self, temp1,name):
        self.name =name
        self.automated = False #Is this what was previously our 'automated'?
        self.desiredTemp = None #should start out empty
        self.currentTemp = 12 # we need to get our heater/thermostat class before being able to define this properly
        self.roomschedule ='hi'  #want to change this to include house default
        self.currentTime ='12:00' # should be a read from now() - for testing purposes leaving this alone rn
        self.heatingRunning = False #states whether heating is on now or nah
        self.nextSchedule = None
        self.thermomstat = thermostat 
        self.defaultSchedule = True #this is by default on can manually turn it off
        self.tempHistory = {} #should this be empty at the start, also is this temp before or after heating is turned on



    #QUESTION is this turning off temp??
    #Or is it like energy saving mode of heating on

    def turnScheduleToDefault(self):
        self.schedule = self.house.schedule

    def turnOffScheduling(self):
        self.schedule.scheduleOn = False


    # method specifies when to kick in scheduled heating
    # leng is length of interval in seconds
    # times is how many times the loop repeats
    def scheduling(self):
        if self.roomSchedule.scheduleOn is True: #if schedule is on
            #first need to get info about the schedule
            info = self.roomSchedule.schedule[self.nextSchedule] #this is single handedly the worst thing iv'e seen in my life#
            self.desiredTemp = info[0]
            self.takeTempReading()
            self.tempHistory.pop(0)
            self.tempHistory.append(self.currentTemp)
            if self.desiredTemp == self.currentTemp():
                return 'No need to turn on heating at all'
            elif self.desiredTemp < self.currentTemp():
                return 'House is already at or above desired Temp'
            else:
                #so either we call erins temperatureSimulator here or else we call turn on heater now and from heater turn on the temperature simulator for now I'll do it here
                self.thermomstat.turnOnHeater()
                


    #need to modify this so that it doesn't just deal with hours but also minutes 
    #       come back later to add that 
    def checkSchedule(self):
        #find next most recent schdule
        nextTime = int(self.nextSchedule[0] + self.nextSchedule[1])
        timeInt = int(self.currentTime[0] +self.currentTime[1])
        timeDif =25
        for schedule in self.roomSchedule.schedule:
            scheduleTime = int(schedule[0] +schedule[1])
            if scheduleTime <= nextTime and timeInt <= scheduleTime and (scheduleTime-timeInt)<timeDif : #this doesn't account for a situation where its 11pm and the next schedule is at 8am
                self.nextSchedule = schedule
                timeDif = scheduleTime - timeInt
        if timeDif ==0:
            #call to function to start the schdule
            self.scheduling()

#manually change temp
    def turnOffSchedule(self):
        self.schedule.scheduleOn = False

    def turnOnSchedule(self):
        self.schedule.scheduleOn = True
    
    
    def changeTempDirectly(self,desiredTemp):
        self.currentTemp = desiredTemp # will call one of the temp functions here instead

    def deleteDefaultSchedule(self):
        #want to delete the default but don't want to delete anything added by user 
        #should probably have a check to see if theres 1) a house schedule 2) a room schedule 
        if self.defaultSchedule and self.schedule:
            for time in self.defaultSchedule():
                if time in self.schedule and self.defaultSchedule[time] == self.schedule[time]:
                    del self.schedule[time]
                    

    def deleteEntryFromSchedule(self,timeToDelete): #have to delete entries one at a time or delete the whole schedule
        if self.schedule:
            for times in self.schedule:
                if times ==timeToDelete:
                    del self.schedule[times]
    
    def deleteEntireSchdule(self):
        self.schedule = None 

    def takeTempReading(self):
        print('stuff')



room1 = Room(23)
room1.roomSchedule.addToSchedule('08:00',20,'12:00')
room1.roomSchedule.addToSchedule('10:00',20,'12:00')
room1.roomSchedule.addToSchedule('12:00',20,'12:00')
room1.roomSchedule.addToSchedule('16:00', 14,'17:00')
room1.checkSchedule()
room1.scheduling(1, 100)  # tester: check the temperature every second five times