import sys
sys.path.insert(0, "src")
from src.room import Room
from src.heater import Thermostat
from src.schedule import Schedule
from src.house import House

user_house = House()

def test():
    # 1. House tests:
    #   - tests to add rooms
    #   - tests to delete rooms
    #   - tests to see all the rooms currently in the house
    user_house.addNewRoom('Bedroom')
    user_house.addNewRoom('Kitchen')
    print("All rooms in the house right now:")
    user_house.getAllRooms()

    user_house.deleteRoom("Kitchen")
    print("All rooms after deletion: ")
    user_house.getAllRooms()

    # 2. Schedule tests:
    #   - tests to add to a schedule
    #   - tests to see the default schedule
    #   - tests to see the entire schedule
    #   - tests to delete a schedule entry
    #   - tests to delete the entire schedule
    user_house.getRoom('Bedroom').addToSchedule("13:00",20,'15:00')
    user_house.getRoom('Bedroom').addToSchedule("15:00",20,'17:00')

    print("The default schedule for the bedroom is:", user_house.getRoom('Bedroom').getDefaultSchedule())

    schedule = {**user_house.getRoom('Bedroom').getDefaultSchedule(),**user_house.getRoom('Bedroom').getRoomSchedule()}
    print("The entire schedule for the bedroom is:", schedule)

    user_house.getRoom('Bedroom').deleteOneEntry("13:00")
    schedule_after_deletion = {**user_house.getRoom('Bedroom').getDefaultSchedule(),**user_house.getRoom('Bedroom').getRoomSchedule()}
    print("New schedule after deletion is:", schedule_after_deletion)

    user_house.getRoom("Bedroom").deleteEntireSchdule()
    print("Schedule after deletion:", user_house.getRoom("Bedroom").getRoomSchedule())

    user_house.getRoom('Bedroom').addToSchedule("22:10",20,'22:20')

    # 3. Temperature tests:
    #   - test to check current temperature in the room
    room_temp = user_house.getRoom("Bedroom").getCurrentTemp()
    print("Current temperature of bedroom is:", room_temp)

    # 4. Heating tests:
    #   - test to check if heating running currently
    heater_state = user_house.getRoom("Bedroom").heatingRunning
    print("current heater state:", heater_state)

    #5. Statistics
    #   - test to set the heater power
    #   - test to set the monthly energy limit
    #   - test to check current energy use
    #   - test to see how much longer the heater should stay on
    #   - test to see if the energy limit has exceeded
    #   - test to check previous month energy use
    user_house.setHeatingPower(1500)

    user_house.setMonthlyEnergyLimit(300)
    limit = str(user_house.getMonthlyEnergyLimit())
    print("Monthly energy limit: ", limit)

    user_house.checkOutsideTempPeriodically()
    current_usage = str(user_house.getMonthlyEnergy())
    print("Current Energy Usage: ", current_usage)

    gauge = str(user_house.getEnergyHoursGuage())
    print("How much longer heating should stay on:", gauge)

    exceeded = str(user_house.getMonthlyEnergyExceeded())
    print("Has the monthly energy limit been exceeded?: ", exceeded)

    stats = str(user_house.getPastMonthStats())
    print("Monthly past statistics: ", stats)

test()