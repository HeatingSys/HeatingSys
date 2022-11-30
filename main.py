import time
from room import *
from house import House
from datetime import datetime


def main():
    while True:
    # the House interface goes here

        print("Outside Temperature:",myHouse.outsideTemp.getCurrentOutsideTemp())
        #this can run every 30 mins 
        myHouse.checkOutsideTempPeriodically()
        for room in myHouse.rooms:
            #room.addToSchedule("16:20",'20','16:00')
            room.getCurrentTemp()
            print()
            now = datetime.now().strftime("%H:%M")
            diffr = False
            current = int(now[3] + now[4])
            if current >30:
                diff = current -30
                if diff <10:
                    diff = str('0'+ str(diff))
                outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
                diffr = True
                
            else:
                outOfRange = now[0]+now[1]+':' +str(current +30)
            val1 =int(outOfRange[0]+outOfRange[1])
            if room.heatingRunning is False:
                if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
                    #room.scheduling()
                    fff = room.nextSchedule[3] +room.nextSchedule[4]
                    ffff= int(room.nextSchedule[3] +room.nextSchedule[4]) >= int(now[3]+now[4])
                    ddddd = int(now[3]+now[4])
                    uuuuu = int(outOfRange[0]+outOfRange[1])
                    if int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                        #call scheduling 
                        room.scheduling()
                    elif int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) >=int(outOfRange[0]+outOfRange[1]) and diffr is True:
                        room.scheduling()
            else:
                room.endSchedule()
            room.checkTempPeriodically()#what is our desired temp if no schedule 
            #gonna need a checker to turn off heater when schedule is done basically 
        #myHouse.calculateMonthlyEnergy()
        time.sleep(3)#wait 30 mins

# print the current external temperature
# Print new room is added - print the room object
# Print new schedule is added - print the schedule object
    # To prove that the new room and schedule is definitely present in memory by printing the room id and all the schedules associated with it
# Print current room temp of: eg room id 1
# Then just print the inside temperature on each iteration - gotta show the inside temp of that room is changing thanks to maths we have





#have to set heating power in house


global myHouse
myHouse = House('24 bothar nua')
myHouse.addNewRoom('bathroom')
myHouse.rooms[0].addToSchedule("16:30",20,'16:35')
myHouse.rooms[0].checkNextSchedule()
main()