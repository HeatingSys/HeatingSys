#I'm separating this from room for now - I think it's just cleaner and doesn't bloat room
# open to changing this back - shouldn't be a big deal to change back
class Schedule:
    def __init__(self) -> None:
        self.schedule = {}
        self.scheduleOn = True

    
    # method specifies when to kick in scheduled heating
    def setUpSchedule(self,startTime,info):
        self.schedule[startTime] = info

    #from user persepective the user will initally try setup schedule and setUpSchedule should be called from inside here
    # So from the website perspective a user submits a form with startime , temp and endtime of the schedule and this method is called
    # regardless of whether self.schedule is empty yet or 
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
                print(startTime,' added to Schedule')
    
    #the todelete should be starting time I guess 
    #*******not been tested yet 
    def deleteFromSchedule(self,todelete):
        for key in self.schedule:
            if key == todelete:
                del self.schedule[key]
                return
