# should be one of these in each room - in theory
# i think this is where the window sensor should go

import math
import random


class thermostat:
    def __init__(self):
        # hopefully shouldn't really need much here in theory
        self.heaterState = False  # should be on or off where True =on and False = Off
        self.currentTemp = 0  # most recent reading
        self.currentEnergy = 0  # most recent update of energy spent in kWh
        self.windowState = False  # True = opened. i think this will not be in thermostat, but rather in room and we will search it?... idk
        # i wrote it here because i needed the item

    def turnOnHeater(self):
        self.heaterState = True
        print('turn on heater')

    def turnOffHeater(self):
        self.heaterState = False
        print('turn off heater')

    # So im thinking outside temp is collected from the data set we want to have and updates every 30m like we planned
    # and the three previous temps can actually be items in the thermostat class
    # where they just copy the data from the outside temp data set until heater is turned on
    # then it will follow this simulator until heater is turned off and inside equals outside again
    # maybe we do a thing where inside is always like 2 degrees higher than outside bc of house heat (lights, bodies, appliances)

    # basically outsideTemp, threeIterAgoTemp, twoIterAgoTemp, oneIterAgoTemp would be objects in thermostat class
    # and method would be:
    # def temperatureSimulator(self):
    # then when the simulator iteration is called, the first thing that would happen would be to update all the new numbers:
    # three = two,  two = one,   one = outside,   outside = fetch from database

    # here's the math formula that simulates temp going up and down when heater is on/off
    def temperatureSimulator(self, previousOutsideTemp, outsideTemp, threeIterAgoTemp, twoIterAgoTemp, oneIterAgoTemp):
        print('temp is simulating')
        # where t is time interval (30 minutes) and k is rate of change
        t = 30
        k = 0
        # if or while... idk how we are connecting all these loops together....

        # While the heater is on:
        if self.heaterState:
            if threeIterAgoTemp <= twoIterAgoTemp:
                if twoIterAgoTemp <= oneIterAgoTemp:
                    # temps are going up with time, ie: 17-18-19
                    k = 0.0035
                else:
                    # temps went up then down, ie: 17-18-17
                    k = 0.0045
            else:
                if twoIterAgoTemp <= oneIterAgoTemp:
                    # temps are going down then up, ie: 18-17-19
                    k = 0.004
                else:
                    # temps are going down with time, ie: 19-18-17
                    k = 0.005
            # exponential heating formula: T(t) = Tc*e^((k-(Tc-To))*t)
            self.currentTemp = oneIterAgoTemp * math.exp((k - (oneIterAgoTemp - outsideTemp) / 10000) * t)

        # while the heater is off
        else:
            # if the heater has been off for a while, inside temp and outside temp should be similar
            if oneIterAgoTemp == previousOutsideTemp or oneIterAgoTemp == (previousOutsideTemp + 3):
                # if heater has been off for a while and window is opened
                if self.windowState:
                    self.currentTemp = outsideTemp
                # if heater has been off for a while and window is closed
                else:
                    self.currentTemp = outsideTemp + 3

            # if heater has been recently turned off, then temp will be exponentially going down
            else:
                if threeIterAgoTemp <= twoIterAgoTemp:
                    if twoIterAgoTemp <= oneIterAgoTemp:
                        # temps are going up with time, ie: 17-18-19
                        k = 0.005
                    else:
                        # temps went up then down, ie: 17-18-17
                        k = 0.004
                else:
                    if twoIterAgoTemp <= oneIterAgoTemp:
                        # temps are going down then up, ie: 18-17-19
                        k = 0.0045
                    else:
                        # temps are going down with time, ie: 19-18-17
                        k = 0.0035
                # if outside temp is hotter than inside temp then current temp will go up
                if (oneIterAgoTemp - outsideTemp) < 0:
                    a = 1
                else:  # if outside temp is colder then current temp will go down
                    a = -1
                self.currentTemp = oneIterAgoTemp * math.exp(a * (k - (oneIterAgoTemp - outsideTemp) / 10000) * t)

                # if the formula makes the currentTemp go down lower than outside: makes no sense
                # if that happens then inside just equals outside
                if (outsideTemp < oneIterAgoTemp) and (self.currentTemp < outsideTemp):
                    self.currentTemp = outsideTemp
                # if the formula makes currentTemp go higher than outside: makes no sense
                # if that happens then inside just equals outside
                if (outsideTemp > oneIterAgoTemp) and (self.currentTemp > outsideTemp):
                    self.currentTemp = outsideTemp

    # here's the method that changes the state of the window.
    def windowSimulator(self):
        # if window is open,
        if self.windowState:
            # there's a 50% chance it will close
            if random.randrange(0, 100) < 50:
                self.windowState = False
            # else stay closed
        # if window is closed
        else:
            # there's a 5% chance it will open
            if random.randrange(0, 100) < 5:
                self.windowState = True

    # here's the  formula that updates the energy spent in kWh
    # heaterPower is the strength of the heater in watts
    def powerCalculator(self, desiredTemp, currentTemp, heaterPower):
        # Watts into Kilowatt-Hours: kWh = (watts × hrs) ÷ 1,000
        kWh = heaterPower / 1000
        print('power calculating')
        moreEnergy = 1.1
        lessEnergy = 0.9

        # idk if there should be an if statement here that says if self.heaterState = True
        # or if this method is called while the heater is on and therefore will be in some other loop....

        # first, if desiredTemp is increasing the heat by a lot it will take more energy (around 10% extra power)
        if (desiredTemp - currentTemp) > 5:
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

