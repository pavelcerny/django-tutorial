from django.test import TestCase
from django.utils import timezone
from .views import date_lt


class ViewMethodsTests(TestCase):
    def test_date_lt_with_earlier_year(self):
        """
        date_is_lt(first, second) should return True for lower year, higher year
        """
        years = 2
        days_per_year = 365.24
        now = timezone.now().date()
        two_years_ago = (timezone.now() - timezone.timedelta(days=(years * days_per_year))).date()
        self.assertIs(date_lt(two_years_ago, now), True)

    def test_date_lt_with_later_year(self):
        """
        date_is_lt(first, second) should return True for lower year, higher year
        """
        years = 2
        days_per_year = 365.24
        now = timezone.now().date()
        two_years_ago = (timezone.now() - timezone.timedelta(days=(years * days_per_year))).date()
        self.assertIs(date_lt(now, two_years_ago), False)

    def test_date_lt_with_earlier_month(self):
        """
        date_is_lt(first, second) should return True for lower month, higher month
        """
        months = 2
        days_per_month = 31
        two_months_ago = (timezone.now() - timezone.timedelta(days=(months * days_per_month))).date()
        now = timezone.now().date()
        self.assertIs(date_lt(two_months_ago, now), True)

    def test_date_lt_with_later_month(self):
        """
        date_is_lt(first, second) should return True for higher month, lower month
        """
        months = 2
        days_per_month = 365.24
        two_month_ago = (timezone.now() - timezone.timedelta(days=(months * days_per_month))).date()
        now = timezone.now().date()
        self.assertIs(date_lt(now, two_month_ago), False)

    def test_date_lt_with_earlier_day(self):
        """
        date_is_lt(first, second) should return True for lower day, higher day
        """
        days = 2
        two_days_ago = (timezone.now() - timezone.timedelta(days=days)).date()
        now = timezone.now().date()
        self.assertIs(date_lt(two_days_ago, now), True)

    def test_date_lt_with_later_day(self):
        """
        date_is_lt(first, second) should return True for higher day, lower day
        """
        days = 2
        two_days_ago = (timezone.now() - timezone.timedelta(days=days)).date()
        now = timezone.now().date()
        self.assertIs(date_lt(now,two_days_ago), False)

    def test_date_lt_with_same_day(self):
        """
        date_is_lt(first, second) should return True for same day, same day
        first is a year earlier
        """
        
        now = timezone.now()
        self.assertIs(date_lt(now, now), False)
