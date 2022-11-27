import time
from room import *
from house import House
from datetime import datetime

global user_house
user_house = House()

global now
now = datetime.now().strftime("%H:%M")

def main():
    while True:
        time.sleep(30)#wait 30 mins
        user_house.checkOutsideTempPeriodically()
        for room in user_house.rooms:
            current = int(now[3] + now[4])
            if current >30:
                diff = current -30
                outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
            else:
                outOfRange = now[0]+now[1]+':' +str(current +30)
            val1 =int(outOfRange[0]+outOfRange[1])
            if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
                room.scheduling()
                if int(room.nextSchedule[3] +room.nextSchedule[4]) >= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                    #call scheduling 
                    room.scheduling()
            
            room.checkTempPeriodically()#what is our desired temp if no schedule 
        #user_house.calculateMonthlyEnergy() '''


#have to set heating power in house

'''user_house.addNewRoom(1)
user_house.addNewRoom(2)
user_house.getAllRooms()
user_house.getRoom(1).addToSchedule("14:00",15,'16:00')
user_house.getRoom(1).addToSchedule("10:00",20,'12:00')
user_house.getRoom(1).addToSchedule("14:00",18,'14:02')
user_house.getRoom(1).checkNextSchedule()
user_house.deleteRoom(2)
user_house.getAllRooms()
main()'''