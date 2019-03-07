import calendar
import datetime
import re

import arrow
from arrow.parser import ParserError
from django.conf import settings
from django.db import models
from django.db.models import Q

from datesdim.constants import JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, \
    DECEMBER, MONTH_CHOICES


class DateDimQuerySet(models.QuerySet):
    def q1(self):
        return self.filter(
            Q(month=JANUARY) | Q(month=FEBRUARY) | Q(month=MARCH)
        )

    def q2(self):
        return self.filter(
            Q(month=APRIL) | Q(month=MAY) | Q(month=JUNE)
        )

    def q3(self):
        return self.filter(
            Q(month=JULY) | Q(month=AUGUST) | Q(month=SEPTEMBER)
        )

    def q4(self):
        return self.filter(
            Q(month=OCTOBER) | Q(month=NOVEMBER) | Q(month=DECEMBER)
        )

    def summer(self):
        return self.filter(
            Q(month=MARCH) | Q(month=APRIL) | Q(month=MAY)
        )

    def xmas(self):
        return self.filter(
            month=DECEMBER,
            day__gte=20,
            day__lte=31
        )

    def days_in_month(self, *, month, year):
        return self.filter(
            month=month,
            year=year
        )

    def get_days_between(self, *, start, end, day_filter=None, inclusive=True):
        if inclusive:
            filter = {
                'date_obj__gte': start.date_obj,
                'date_obj__lte': end.date_obj
            }
        else:
            filter = {
                'date_obj__gt': start.date_obj,
                'date_obj__lt': end.date_obj
            }

        if day_filter:
            filter['day_name__in'] = day_filter

        return self.filter(**filter)


class DateDimManager(models.Manager):
    def get_queryset(self):
        return DateDimQuerySet(self.model, using=self._db)

    def today(self):
        day = arrow.utcnow().to(settings.TIME_ZONE)
        return self.parse_get(day.format('YYYY-MM-DD'))

    def q1(self):
        return self.get_queryset().q1()

    def q2(self):
        return self.get_queryset().q2()

    def q3(self):
        return self.get_queryset().q3()

    def q4(self):
        return self.get_queryset().q4()

    def summer(self):
        return self.get_queryset().summer()

    def xmas(self):
        return self.get_queryset().xmas()

    def days_in_month(self, *, month, year):
        return self.get_queryset().days_in_month(month=month, year=year)

    def create(self, *args, **kwargs):
        try:
            d = self.model.objects.get(
                year=kwargs['year'],
                month=kwargs['month'],
                day=kwargs['day']
            )
            return d
        except self.model.DoesNotExist:
            super(DateDimManager, self).create(*args, **kwargs)
            d = self.model.objects.get(
                year=kwargs['year'],
                month=kwargs['month'],
                day=kwargs['day']
            )
            d.date_obj = arrow.get(str(d)).date()
            d.day_name = calendar.day_name[calendar.weekday(d.year, d.month, d.day)]
            d.week_day = calendar.weekday(d.year, d.month, d.day)
            d.week_month = (d.day // 7) + 1

            start_of_year = arrow.get('{}-01-01'.format(d.year))
            days_since_start = (arrow.get(d.date_obj) - start_of_year).days
            d.week_year = (days_since_start // 7) + 1
            d.save(using=self._db)
            return d

    def parse(self, s: str):
        try:
            date = datetime.datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            return False
        except TypeError:
            return False
        return {
            'year': date.year,
            'month': date.month,
            'day': date.day
        }

    def parse_get(self, str):
        if type(str) == self.model:
            return str

        date = self.parse(str)
        if date:
            try:
                return self.model.objects.get(
                    **date
                )
            except self.model.DoesNotExist:
                self.create(year=date['year'], month=date['month'], day=date['day'])
                return self.model.objects.get(
                    **date
                )
        return False

    def preload_year(self, *args, **kwargs):
        calendar.setfirstweekday(calendar.MONDAY)
        if not kwargs['year']:
            return False
        year = int(kwargs['year'])

        for month in MONTH_CHOICES:
            num_days = calendar.monthrange(year, month[0])[1]
            for day in range(1, num_days + 1):
                self.create(year=year, month=month[0], day=day)

    def get_days_between(self, *, start, end, day_filter=None, inclusive=True):
        if type(start) == str:
            start = self.parse_get(start)
            if not start:
                return False
        if type(end) == str:
            end = self.parse_get(end)
            if not end:
                return False
        return self.get_queryset().get_days_between(start=start, end=end, day_filter=day_filter, inclusive=inclusive)


class TimeDimQuerySet(models.QuerySet):
    def morning(self):
        return self.filter(
            hour__lte=12
        )

    def noon(self):
        return self.filter(
            hour__gte=12,
            hour__lte=13
        )

    def afternoon(self):
        return self.filter(
            hour__gte=3,
            hour__lte=18
        )

    def evening(self):
        return self.filter(hour__gte=18)


class TimeDimManager(models.Manager):
    def get_queryset(self):
        return TimeDimQuerySet(self.model, using=self._db)

    def morning(self):
        return self.get_queryset().morning()

    def noon(self):
        return self.get_queryset().noon()

    def afternoon(self):
        return self.get_queryset().afternoon()

    def evening(self):
        return self.get_queryset().evening()

    def convert_to_24(self, t):
        """Converts 12 hours time format to 24 hours
        """
        t = t.replace(' ', '').lower()
        if "am" in t or "pm" in t:
            try:
                _time = datetime.datetime.strptime(t, '%I:%M%p').time()
                return f'{_time.hour}:{_time.minute}'
            except ValueError:
                return False
        else:
            raise ValueError("Didn't end with AM or PM.")

    def parse(self, t):
        """
        Try to parse string (HH:MM) or datetime
        :param t:
        :type t:
        :return:
        :rtype:
        """
        if type(t) == str:
            t = t.lower()
            if "am" in t or "pm" in t:
                t = self.convert_to_24(t)
                if not t:
                    return False

            pattern = re.compile('^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$')
            match = pattern.match(t)
            if match:
                hour, min = [int(t) for t in match.group().split(":")]
                try:
                    t = self.get(
                        hour=hour,
                        minute=min
                    )
                    return t
                except self.model.DoesNotExist:
                    return False
            return False
        elif type(t) == datetime.datetime:
            try:
                t = self.get(
                    hour=t.hour,
                    minute=t.minute
                )
                return t
            except self.model.DoesNotExist:
                return False
        else:
            return False

    def create(self, *args, **kwargs):
        try:
            t = self.model.objects.get(
                hour=kwargs['hour'],
                minute=kwargs['minute']
            )
            return t
        except self.model.DoesNotExist:
            if kwargs['hour'] < 24 and kwargs['minute'] < 60:
                super(TimeDimManager, self).create(*args, **kwargs)
            else:
                return False

            t = self.model.objects.get(
                hour=kwargs['hour'],
                minute=kwargs['minute']
            )

            if t.hour > 0:
                t.minutes_since = (t.hour * 60) + t.minute
            else:
                t.minutes_since = t.minute

            t.save(using=self.db)
            return t

    def preload_times(self):
        for hour in range(0, 24):
            for minute in range(0, 60):
                self.create(
                    hour=hour,
                    minute=minute
                )
