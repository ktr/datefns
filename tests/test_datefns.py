"""
test_datefns.py - test datefns library
"""

from datetime import date
import os
import unittest

from .context import datefns


class TestWeekEndingFn(unittest.TestCase):

    def setUp(self):
        self.days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def test_monday(self):
        d1 = date(2018, 7, 9)
        expected = (
            date(2018, 7, 9), # M
            date(2018, 7, 10), # T
            date(2018, 7, 11), # W
            date(2018, 7, 12), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_tuesday(self):
        d1 = date(2018, 7, 10)
        expected = (
            date(2018, 7, 16), # M
            date(2018, 7, 10), # T
            date(2018, 7, 11), # W
            date(2018, 7, 12), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_wednesday(self):
        d1 = date(2018, 7, 11)
        expected = (
            date(2018, 7, 16), # M
            date(2018, 7, 17), # T
            date(2018, 7, 11), # W
            date(2018, 7, 12), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_thursday(self):
        d1 = date(2018, 7, 12)
        expected = (
            date(2018, 7, 16), # M
            date(2018, 7, 17), # T
            date(2018, 7, 18), # W
            date(2018, 7, 12), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_friday(self):
        d1 = date(2018, 7, 13)
        expected = (
            date(2018, 7, 16), # M
            date(2018, 7, 17), # T
            date(2018, 7, 18), # W
            date(2018, 7, 19), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_saturday(self):
        d1 = date(2018, 7, 14)
        expected = (
            date(2018, 7, 16), # M
            date(2018, 7, 17), # T
            date(2018, 7, 18), # W
            date(2018, 7, 19), # T
            date(2018, 7, 20), # F
            date(2018, 7, 14), # S
            date(2018, 7, 15), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))

    def test_sunday(self):
        d1 = date(2018, 7, 8)
        expected = (
            date(2018, 7, 9), # M
            date(2018, 7, 10), # T
            date(2018, 7, 11), # W
            date(2018, 7, 12), # T
            date(2018, 7, 13), # F
            date(2018, 7, 14), # S
            date(2018, 7, 8), # S
        )
        for pos, day in enumerate(self.days):
            self.assertEqual(expected[pos], datefns.week_ending(d1, day))


if __name__ == '__main__':
    unittest.main()
