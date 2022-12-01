from datetime import datetime
import sys
sys.path.insert(0, "src")
from heater import Thermostat
from schedule import Schedule

class Room:
    def __init__(self,room_id,outsideTemp):
        self.id = room_id
        self.automated = True #Is this what was previously our 'automated'? this is redundant its already in schedule
        self.desiredTemp = None 
        self.heatingRunning = False #states whether heating is on now or nah
        self.nextSchedule = '23:00'
        self.defaultSchedule = Schedule()#None #this is by default on can manually turn it off
        self.defaultScheduleState = True
        self.roomSchedule = Schedule()
        self.outsideTemp = outsideTemp
        self.heatingPower = None
        self.currentTime = datetime.now().strftime("%H:%M")
        self.thermostat = Thermostat(self.outsideTemp.getCurrentOutsideTemp())
        self.currentTemp = self.thermostat.getCurrentTemp() # we need to get our heater/thermostat class before being able to define this properly
        

    #Can delete if you want but I physically can't /won't do it 
    def addDefaultToExistingSchedule(self):
        for time in self.defaultSchedule.schedule:
            if time not in self.roomSchedule.schedule: #
                mylist = self.defaultSchedule.schedule[time]
                wantedTemp = mylist[0]
                endTime = mylist[1]
                self.roomSchedule.addToSchedule(time,wantedTemp,endTime)

    def defaultSchedulingOnly(self):
        self.deleteEntireSchdule()
        self.addDefaultToExistingSchedule()

    def turnOffScheduling(self):
        self.roomSchedule.scheduleOn = False
    
    def turnOnScheduling(self):
        self.roomSchedule.scheduleOn = True

    # method specifies when to kick in scheduled heating
    def scheduling(self):
        if self.roomSchedule.scheduleOn:  # if schedule is on
            # first need to get info about the schedule
            info = self.roomSchedule.schedule[self.nextSchedule]  # this is single handedly the worst thing iv'e seen in my life#
            self.desiredTemp = info[0]
            self.thermostat.getCurrentTemp() 
            #delete if - is there more?
            #so either we call erins temperatureSimulator here or else we call turn on heater now and from heater turn on the temperature simulator for now I'll do it here
            self.heatingRunning  = True
            self.thermostat.heaterOn(self.desiredTemp,self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp(),self.heatingPower)
        
    #check every 30 mins for erins temp
    #this is called from house so no need for outside temp in roo, can pass vars in from house
    #This logically doesn't make sense to have
    #CHANGE NAME - NO LONGER FITS
    def checkTempPeriodically(self):
        if self.heatingRunning:
            self.thermostat.heaterOn(self.desiredTemp,self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp(),self.heatingPower)
        else:
            #   def heaterOff(self, desiredTemp, previousOutsideTemp, currentOutsideTemp):
            self.thermostat.heaterOff(self.desiredTemp,self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp())
            self.heatingRunning = False

    # need to modify this so that it doesn't just deal with hours but also minutes
    #       come back later to add that 

    #shouldn't need to check for minutes anymore - system enforces schedule must be 1 hour diff at least
    def checkNextSchedule(self):
        if self.defaultScheduleState is True:
            for time in self.defaultSchedule.schedule:
                if self.roomSchedule is None or time not in self.roomSchedule.schedule:
                    self.addDefaultToExistingSchedule()
        nextTime = int(self.nextSchedule[0] + self.nextSchedule[1])

        timeInt = int(self.currentTime[0] + self.currentTime[1])
        timeDif = nextTime - timeInt
        if timeDif <0:
            timeDif = timeDif *-1 
        for schedule in self.roomSchedule.schedule:
            scheduleTime = int(schedule[0] + schedule[1])
            if scheduleTime <= nextTime and timeInt <= scheduleTime and (scheduleTime-timeInt)<timeDif : #this doesn't account for a situation where its 11pm and the next schedule is at 8am

                self.nextSchedule = schedule
                timeDif = scheduleTime - timeInt
                if timeDif < 0:
                    timeDif = timeDif * -1

    def endSchedule(self):
        if self.heatingRunning is True:
            endTime = self.roomSchedule.schedule[self.nextSchedule][1]
            #self.heatingRunning = False
            now = datetime.now().strftime("%H:%M")
            current = int(now[3] + now[4])
            diffSet = False
            if current >30:
                diffSet = True
                diff = current -30
                if diff < 10:
                    diff = str('0'+ str(diff))
                outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
            else:
                outOfRange = now[0]+now[1]+':' +str(current +30)
            if int(endTime[0] +endTime[1]) >= int(now[0]+now[1]) and int(endTime[0] +endTime[1]) <=int(outOfRange[0]+outOfRange[1]):
                if int(endTime[3] +endTime[4]) <= int(now[3]+now[4]) and int(endTime[3] +endTime[4]) <=int(outOfRange[0]+outOfRange[1]):
                    self.thermostat.heaterOff(self.desiredTemp,self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp())
                    self.heatingRunning = False
                    self.checkNextSchedule()
                elif int(endTime[3] +endTime[4]) <= int(now[3]+now[4]) and int(endTime[3] +endTime[4]) >=int(outOfRange[0]+outOfRange[1]) and diff is True:
                    self.thermostat.heaterOff(self.desiredTemp,self.outsideTemp.getPreviousOutsideTemp(),self.outsideTemp.getCurrentOutsideTemp())
                    self.heatingRunning = False
                    self.checkNextSchedule()

    def changeTempDirectly(self,desiredTemp, prevOutsideTemp,currentOutside):
        self.thermostat.turnOnHeater(desiredTemp,prevOutsideTemp,currentOutside)

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

    def getCurrentTemp(self):
        self.currentTemp = self.thermostat.getCurrentTemp()
        #print("Current room Temp: ",self.currentTemp)
        return self.currentTemp
        
    def deleteOneEntry(self,startTime):
        self.deleteFromSchedule(self,startTime)

    def getDefaultSchedule(self):
        return self.defaultSchedule.schedule

    def getRoomSchedule(self):
        return self.roomSchedule.schedule