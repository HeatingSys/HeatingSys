import time
from room import *
from house import House
from datetime import datetime


def main():
    pass
    # the House interface goes here
    myHouse = House('24 bothar nua')
    myHouse.addNewRoom('bathroom')
    #this can run every 30 mins 
    myHouse.checkOutsideTempPeriodically()
    for room in myHouse.rooms:
        now = datetime.now().strftime("%H:%M")
        current = int(now[3] + now[4])
        if current >30:
            diff = current -30
            outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
        else:
            outOfRange = now[0]+now[1]+':' +str(current +30)
        val1 =int(outOfRange[0]+outOfRange[1])
        if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
            if int(room.nextSchedule[3] +room.nextSchedule[4]) >= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                #call scheduling 
                room.scheduling()
        
        room.checkTempPeriodically(myHouse.outsideTemp.getPreviousOutsideTemp,myHouse.outsideTemp.getCurrentOutsideTemp(),room.heatingPower)#what is our desired temp if no schedule 
    #myHouse.calculateMonthlyEnergy()
    time.sleep(10)#wait 30 mins










i =0
while i<10:
    main() 
    i +=1
