import calendar

import arrow
from django.conf import settings
from django.db import models

from datesdim.constants import MONTH_CHOICES
from datesdim.managers import DateDimManager, TimeDimManager


class DateDim(models.Model):
    year = models.IntegerField(default=2018)
    month = models.PositiveIntegerField(choices=MONTH_CHOICES)
    day = models.PositiveSmallIntegerField()
    date_obj = models.DateField(blank=True, null=True)
    day_name = models.CharField(blank=True, null=True, max_length=12)
    week_day = models.PositiveSmallIntegerField(blank=True, null=True)
    week_month = models.PositiveSmallIntegerField(blank=True, null=True)
    week_year = models.PositiveSmallIntegerField(blank=True, null=True)

    objects = DateDimManager()

    class Meta:
        ordering = ('-year', '-month', '-day')
        unique_together = ('year', 'month', 'day')

    def __str__(self):
        return "{}-{}-{}".format(self.year, self.month_str(), self.day_str())

    def __sub__(self, other):
        x = self.obj()
        y = other.obj()

        return x - y

    def day_str(self):
        if self.day < 10:
            return '0{}'.format(self.day)
        return str(self.day)

    def month_str(self):
        if self.month < 10:
            return '0{}'.format(self.month)
        return str(self.month)

    def datestr(self):
        return self.__str__()

    def obj(self):
        return arrow.get(self.datestr())

    def nice_name(self):
        month_name = self.get_month_display()
        return f'{self.day_name}, {month_name} {self.day}, {self.year}'

    def get_weeks(self):
        c = calendar.Calendar(calendar.MONDAY)
        __weeks = c.monthdatescalendar(self.year, self.month)
        weeks = []
        for week in __weeks:
            days = [
                DateDim.objects.parse_get('{}-{}-{}'.format(
                    day.year,
                    day.month,
                    day.day
                ))
                for day in week
            ]
            weeks.append(days)
        return weeks

    def get_week(self):
        weeks = self.get_weeks()
        for week in weeks:
            if self in week:
                return week

    def tomorrow(self):
        return self.obj().shift(days=1).format('YYYY-MM-DD')

    def yesterday(self):
        return self.obj().shift(days=-1).format('YYYY-MM-DD')

    def next_month(self):
        return self.obj().shift(months=1).format('YYYY-MM-DD')

    def last_month(self):
        return self.obj().shift(months=-1).format('YYYY-MM-DD')

    def next_week(self):
        return self.obj().shift(weeks=1).format('YYYY-MM-DD')

    def last_week(self):
        return self.obj().shift(weeks=-1).format('YYYY-MM-DD')


class TimeDim(models.Model):
    hour = models.PositiveSmallIntegerField(blank=True, null=True)
    minute = models.PositiveSmallIntegerField(blank=True, null=True)
    minutes_since = models.PositiveSmallIntegerField(blank=True, null=True)

    objects = TimeDimManager()

    class Meta:
        ordering = ('-hour', '-minute')
        unique_together = ('hour', 'minute')

    def hour_str(self, hour):
        if hour < 10:
            return '0{}'.format(hour)
        else:
            return hour

    def minute_str(self, minute):
        if minute < 10:
            return '0{}'.format(minute)
        else:
            return minute

    def as_string(self):
        return self.__str__()

    def __str__(self):
        return '{}:{}'.format(self.hour_str(self.hour), self.minute_str(self.minute))  # 24-hour clock format

    def format_12(self):

        if self.hour >= 12:
            am_pm = 'PM'
            hour = self.hour - 12
        else:
            am_pm = 'AM'
            hour = self.hour

        return '{}:{} {}'.format(self.hour_str(hour), self.minute_str(self.minute), am_pm)
