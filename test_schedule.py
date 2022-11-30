import unittest
from schedule import Schedule


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.schedule1 = Schedule()

    def test_addToSchedule(self):
        self.assertEqual(self.schedule1.schedule, {})

        self.schedule1.addToSchedule('10:00', 23, '17:00')
        self.assertEqual(self.schedule1.schedule, {'10:00':[23, '17:00']})

        self.schedule1.addToSchedule('09:00', 23, '16:00')
        self.assertEqual(self.schedule1.schedule, {'10:00':[23, '17:00'], '09:00':[23, '16:00']})

        self.schedule1.addToSchedule('16:00', -15, '17:00')
        self.assertEqual(self.schedule1.schedule, {'10:00':[23, '17:00'], '09:00':[23, '16:00'], '16:00':[-15, '17:00']})

    def test_deleteFromSchedule(self):
        self.schedule1.addToSchedule('10:00', 23, '17:00')
        self.schedule1.addToSchedule('09:00', 23, '16:00')
        self.schedule1.addToSchedule('16:00', -15, '17:00')

        self.schedule1.deleteFromSchedule('10:00')
        self.assertEqual(self.schedule1.schedule, {'09:00':[23, '16:00'], '16:00':[-15, '17:00']})

        self.schedule1.deleteFromSchedule('16:00')
        self.assertEqual(self.schedule1.schedule, {'09:00':[23, '16:00']})


if __name__ == '__main__':
    unittest.main()