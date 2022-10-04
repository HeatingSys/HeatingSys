# Basic structure of room for now
import schedule
import time


class Room:
    def __init__(self, temp1):
        self.temp = temp1
        self.greenStatus = False
        """
        self.desiredTemp = 21
        self.currentTemp = ?
        self.desiredGreenTemp = 10    # online it says eco heating is between 7 and 19C
        self.greenStatus = False
        self.heater = Heater object
        """

    # our setter
    # def changeTemp(self):

    # our getter
    # def checkTempPeriodically(self):

    # method called by the scheduler
    # checks current temperature and calls heater method to turn on or off heater
    def check_temp(self):
        print(self.temp)  # tester
        """
        if self.greenStatus == False:
            if self.currentTemp < self.desiredTemp:
                self.heater.turnOn(currentTemp, desiredTemp) # defined in heater class
            elif:
                self.heater.turnOff() # defined in heater class
        elif:
            if self.currentTemp < self.desiredGreenTemp:
                self.heater.turnOn(currentTemp, desiredGreenTemp)
            elif:
                self.heater.turnOff()
        """

    # method turning on heating lower heating
        # change desiredTemp to lower temp and call check_temp
    def turn_on_low_heating(self):
        print("green heating on ")  # tester
        """
        self.greenStatus = True
        self.check_temp
        """

    def turn_off_low_heating(self):
        print("regular heating on")  # tester
        """
        self.greenStatus = False
        self.check_temp
        """

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


room1 = Room(23)
room1.scheduling(1, 100)  # tester: check the temperature every second five times
