from room import *
from house import House
from datetime import datetime


def main():
    myHouse = House('24 bothar nua')
    myHouse.addNewRoom('bathroom')
    #this can run forever and forever or we can do every 30 mins 
    for room in myHouse.rooms():
        now = datetime.now().strftime("%H:%M")
        current = int(now[3] + now[4])
        if current >30:
            diff = current -30
            outOfRange = str()
        outOfRange = current +30
        
        if self.



        
       


if __name__ == '__main__':
    main()