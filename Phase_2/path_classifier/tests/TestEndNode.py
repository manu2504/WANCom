import unittest
import models.EndNode as n

class TestEndNode(unittest.TestCase):
    def setUp(self):
        self.a = n.EndNode('192.168.0.1', id = 1)
        self.b = n.EndNode('192.168.0.1')
        self.c = n.EndNode('192.168.0.3')

    def testEquality(self):
        self.assertTrue(self.a == self.a)
        self.assertTrue(self.b == self.b)
        self.assertTrue(self.c == self.c)
        self.assertTrue(self.a == self.b)
        self.assertFalse(self.a == self.c)
        self.assertFalse(self.b == self.c)

    def testIp(self):
        self.assertEqual(self.a.ip,"192.168.0.1")
        self.assertNotEqual(self.a.ip,"192.168.0.3")
        self.assertEqual(self.a.ip, self.b.ip)
        self.assertEqual(self.b.ip,"192.168.0.1")
        self.assertEqual(self.c.ip, "192.168.0.3")


if __name__ == '__main__':
    unittest.main()