# This should be in house doc but not house class
# will update the array for outside temps for next 4 hours
def generateOutsideTempForFourHours():

    outsideTempsForNext4Hours = [None]*9

    ## Current outside temp = outsideTempForNext4Hours[8] of last array
    # i might need to create a get function getLastOutsideTemp since this is outside house class....
    # i put 6 as a random number just to test that it works
    outsideTempsForNext4Hours[0] = 6 #outsideTempsForNext4Hours[0] = getLastOutsideTemp()

    # this finds the outside temp that will occur in 4 hours
    # generate a random float between 4 and 8 degree
    outsideTempsForNext4Hours[8] = round(random.uniform(4.0, 8.0), 2)
    # 5% chance that it will be a temp between -10 and 15
    if random.randrange(0, 100) < 5:
        outsideTempsForNext4Hours[8] = round(random.uniform(-10.0, 15.0), 2)

    # find rate of change of function from current temp to temp in four hours
    # T4 = To*e^k*t
    # ln(T4/To)/t=k
    k = round((math.log(outsideTempsForNext4Hours[8]/outsideTempsForNext4Hours[0]))/4, 4)

    # now that have rate, calculate outside temp every 30 minutes and put into array
    h = 1.5
    for i in range(1, 8):
        outsideTempsForNext4Hours[i] = round((outsideTempsForNext4Hours[0] * math.exp(k * h)),2)
        h = h + 0.5

    return outsideTempsForNext4Hours

# so now that the  temps for the next 4 hours have been created, need to go through array
    # basically, method called every 30 minutes
    # it will work through the array by house having an index var that's incremented each time its called
        # if it's at the end of the array, it calls the generateOutsideTempForFourHours method to update a new array
        # then re-start at index 1 next time its called to provide next temp
def getCurrentOutsideTemp(index):
    # going to need an index value in house
        # at the moment, returning the next index value
        # but in house, should have index variable.
    outsideTempArray = generateOutsideTempForFourHours() # delete line in house, i just need this at the moment cuz in wrong doc
    # ^^^ this will just be self.outsideTempArray

    # when program first starts, index should be at 0 (only time it will be at zero),
    # it will create first temp and generate the rest of the array
    if index == 0:
        outsideTempArray[0] = round(random.uniform(4.0, 8.0), 2)
        # 5% chance that it will be a temp between -10 and 15
        if random.randrange(0, 100) < 5:
            outsideTempArray[0] = round(random.uniform(-10.0, 15.0), 2)
        # self.outsideTempArray = generateOutsideTempForFourHours() # sets the outsideTempArray
        # self.currentTemp = outsideTempArray[index]  # currentTemp is the thing that will be returned
        # self.index = self.index + 1
    # if you get to end of array, generate the next four hours of temps and post the last temp
    elif index == 8:
        index = index #filler text until i can remove #s
        # self.outsideTempArray = generateOutsideTempForFourHours() # sets the outsideTempArray
        # self.index = 1 (skip 0 because thats the same temp as outsideTempArray[8])
    # else its just going up through the array
    else:
        index = index # filler text until i can remove #s
        # self.currentTemp = outsideTempArray[index]  # currentTemp is the thing that will be returned
        # self.index = self.index + 1





# tests
heater = thermostat()
heater.turnOnHeater()
heater.temperatureSimulator(14, 15, 20, 21, 18)
print(heater.currentTemp)
heater.turnOffHeater()
heater.temperatureSimulator(1, 1, 22, 26, 27)
print(heater.currentTemp)
heater.temperatureSimulator(29, 30, 22, 26, 27)
print(heater.currentTemp)
heater.powerCalculator(21, 17, 1000)
print(heater.currentEnergy)
print("outside temp tests")
print(generateOutsideTempForFourHours())

