import unittest
import models.Measurement as m

class TestMeasurement(unittest.TestCase):
    def setUp(self):
        self.m1 = m.Measurement(66, 1476351846113)
        self.m2 = m.Measurement(69, 1476351876762)
        self.m3 = m.Measurement(62, 1476351898901)
        self.m4 = m.Measurement(66, 1476351846113)

    def testEquality(self):
        self.assertNotEqual(self.m1, self.m2)
        self.assertNotEqual(self.m2, self.m3)
        self.assertNotEqual(self.m3, self.m4)
        self.assertEqual(self.m1, self.m4)

if __name__ == '__main__':
    unittest.main()
