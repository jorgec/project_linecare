import calendar

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


class DateDimManager(models.Manager):
    def get_queryset(self):
        return DateDimQuerySet(self.model, using=self._db)

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

    def parse(self, str):
        try:
            date = arrow.get(str)
        except ParserError:
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
        try:
            return self.model.objects.get(
                **date
            )
        except self.model.DoesNotExist:
            return False

    def preload_year(self, *args, **kwargs):
        if not kwargs['year']:
            return False
        year = int(kwargs['year'])

        for month in MONTH_CHOICES:
            num_days = calendar.monthrange(year, month[0])[1]
            for day in range(1, num_days + 1):
                self.create(year=year, month=month[0], day=day)
