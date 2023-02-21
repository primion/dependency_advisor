import unittest
from unittest.mock import patch, call
from app.version import Version

# https://docs.python.org/3/library/unittest.html


class TestVersion(unittest.TestCase):

    def test_init(self):
        v = Version("1.2.3")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.build, 3)
        self.assertEqual(v.extension, 0)

    def test_init_broken_string(self):
        with self.assertRaises(ValueError):
            v = Version("Broken")
    
    def test_init_broken_none(self):
        with self.assertRaises(ValueError):
            v = Version(None)

    def test_init_short(self):
        v = Version("1")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.build, 0)
        self.assertEqual(v.extension, 0)

    def test_init_broken_part2(self):
        with self.assertRaises(ValueError):
            v = Version("1.A.3.4")        

    def test_str(self):
        v = Version("1.2.3")
        self.assertEqual(str(v), "1.2.3-0")

    def test_equal(self):
        v1 = Version("1.2.3")
        v2 = Version("1.2.3")
        self.assertEqual(v1, v2)
        self.assertTrue(v1 == v2)

    def test_lt1(self):
        v1 = Version("1.2.0")
        v2 = Version("1.2.3")        
        self.assertTrue(v1 < v2)

    def test_lt2(self):
        v1 = Version("1.0.5")
        v2 = Version("1.2.3")        
        self.assertTrue(v1 < v2)

    def test_lt3(self):
        v1 = Version("0.5.5")
        v2 = Version("1.2.3")        
        self.assertTrue(v1 < v2)

    def test_gt1(self):
        v1 = Version("1.2.0")
        v2 = Version("1.2.3")        
        self.assertTrue(v2 > v1)

    def test_gt2(self):
        v1 = Version("1.0.5")
        v2 = Version("1.2.3")        
        self.assertTrue(v2 > v1)

    def test_gt3(self):
        v1 = Version("0.5.5")
        v2 = Version("1.2.3")        
        self.assertTrue(v2 > v1)


if __name__ == '__main__':
    unittest.main()
