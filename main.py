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
        time.sleep(5)
        user_house.checkOutsideTempPeriodically()

        for room in user_house.rooms:
            current = int(now[3] + now[4])
            diffSet = False
            if current > 30:
                diff = current - 30
                if diff < 10:
                    diff = str('0'+ str(diff))
                outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
                diffSet = True
            else:
                outOfRange = now[0]+now[1]+':' +str(current +30)
            val1 =int(outOfRange[0]+outOfRange[1])
            if room.heatingRunning is False:
                if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
                    if int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                        room.scheduling()
                    elif int(room.nextSchedule[3] +room.nextSchedule[4]) <= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) >=int(outOfRange[0]+outOfRange[1]) and diffSet is True:
                        room.scheduling()
            else:
                room.endSchedule()
            
            user_house.calculateEnergyUse()
            room.checkTempPeriodically()
        
        
        current_usage = str(user_house.getMonthlyEnergy())
        gauge = str(user_house.getEnergyHoursGuage())
        exceeded = str(user_house.getMonthlyEnergyExceeded())
        stats = str(user_house.getPastMonthStats())
        limit = str(user_house.getMonthlyEnergyLimit())
        print(current_usage, "current_usage")
        print(gauge, "gauge")
        print(exceeded, "- exceeded or not?")
        print(stats, "stats")
        print(limit, "limit")
        
        room_temp = str(user_house.getRoom(1).getCurrentTemp())
        heater_state = str(user_house.getRoom(1).heatingRunning)
        print(room_temp, " - room_temp")
        print(heater_state, "- heater_state")
        
        
        # reset all energy calculating variables on the 1st of every month
        today = datetime.today().strftime('%d')
        if today == '01':
            user_house.resetNewMonthEnergyStats()


user_house.addNewRoom(1)

#self.defaultSchedule.addToSchedule('00:00',15,'06:59')
#self.defaultSchedule.addToSchedule('07:00',21,'09:00')
#self.defaultSchedule.addToSchedule('17:00',22,'22:00')

user_house.getRoom(1).addToSchedule("12:00",20,"12:45")
user_house.getRoom(1).checkNextSchedule()

main()