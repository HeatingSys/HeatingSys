# Basic structure of room for now
#import schedule
import time


class Room:
    def __init__(self, temp1):
        self.temp = temp1
        self.greenStatus = False #Is this what was previously our 'automated'?
        self.desiredTemp = None #should start out empty
        self.currentTemp = 12 # we need to get our heater/thermostat class before being able to define this properly
        self.desiredGreenTemp = 10    # online it says eco heating is between 7 and 19C -- QUESTION: What is it and can it be moved to house
        self.greenStatus = False        #QUESTION -- the same question as ^
        self.schedule = {}
        self.scheduleOn = False #this should allow us to turn off the schedule manually based on user 
        #self.heater = Heater object #gonna comment this out until we have our thermostat class
        """

    # our setter
    # def changeTemp(self):

    # our getter
    # def checkTempPeriodically(self):

    # method called by the scheduler
    # checks current temperature and calls heater method to turn on or off heater"""
    def check_temp(self):
        print(self.temp)  # tester
        
        if self.greenStatus == False:
            if self.currentTemp < self.desiredTemp:
                self.heater.turnOn(currentTemp, desiredTemp) # defined in heater class
            else:
                self.heater.turnOff() # defined in heater class
        else:
            if self.currentTemp < self.desiredGreenTemp:
                self.heater.turnOn(currentTemp, desiredGreenTemp)
            else:
                self.heater.turnOff()
        """

    # method turning on heating lower heating
        # change desiredTemp to lower temp and call check_temp"""
    def turn_on_low_heating(self):
        print("green heating on ")  # tester
        
        self.greenStatus = True
        self.check_temp
        

    def turn_off_low_heating(self):
        print("regular heating on")  # tester
       
        self.greenStatus = False
        self.check_temp


    # method specifies when to kick in scheduled heating
    # leng is length of interval in seconds
    # times is how many times the loop repeats
    def scheduling(self, leng, times):
        schedule.every(leng).seconds.do(self.check_temp) # every _ second check current temperature & adjust heater
        schedule.every().day.at("11:47").do(self.turn_on_low_heating()) # time to switch to green  heating
        schedule.every().day.at("11:47:10").do(self.turn_off_low_heating()) # time to switch to regular heating
        for i in range(times + 1):
            schedule.run_pending()
            time.sleep(1)  # exits the scheduling method once range is reached

    # method specifies when to kick in scheduled heating
    def setUpSchedule(self,startTime,info):
        self.schedule[startTime] = info

    #from user persepective the user will initally try setup schedule and setUpSchedule should be called from inside here
    # So from the website perspective a user submits a form with startime , temp and endtime of the schedule and this method is called
    # regardless of whether self.schedule is empty yet or nah 
    def addToSchedule(self,startTime,temp,endTime): #could have an override true or false that could be an optional input 
        scheduleList = [temp,endTime]
        if len(self.schedule) ==0:
            return self.setUpSchedule(startTime,scheduleList)#do we even need a separate method for this ?? - it's better in theory but stupid in practice
        else:
            #the time should be a string
            if startTime in self.schedule:
                #clash, for now we'll override this automatically - discuss how to proceed with this
                self.schedule[startTime] = scheduleList
            else:
                self.schedule[startTime] = scheduleList

room1 = Room(23)
room1.addToSchedule('10:00',20,'12:00')
room1.addToSchedule('16:00', 14,'17:00')
room1.scheduling(1, 100)  # tester: check the temperature every second five times
