from datetime import datetime
from heater import Thermostat
from schedule import Schedule

class Room:
    def __init__(self,room_id,outsideTemp):
        self.room_id = room_id
        self.automated = True #Is this what was previously our 'automated'? this is redundant its already in schedule
        self.desiredTemp = 12 #should start out empty
        self.currentTemp = 12 # we need to get our heater/thermostat class before being able to define this properly
        self.heatingRunning = False #states whether heating is on now or nah
        self.nextSchedule = '21:00'
        self.thermomstat = Thermostat(12)
        self.defaultSchedule = Schedule()#None #this is by default on can manually turn it off
        self.defaultScheduleState = True
        self.roomSchedule = Schedule()
        self.outsideTemp = outsideTemp
        self.heaterPower = None
        self.currentTime = datetime.now().strftime("%H:%M")

    def defaultSchedulingOnly(self):
        self.deleteEntireSchdule()

    def turnOffScheduling(self):
        self.roomSchedule.scheduleOn = False
    
    def turnOnScheduling(self):
        self.roomSchedule.scheduleOn = True

    # method specifies when to kick in scheduled heating
    def scheduling(self):
        if self.roomSchedule.scheduleOn:  # if schedule is on
            # first need to get info about the schedule
            info = self.roomSchedule.schedule[
                self.nextSchedule]  # this is single handedly the worst thing iv'e seen in my life#
            self.desiredTemp = info[0]
            self.thermomstat.getCurrentTemp() 
            #delete if - is there more?
            #so either we call erins temperatureSimulator here or else we call turn on heater now and from heater turn on the temperature simulator for now I'll do it here
            self.heatingRunning  = True
            self.thermomstat.heaterOn(info[0],self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp(),self.heaterPower)
        
    #check every 30 mins for erins temp
    #this is called from house so no need for outside temp in roo, can pass vars in from house
    #This logically doesn't make sense to have
    #CHANGE NAME - NO LONGER FITS
    def checkTempPeriodically(self, previousOutsideTemp, currentOutsideTemp, heaterPower):
        if self.heatingRunning:
            self.thermomstat.heaterOn(self.desiredTemp, previousOutsideTemp, currentOutsideTemp, heaterPower)
        else:
            self.thermomstat.heaterOff(previousOutsideTemp,currentOutsideTemp, heaterPower)
            self.heatingRunning = False

    # need to modify this so that it doesn't just deal with hours but also minutes
    #       come back later to add that 

    #shouldn't need to check for minutes anymore - system enforces schedule must be 1 hour diff at least
    def checkNextSchedule(self):
        #find next most recent schdule
        nextTime = int(self.nextSchedule[0] + self.nextSchedule[1])

        timeInt = int(self.currentTime[0] +self.currentTime[1])
        timeDif =nextTime - timeInt
        if timeDif <0:
            timeDif = timeDif *-1 
        for schedule in self.roomSchedule.schedule:
            scheduleTime = int(schedule[0] +schedule[1])
            if scheduleTime <= nextTime and timeInt <= scheduleTime and (scheduleTime-timeInt)<timeDif : #this doesn't account for a situation where its 11pm and the next schedule is at 8am

                self.nextSchedule = schedule
                timeDif = scheduleTime - timeInt
                if timeDif < 0:
                    timeDif = timeDif * -1
        if timeDif == 0:
            # call to function to start the schdule
            self.scheduling()



    def changeTempDirectly(self,desiredTemp, prevOutsideTemp,currentOutside):
        self.thermomstat.turnOnHeater(desiredTemp,prevOutsideTemp,currentOutside ) # will call one of the temp functions here instead

    def deleteDefaultSchedule(self):
        #want to delete the default but don't want to delete anything added by user 
        #should probably have a check to see if theres 1) a house schedule 2) a room schedule 
        if self.defaultSchedule and self.roomSchedule:
            for time in self.defaultSchedule.schedule.keys():
                if time in self.roomSchedule.schedule and self.defaultSchedule.schedule[time] == self.roomSchedule.schedule[time]:
                    del self.roomSchedule.schedule[time]
    
    def deleteEntireSchdule(self):
        self.roomSchedule = None
        self.roomSchedule = Schedule()

    def addToSchedule(self,startTime,desiredTemp, endTime):
        self.roomSchedule.addToSchedule(startTime,desiredTemp,endTime)


'''
room1 = Room(23,10)
room1.roomSchedule.addToSchedule('08:00',20,'12:00')
room1.roomSchedule.addToSchedule('10:00',20,'12:00')
room1.roomSchedule.deleteFromSchedule('10:00')
room1.deleteEntireSchdule()
room1.roomSchedule.addToSchedule('12:00',20,'12:00')
room1.roomSchedule.addToSchedule('16:00', 14,'17:00')
room1.defaultSchedule.addToSchedule('01:30',17,'04:00')
room1.checkNextSchedule()'''