"""
test_datefns.py - test datefns library
"""

from datetime import date
import os
import unittest
import sqlite3

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


class TestHolidayFn(unittest.TestCase):

    def test_new_years(self):
        self.assertEqual("New Year's", datefns.holiday_name(date(2018, 1, 1)))

    def test_day_after_new_years(self):
        self.assertIsNone(datefns.holiday_name(date(2018, 1, 2)))

    def test_mlk_day(self):
        self.assertEqual("Martin Luther King", datefns.holiday_name(date(2018, 1, 15)))
        # date(2018, 2, 19), date(2018, 2, 20), date(2018, 5, 21),
        # date(2018, 5, 28), date(2018, 5, 29), date(2018, 5, 31),
        # date(2018, 7, 4), date(2018, 9, 3), date(2018, 9, 10),
        # date(2018, 11, 22), date(2018, 11, 23), date(2018, 11, 29),
        # date(2018, 11, 30), date(2018, 12, 24), date(2018, 12, 25),
        # date(2018, 12, 31)]

    def test_thanksgiving_day(self):
        self.assertEqual("Thanksgiving", datefns.holiday_name(date(2018, 11, 22)))

    def test_day_after_thanksgiving_day(self):
        self.assertEqual("Day After Thanksgiving", datefns.holiday_name(date(2018, 11, 23)))

    def test_thanksgiving_day_on_fri_first_day(self):
        self.assertEqual("Thanksgiving", datefns.holiday_name(date(2019, 11, 28)))

    def test_day_after_thanksgiving_day_on_fri_first_day_good(self):
        self.assertEqual("Day After Thanksgiving", datefns.holiday_name(date(2019, 11, 29)))

    def test_day_after_thanksgiving_day_on_fri_first_day_bad(self):
        self.assertIsNone(datefns.holiday_name(date(2019, 11, 22)))

    def test_jul32019(self):
        self.assertIsNone(datefns.holiday_name(date(2019, 7, 3)))

    def test_jul42019(self):
        self.assertEqual("4th of July", datefns.holiday_name(date(2019, 7, 4)))


class TestTimeFns(unittest.TestCase):

    def test_insert_2xs(self):
        conn = sqlite3.connect(':memory:')
        ts = datefns.time_table()
        datefns.load_time_table(conn, ts)
        datefns.load_time_table(conn, ts)


if __name__ == '__main__':
    unittest.main()
