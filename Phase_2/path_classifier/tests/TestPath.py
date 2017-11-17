import unittest
import models.Path as p
import models.Measurement as m

class TestPath(unittest.TestCase):
    def setUp(self):
        self.h1 = ['192.168.0.1', '192.168.0.36', '192.168.0.28',
            '192.168.0.34', '192.168.0.42', '192.168.0.3']
        self.h2 = ['192.168.0.2', '192.168.0.136', '192.168.0.8',
            '192.168.0.16', '192.168.0.39', '192.168.0.146', '192.168.0.3']
        self.h3 = ['192.168.0.1', '192.168.0.136', '192.168.0.8', '192.168.0.18'
            '192.168.0.16', '192.168.0.39', '192.168.0.146', '192.168.0.4']

        self.p1 = p.Path(hops=self.h1, id=1)
        self.p2 = p.Path(hops=self.h2, id=2)
        self.p3 = p.Path(hops=self.h3, id=3)
        self.p4 = p.Path(hops=self.h1, id=4)

        self.m1 = m.Measurement(66, 1476351846113)
        self.m2 = m.Measurement(69, 1476351876762)
        self.m3 = m.Measurement(62, 1476351898901)
        self.m4 = m.Measurement(66, 1476351846113)

    def testEquality(self):
        self.assertNotEqual(self.p1, self.p2)
        self.assertNotEqual(self.p2, self.p3)
        self.assertNotEqual(self.p3, self.p4)
        self.assertEqual(self.p1, self.p4)

    def testSource(self):
        self.assertEqual(self.p1.source(), self.h1[0])
        self.assertEqual(self.p2.source(), self.h2[0])
        self.assertEqual(self.p3.source(), self.h3[0])
        self.assertEqual(self.p4.source(), self.h1[0])
        self.assertEqual(self.p1.source(), '192.168.0.1')

    def testDestination(self):
        self.assertEqual(self.p1.destination(), self.h1[-1])
        self.assertEqual(self.p2.destination(), self.h2[-1])
        self.assertEqual(self.p3.destination(), self.h3[-1])
        self.assertEqual(self.p4.destination(), self.h1[-1])
        self.assertEqual(self.p1.destination(), '192.168.0.3')

    def testAddMeasurement(self):
        self.p1.addMeasurement(self.m1)
        self.assertEqual(len(self.p1.measurements), 1)
        self.p1.addMeasurement(self.m2)
        self.assertEqual(len(self.p1.measurements), 2)
        self.assertEqual(self.p1.measurements[0], self.m1)
        self.assertEqual(self.p1.measurements[1], self.m2)

if __name__ == '__main__':
    unittest.main()
