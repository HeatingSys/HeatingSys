import unittest
import sys
sys.path.insert(0, "src")
from outsideTemp import OutsideTemp

class TestOutsideTemp(unittest.TestCase):
    def setUp(self):
        self.outside = OutsideTemp()

    def test_getgetCurrentOutsideTemperature(self):
        currentTemp = self.outside.getCurrentOutsideTemp()
        self.assertIn(currentTemp, self.outside.outsideTempsForNext4Hours)
        self.assertEqual(currentTemp, self.outside.outsideTempsForNext4Hours[self.outside.index])

    def test_getPreviousOutsideTemp(self):
        prevTemp = self.outside.getPreviousOutsideTemp()
        self.assertIn(prevTemp, self.outside.outsideTempsForNext4Hours)
        self.assertEqual(prevTemp, self.outside.outsideTempsForNext4Hours[self.outside.index - 1])

    def test_generateOutsideTempForFourHours(self):
        outsideTemp1 = self.outside.generateOutsideTempForFourHours()
        self.assertEqual(outsideTemp1, self.outside.generateOutsideTempForFourHours())
        self.assertTrue(self.outside.index != 0)


        

if __name__ == '__main__':
    unittest.main()

