class Schedule:
    def __init__(self) -> None:
        self.schedule = {}
        self.scheduleOn = True

    # method specifies when to kick in scheduled heating
    def setUpSchedule(self, startTime,info):
        self.schedule[startTime] = info

    #*******WHEN ADDING TO SCHEDULE WOULD BE NICE TO CALL THE CHECKNEXTSCHEDULE AFTER ADDING TO THIS
    def addToSchedule(self,startTime,temp,endTime): #could have an override true or false that could be an optional input 
        scheduleList = [temp,endTime]
        if len(self.schedule) ==0:
            return self.setUpSchedule(startTime,scheduleList)#do we even need a separate method for this ?? - it's better in theory but stupid in practice
        else:
            #the time should be a string
            if startTime in self.schedule:
                #clash, for now we'll override this automatically
                #could add here ability to throw the option to user whether to overide or not - come back later on
                self.schedule[startTime] = scheduleList
            else:
                self.schedule[startTime] = scheduleList
    
    # Deletes Schedule Object From Schedule Dictionary 
    def deleteFromSchedule(self, start_time_key):
        for key in self.schedule:
            if key == start_time_key:
                del self.schedule[start_time_key]
                return "success"