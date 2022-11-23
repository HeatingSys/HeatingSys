#############
# Heater file contains:
#   - Thermostat class
#       - should be one of these in each room - in theory
#       - Thermostat class contains:
#           - Method that creates thermostat object, needs current OutsideTemp
#           - Method to get current inside temp
#           - Methods that controls if heater is on or off (room calls either method every 30 minutes) !!!!!
#               - will call temperatureSimulator, windowSimulator, and powerCalculator
#               - needs desiredTemp, previousOutsideTemp, outsideTemp, heaterPower
#           - Method that simulates inside temperature
#           - Method that simulates window opening and closing
#           - Method that calculates power
##############

import math
import random


class Thermostat:
    def __init__(self, currentOutsideTemp):
        self.heaterState = False  # Is heater on?  True = On and False = Off
        self.currentEnergy = 0  # energy spent in kWh
        self.windowState = False  # Is window open? True = opened
        self.insideTempHistory = [
                                     currentOutsideTemp + 3] * 4  # when thermostat first made, history will just use outsideTemp

    def getCurrentTemp(self):
        return self.insideTempHistory[0]

    # Room class will call either turnOnHeater or turnOffHeater every 30 minutes
    def heaterOn(self, desiredTemp, previousOutsideTemp, currentOutsideTemp, heaterPower):
        # if currentTemp > desiredTemp, heater should not go on
        if self.insideTempHistory[0] > desiredTemp:
            self.heaterState = False
            self.temperatureSimulator(desiredTemp, previousOutsideTemp, currentOutsideTemp)  # will simulate next temp
            self.windowSimulator()  # will simulate the next window state
            # will NOT calculate how much power is used because no power is used
            return 'Heating is off, room is already above desired Temp'
        else:
            self.heaterState = True
            self.temperatureSimulator(desiredTemp, previousOutsideTemp, currentOutsideTemp)  # will simulate next temp
            self.windowSimulator()  # will simulate the next window state
            # if user inputted heaterPower, can calculate heater statistics
            if heaterPower is not None:
                self.powerCalculator(desiredTemp, heaterPower)  # will calculate how much power is used

    def heaterOff(self, desiredTemp, previousOutsideTemp, currentOutsideTemp):
        self.heaterState = False
        self.temperatureSimulator(desiredTemp, previousOutsideTemp, currentOutsideTemp)  # will simulate next temp
        self.windowSimulator()  # will simulate the next window state
        # will NOT calculate how much power is used because no power is used

    # here's the math formula that simulates temp going up and down when heater is on/off
    def temperatureSimulator(self, desiredTemp, previousOutsideTemp, currentOutsideTemp):
        # where t is time interval (30 minutes) and k is rate of change
        t = 30
        k = 0.0035
        a = 1

        # While the heater is on:
        if self.heaterState:
            # if currentTemp = desiredTemp, leave currentTemp = desiredTemp
            if self.insideTempHistory[0] == desiredTemp:
                # Update the insideTempHistory array:
                self.insideTempHistory[3] = self.insideTempHistory[2]  # 2 iterAgo becomes 3 terAgo
                self.insideTempHistory[2] = self.insideTempHistory[1]  # 1iterAgo becomes 2 iterAgo
                self.insideTempHistory[1] = self.insideTempHistory[0]  # current temp become 1iterAgo
                self.insideTempHistory[0] = desiredTemp

            if self.insideTempHistory[3] <= self.insideTempHistory[2]:
                if self.insideTempHistory[2] <= self.insideTempHistory[1]:
                    # temps are going up with time, ie: 17-18-19
                    k = 0.0035
                else:
                    # temps went up then down, ie: 17-18-17
                    k = 0.0045
            else:
                if self.insideTempHistory[2] <= self.insideTempHistory[1]:
                    # temps are going down then up, ie: 18-17-19
                    k = 0.004
                else:
                    # temps are going down with time, ie: 19-18-17
                    k = 0.005

            # Update the insideTempHistory array:
            self.insideTempHistory[3] = self.insideTempHistory[2]  # 2 iterAgo becomes 3 terAgo
            self.insideTempHistory[2] = self.insideTempHistory[1]  # 1iterAgo becomes 2 iterAgo
            self.insideTempHistory[1] = self.insideTempHistory[0]  # current temp become 1iterAgo

            # update currentTemp, aka insideTempHistory[0]
            # exponential heating formula: T(t) = Tc*e^((k-(Tc-To)/1000)*t)
            ## use insideTempHistory[2] bc array has been updated, so previous insideTemp is actually in position [2]
            self.insideTempHistory[0] = self.insideTempHistory[1] * math.exp(
                (k - (self.insideTempHistory[1] - currentOutsideTemp) // 10000) * t)
            # if currentTemp > desiredTemp, make currentTemp = desiredTemp
            if self.insideTempHistory[0] >= desiredTemp:
                self.insideTempHistory[0] = desiredTemp

        # while the heater is off
        else:
            # if the heater has been off for a while, inside temp and outside temp should be similar
            if self.insideTempHistory[1] == previousOutsideTemp or self.insideTempHistory[1] == (
                    previousOutsideTemp + 3):
                # Update the insideTempHistory array:
                self.insideTempHistory[3] = self.insideTempHistory[2]  # 2 iterAgo becomes 3 terAgo
                self.insideTempHistory[2] = self.insideTempHistory[1]  # 1iterAgo becomes 2 iterAgo
                self.insideTempHistory[1] = self.insideTempHistory[0]  # current temp become 1iterAgo

                # update currentTemp, aka insideTempHistory[0]
                # if heater has been off for a while and window is opened
                if self.windowState:
                    self.insideTempHistory[0] = currentOutsideTemp
                # if heater has been off for a while and window is closed
                else:
                    
                    self.insideTempHistory[0] = currentOutsideTemp + 3

            # if heater has been recently turned off, then temp will be exponentially going down
            else:
                if self.insideTempHistory[3] <= self.insideTempHistory[2]:
                    if self.insideTempHistory[2] <= self.insideTempHistory[1]:
                        # temps are going up with time, ie: 17-18-19
                        k = 0.005
                    else:
                        # temps went up then down, ie: 17-18-17
                        k = 0.004
                else:
                    if self.insideTempHistory[2] <= self.insideTempHistory[1]:
                        # temps are going down then up, ie: 18-17-19
                        k = 0.0045
                    else:
                        # temps are going down with time, ie: 19-18-17
                        k = 0.0035
                # if outside temp is hotter than inside temp then current temp will go up
                if (self.insideTempHistory[1] - currentOutsideTemp) < 0:
                    a = 1
                else:  # if outside temp is colder then current temp will go down
                    a = -1

                # Update the insideTempHistory array:
                self.insideTempHistory[3] = self.insideTempHistory[2]  # 2 iterAgo becomes 3 terAgo
                self.insideTempHistory[2] = self.insideTempHistory[1]  # 1iterAgo becomes 2 iterAgo
                self.insideTempHistory[1] = self.insideTempHistory[0]  # current temp become 1iterAgo

                # update currentTemp, aka insideTempHistory[0]
                # use insideTempHistory[2] bc array was updated, so previous insideTemp is actually in position [2]
                self.insideTempHistory[0] = self.insideTempHistory[2] * math.exp(
                    a * (k - (self.insideTempHistory[2] - currentOutsideTemp) / 10000) * t)

                # formula should stabilize to outsideTemp after heater has been off for a while
                # if its colder outside, currentTemp will go down until it reaches outsideTemp
                # if its hotter outside, currentTemp will go up until it reaches outsideTemp
                # use insideTempHistory[2] bc array was updated, so previous insideTemp is actually in position [2]
                if ((currentOutsideTemp < self.insideTempHistory[2]) and (
                        self.insideTempHistory[0] < currentOutsideTemp)) \
                        or ((currentOutsideTemp > self.insideTempHistory[2]) and (
                        self.insideTempHistory[0] > currentOutsideTemp)):
                    if self.windowState:  # if window is open, currentTemp = outsideTemp
                        self.insideTempHistory[0] = currentOutsideTemp
                    else:  # if window is close, currentTemp = outsideTemp + 3
                        self.insideTempHistory[0] = currentOutsideTemp + 3

    # here's the method that changes the state of the window.
    def windowSimulator(self):
        if self.windowState:  # if window is open,
            # there's a 50% chance it will close
            if random.randrange(0, 100) < 50:
                self.windowState = False
            # else stay opened
        else:  # if window is closed
            # there's a 5% chance it will open
            if random.randrange(0, 100) < 5:
                self.windowState = True
            # else stay closed

    # here's the  formula that updates the energy spent in kWh
    # heaterPower is the strength of the heater in watts
    # how are we getting desiredTemp and heaterPower?
    def powerCalculator(self, desiredTemp, heaterPower):
        # Watts into Kilowatt-Hours: kWh = (watts × hrs) ÷ 1,000
        kWh = heaterPower / 1000
        print('power calculating')
        moreEnergy = 1.1
        lessEnergy = 0.9

        # idk if there should be an if statement here that says if self.heaterState = True
        # or if this method is called while the heater is on and therefore will be in some other loop....

        # first, if desiredTemp is increasing the heat by a lot it will take more energy (around 10% extra power)
        if (desiredTemp - self.insideTempHistory[0]) > 5:
            self.currentEnergy = self.currentEnergy + (kWh / 2) * moreEnergy
        # then, at average household temperature 20 degrees, heater of i kWh will use i kWh per hour
        if desiredTemp == 20:
            self.currentEnergy = self.currentEnergy + kWh / 2
        # for each degree more than the average temp, spend an extra 10% of energy
        elif desiredTemp > 20:
            for r in range(desiredTemp - 20):
                self.currentEnergy = self.currentEnergy + (kWh / 2) * moreEnergy
        # for each degree less than the average temp, spend 10% less energy
        else:
            for r in range(20 - desiredTemp):
                self.currentEnergy = self.currentEnergy + (kWh / 2) * lessEnergy
