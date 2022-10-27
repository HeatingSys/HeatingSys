<<<<<<< HEAD
#should be one of these in each room - in theory
#I think some of the maths stuff should work in here
class thermostat:
    def __init__(self):
        #hopefully shouldn't really need much here in theory
        self.heaterState = False #should be on or off where True =on and False = Off 
        self.currentTemp = 0 #most recent reading
        print('hi')

    def turnOnHeater(self):
        print('turn on heater')

    #Need method here to like mimic the increase in room temp 
=======
# should be one of these in each room - in theory
# i think this is where the window sensor should go

import math


class thermostat:
    def __init__(self):
        # hopefully shouldn't really need much here in theory
        self.heaterState = False  # should be on or off where True =on and False = Off
        self.currentTemp = 0  # most recent reading
        self.currentEnergy = 0  # most recent update of energy spent in kWh
        self.windowState = False # True = opened. i think this will not be in thermostat, but rather in room and we will search it?... idk
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

        #first, if desiredTemp is increasing the heat by a lot it will take more energy (around 10% extra power)
        if (desiredTemp - currentTemp) > 5:
            self.currentEnergy = self.currentEnergy + (kWh/2)*moreEnergy
        #then, at average household temperature 20 degrees, heater of i kWh will use i kWh per hour
        if desiredTemp == 20:
            self.currentEnergy = self.currentEnergy + kWh/2
        # for each degree more than the average temp, spend an extra 10% of energy
        elif desiredTemp > 20:
            for r in range(desiredTemp - 20):
                self.currentEnergy = self.currentEnergy + (kWh/2)*moreEnergy
        # for each degree less than the average temp, spend 10% less energy
        else:
            for r in range(20-desiredTemp):
                self.currentEnergy = self.currentEnergy + (kWh/2)*lessEnergy



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
heater.powerCalculator(21,17,1000)
print(heater.currentEnergy)
>>>>>>> 9457a17b7bae442c56e93bea513313a20a539043
