#############
# outsideTemp file contains:
#   - outsideTemp class
#       - should be one for each house
#       - outsideTemp class contains:
#           - Method that creates outsideTemp object and initializes first array (Called once by house)
#           - Method that gets the current outside temperature
#           - Method that gets the previous outside temperature
#           - Method that is called every 30 minutes from house to set new current Temp!!!!!!!
#           - Methods that generates an array of 9 temperatures
#               - that represents temps of the next 4 hours at 30 minute intervals
##############

import random
import math


class OutsideTemp:

    def __init__(self):
        # Create empty array of temps for the next 4 hours at 30 minute intervals
        self.outsideTempsForNext4Hours = [None] * 9
        # Create first temp
        self.outsideTempsForNext4Hours[0] = round(random.uniform(4.0, 8.0), 2)
        # 5% chance that it will be a temp between -10 and 15
        if random.randrange(0, 100) < 5:
            self.outsideTempsForNext4Hours[0] = round(random.uniform(-10.0, 15.0), 2)
        # Generate the rest of the array
        self.index = 0 # necessary to correctly generate first array
        self.generateOutsideTempForFourHours()
        # Initialize index
        self.index = 1  # index represents where currentTemp is in outsideTemp array, number from 0 to 8

    # Getter methods for outsideTemp
    def getCurrentOutsideTemp(self):
        return round(self.outsideTempsForNext4Hours[self.index],2)

    def getPreviousOutsideTemp(self):
        return round(self.outsideTempsForNext4Hours[self.index - 1],2)

    # current temperature is an index var that's incremented each time its called in the outsideTemp array
    def setCurrentOutsideTemp(self):
        # if you get to end of array, generate the next four hours of temps and re-set index to 1
        if self.index == 8:
            self.generateOutsideTempForFourHours()
            self.index = 1  # skip 0 because that's the same temp as previous self.outsideTempsForNext4Hours[8]
        # else its just going up through the array
        else:
            self.index = self.index + 1

    # will update the array for outside temps for next 4 hours
    def generateOutsideTempForFourHours(self):
        # when object is first create, index is at 0 (only time it will be at zero),
        # and it will have no previous array so skip this step
        if self.index != 0:
            # new [0] is previous array's last temperature
            self.outsideTempsForNext4Hours[0] = self.outsideTempsForNext4Hours[8]

        # this finds the outside temp that will occur in 4 hours
        # generate a random float between 4 and 8 degree
        self.outsideTempsForNext4Hours[8] = round(random.uniform(4.0, 8.0), 2)
        # 5% chance that it will be a temp between -10 and 15
        if random.randrange(0, 100) < 5:
            self.outsideTempsForNext4Hours[8] = round(random.uniform(-10.0, 15.0), 2)

        # find rate of change of function from current temp to temp in four hours
        # T4 = To*e^k*t
        # -> ln(T4/To)/t=k
        # t = 4 hours
        # if currentTemp = 0, then divide by zero, illegal math, so change value of currentTemp by insignificant amount
        if self.outsideTempsForNext4Hours[0] == 0:
            self.outsideTempsForNext4Hours[0] = 0.1
        k = round((math.log(self.outsideTempsForNext4Hours[8] / self.outsideTempsForNext4Hours[0])) / 4, 4)

        # now that we have rate, calculate outside temp every 30 minutes and put into array
        h = 1.5
        for m in range(1, 8):
            self.outsideTempsForNext4Hours[m] = round((self.outsideTempsForNext4Hours[0] * math.exp(k * h)), 2)
            h = h + 0.5


# test
#outside = OutsideTemp()  # create item
#print("get current without setting: " + str(outside.getCurrentOutsideTemp()))
#for i in range(20):
#    outside.setCurrentOutsideTemp()
#    print("previous: " + str(outside.getPreviousOutsideTemp()) + " current: " + str(
#        outside.getCurrentOutsideTemp()) + "\n")
