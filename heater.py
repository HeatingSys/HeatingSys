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