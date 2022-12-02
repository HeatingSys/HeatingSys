import unittest
import sys
sys.path.insert(0, "src")
from room import Room
from heater import Thermostat
from schedule import Schedule
from house import House

class TestRoom(unittest.TestCase):
    def setUp(self):
        self.house = House()
        self.house.addNewRoom(1)
        self.room1 = self.house.getRoom(1)
        self.room1.addToSchedule('10:00', 23, '15:00')

    def test_addDefaultToExistingSchedule(self):
        self.room1.defaultSchedule.addToSchedule('00:00',15,'06:59')
        self.room1.defaultSchedule.addToSchedule('07:00',21,'09:00')
        self.room1.defaultSchedule.addToSchedule('17:00',22,'22:00')
        self.room1.addDefaultToExistingSchedule()

        self.assertEqual(self.room1.getRoomSchedule(), {'10:00':[23,'15:00'],'00:00':[15,'06:59'], '07:00':[21,'09:00'], '17:00':[22,'22:00']})

    def test_defaultSchedulingOnly(self):
        self.room1.defaultSchedule.addToSchedule('00:00',15,'06:59')
        self.room1.defaultSchedule.addToSchedule('07:00',21,'09:00')
        self.room1.defaultSchedule.addToSchedule('17:00',22,'22:00')
        self.room1.addDefaultToExistingSchedule()

        self.assertEqual(self.room1.getRoomSchedule(), {'10:00':[23,'15:00'], '00:00':[15,'06:59'], '07:00':[21,'09:00'], '17:00':[22,'22:00']})

        self.room1.defaultSchedulingOnly()
        self.assertEqual(self.room1.getDefaultSchedule(), {'00:00':[15,'06:59'], '07:00':[21,'09:00'], '17:00':[22,'22:00']})

    def test_userProvidedSchedulingAndDefaultScheduling(self):
        self.room1.addToSchedule('15:10', 20, '15:30')

        self.assertEqual(self.room1.getRoomSchedule(), {'10:00':[23,'15:00'],'15:10':[20,'15:30']})

    def test_turnOffScheduling(self):
        self.assertFalse(self.room1.turnOffScheduling())

    def test_turnOnScheduling(self):
        self.assertTrue(self.room1)

    def test_checkTempPeriodically(self):
        temp = self.room1.checkTempPeriodically()
        on = self.room1.thermostat.heaterOn(20, 18, 19, 25)
        self.assertEqual(temp, on)

    def test_checkNextSchedule(self):
        self.room1.defaultSchedule.addToSchedule('09:30', 20, '16:00')
        self.room1.checkNextSchedule()




        

if __name__ == '__main__':
    unittest.main()