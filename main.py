import time
from src.room import *
from src.house import House
from datetime import datetime

global user_house
user_house = House()

global now
now = datetime.now().strftime("%H:%M")

def main():
    while True:
        time.sleep(10)#wait 30 mins
        user_house.checkOutsideTempPeriodically()

        for room in user_house.rooms:
            current = int(now[3] + now[4])
            diffSet = False
            if current >30:
                diff = current -30
                if diff <10:
                    diff = str('0'+ str(diff))
                outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
                diffSet = True
            else:
                outOfRange = now[0]+now[1]+':' +str(current +30)
            val1 =int(outOfRange[0]+outOfRange[1])
            if room.heatingRunning is False:
                if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
                    if int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                        #call scheduling 
                        room.scheduling()
                    elif int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) >=int(outOfRange[0]+outOfRange[1]) and diffSet is True:
                        room.scheduling()
            else:
                room.endSchedule()
            
            user_house.calculateEnergyUse()
            
            room.checkTempPeriodically()
        
        
        '''current_usage = str(user_house.getMonthlyEnergy())
        gauge = str(user_house.getEnergyHoursGuage())
        exceeded = str(user_house.getMonthlyEnergyExceeded())
        stats = str(user_house.getPastMonthStats())
        limit = str(user_house.getMonthlyEnergyLimit())
        print(current_usage, "current_usage")
        print(gauge, "gauge")
        print(exceeded, "exceeded")
        print(stats, "stats")
        print(limit, "limit")'''
        
        # reset
        # user_house.resetNewMonthEnergyStats()


'''
user_house.addNewRoom(1)
user_house.addNewRoom(2)
user_house.getAllRooms()
user_house.getRoom(1).addToSchedule("15:00",30,'16:00')
user_house.getRoom(1).addToSchedule("10:00",20,'12:00')



user_house.getRoom(1).checkNextSchedule()

user_house.setHeatingPower(1500)
user_house.setMonthlyEnergyLimit(50)

main()
'''