import unittest
from room import Room

class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room1 = Room('bedroom1', 17)
        self.room1.roomSchedule.addToSchedule('10:00', 23, '17:00')
        self.room1.roomSchedule.addToSchedule('09:00', 23, '15:00')


    def test_addDefaultToExistingSchedule(self):
        self.room1.defaultSchedule.addToSchedule('09:30', 20, '16:00')
        self.room1.addDefaultToExistingSchedule()

        self.assertEqual(self.room1.roomSchedule.schedule, {'10:00':[23,'17:00'], '09:00':[23,'15:00'], '09:30':[20,'16:00']})

    def test_defaultSchedulingOnly(self):
        self.room1.defaultSchedule.addToSchedule('09:30', 20, '16:00')
        self.room1.addDefaultToExistingSchedule()

        self.assertEqual(self.room1.roomSchedule.schedule, {'10:00':[23,'17:00'], '09:00':[23,'15:00'], '09:30':[20,'16:00']})

        self.room1.defaultSchedulingOnly()
        self.assertEqual(self.room1.roomSchedule.schedule, {'09:30':[20,'16:00']})

    def test_turnOffScheduling(self):
        self.assertFalse(self.room1.turnOffScheduling())

    def test_turnOnScheduling(self):
        self.assertTrue(self.room1)

    def test_checkTempPeriodically(self):
        temp = self.room1.checkTempPeriodically(18, 19, 25)
        on = self.room1.thermostat.heaterOn(20, 18, 19, 25)
        self.assertEqual(temp, on)

    def test_checkNextSchedule(self):
        self.room1.defaultSchedule.addToSchedule('09:30', 20, '16:00')
        self.room1.checkNextSchedule()




        

if __name__ == '__main__':
    unittest.main()