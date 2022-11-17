# Basic structure of room for now
import schedule
import time

from heater import Thermostat
from schedule import Schedule


class Room:
    def __init__(self, name):
        self.name = name
        self.automated = True  # Is this what was previously our 'automated'? this is redundant its already in schedule
        self.desiredTemp = None  # should start out empty
        self.currentTemp = 12  # we need to get our heater/thermostat class before being able to define this properly
        self.roomschedule = 'hi'  # want to change this to include house default
        self.currentTime = '12:00'  # should be a read from now() - for testing purposes leaving this alone rn
        self.heatingRunning = False  # states whether heating is on now or nah
        self.nextSchedule = '24:00'
        self.thermostat = Thermostat(CurrentOutsideTemp)  # needs currentOutsideTemp
        self.defaultSchedule = self.house.schedule  # this is by default on can manually turn it off
        self.defaultScheduleState = True
        self.schedule = Schedule()
        # self.enableDefaultSchedule()

    # QUESTION wtf is this
    # remove this and just have a method that can add onto default
    # in what world would someone want to add default settings to their own schedule
    def addDefaultToSchedule(self):
        for time in self.defaultSchedule.schedule:
            if time not in self.schedule.schedule:
                mylist = self.defaultSchedule.schedule[time]
                wantedTemp = mylist[0]
                endTime = mylist[1]
                self.schedule.addToSchedule(time, wantedTemp, endTime)
        self.defaultScheduleState = False

    def turnScheduleToDefault(self):
        self.schedule = self.defaultSchedule
        self.defaultScheduleState = True


    # method specifies when to kick in scheduled heating
    # leng is length of interval in seconds
    # times is how many times the loop repeats
    def scheduling(self):
        if self.roomSchedule.scheduleOn:  # if schedule is on
            # first need to get info about the schedule
            info = self.roomSchedule.schedule[
                self.nextSchedule]  # this is single handedly the worst thing iv'e seen in my life#
            self.desiredTemp = info[0]
            # call heaterOn which will call temperatureSimulator, windowSimulator, and powerCalculator
            self.thermostat.heaterOn(self.desiredTemp, previousOutsideTemp, currentOutsideTemp, heaterPower)
        else:  # if schedule is on
            # call heaterOff which will call temperatureSimulator and windowSimulator
            self.thermostat.heaterOff(self.desiredTemp, previousOutsideTemp, currentOutsideTemp, heaterPower)

    # need to modify this so that it doesn't just deal with hours but also minutes
    #       come back later to add that 
    def checkSchedule(self):
        # find next most recent schedule
        if self.defaultScheduleState is True:
            # check if default is in here
            for time in self.defaultSchedule.schedule:
                if self.schedule is None or time not in self.schedule.schedule:
                    self.addDefaultToSchedule()
        nextTime = int(self.nextSchedule[0] + self.nextSchedule[1])
        timeInt = int(self.currentTime[0] + self.currentTime[1])
        timeDif = nextTime - timeInt
        if timeDif < 0:
            timeDif = timeDif * -1
        for schedule in self.schedule.schedule:
            scheduleTime = int(schedule[0] + schedule[1])
            if scheduleTime <= nextTime and timeInt <= scheduleTime and (
                    scheduleTime - timeInt) < timeDif:  # this doesn't account for a situation where its 11pm and the next schedule is at 8am
                self.nextSchedule = schedule
                timeDif = scheduleTime - timeInt
                if timeDif < 0:
                    timeDif = timeDif * -1
        if timeDif == 0:
            # call to function to start the schdule
            self.scheduling()

    # manually change temp
    def turnOffSchedule(self):
        self.schedule.scheduleOn = False

    def turnOnSchedule(self):
        self.schedule.scheduleOn = True

    def changeTempDirectly(self, desiredTemp):
        self.currentTemp = desiredTemp  # will call one of the temp functions here instead

    def deleteEntireSchedule(self):
        self.schedule = None
        self.schedule = Schedule()



# room1 = Room(23,'emmasRoom')
# room1.schedule.addToSchedule('08:00',20,'12:00')
# room1.schedule.addToSchedule('10:00',20,'12:00')
# room1.schedule.deleteFromSchedule('10:00')
# room1.deleteEntireSchdule()
# room1.schedule.addToSchedule('12:00',20,'12:00')
# room1.schedule.addToSchedule('16:00', 14,'17:00')
# room1.checkSchedule()
# room1.scheduling(1, 100)  # tester: check the temperature every second five times
