from datetime import date

from django.test import TestCase
from utils.utils import format_date


class FormatDateTests(TestCase):
    def test_format_date_valid(self):
        self.assertEqual(format_date("2024-06-22"), date(2024, 6, 22))

    def test_format_date_none(self):
        self.assertIsNone(format_date(None))

    def test_format_date_invalid(self):
        with self.assertRaises(ValueError):
            format_date("22-06-2024")
