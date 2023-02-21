import unittest
from unittest.mock import patch, call
from app.severity import Severity

# https://docs.python.org/3/library/unittest.html


class TestSeverity(unittest.TestCase):

    def test_init_neglible(self):
        s = Severity.parse("NEGLIGIBLE")        
        self.assertEqual(s, Severity.LOW)
        
    def test_init_neglible_lc(self):
        s = Severity.parse("Negligible")
        self.assertEqual(s, Severity.LOW)

    def test_init_broken_str(self):
        with self.assertRaises(ValueError):
            s = Severity.parse("broken") 

    def test_init_low_int(self):
        s = Severity.parse(1)
        self.assertEqual(s, Severity.LOW)
        
    def test_init_med_int(self):
        s = Severity.parse(5)
        self.assertEqual(s, Severity.MEDIUM)

    def test_init_high_int(self):
        s = Severity.parse(8)
        self.assertEqual(s, Severity.HIGH)

    def test_init_crit_int(self):
        s = Severity.parse(9)
        self.assertEqual(s, Severity.CRITICAL)

    def test_init_broken_int_low(self):
        with self.assertRaises(ValueError):
            s = Severity.parse(-1)
    
    def test_init_broken_int_high(self):
        with self.assertRaises(ValueError):
            s = Severity.parse(42)

    def test_init_med_float(self):
        s = Severity.parse(5.3)
        self.assertEqual(s, Severity.MEDIUM)

    def test_to_str(self):
        s = Severity.parse(5.3)
        self.assertEqual(str(s), "MEDIUM")


if __name__ == '__main__':
    unittest.main()