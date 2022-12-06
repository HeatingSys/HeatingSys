#############
# schedule file contains:
#   - Schedule class
#       - should be one for each room
#       - Schedule class contains:
#           - Method that sets up a schedule
#           - Method that adds to a schedule
#           - Method that deletes from a schedule
##############

class Schedule:
    def __init__(self) -> None:
        self.schedule = {} # schedule is stored as a dictionary
        self.scheduleOn = True # has the schedule started? True = Yes, False = No

    # Specifies when to kick in scheduled heating
    def setUpSchedule(self, startTime,info):
        self.schedule[startTime] = info # key = startTime, value = schedule information

    # Adds to a schedule, gets passed in the start time, temperatur and end time
    def addToSchedule(self,startTime,temp,endTime):
        scheduleList = [temp,endTime]
        if len(self.schedule) ==0:
            return self.setUpSchedule(startTime,scheduleList)
        else:
            # the time should be a string
            if startTime in self.schedule:
                self.schedule[startTime] = scheduleList
            else:
                self.schedule[startTime] = scheduleList
    
    # Deletes Schedule Object from Schedule Dictionary 
    def deleteFromSchedule(self, start_time_key):
        for key in self.schedule:
            if key == start_time_key:
                del self.schedule[start_time_key]
                return "success"
