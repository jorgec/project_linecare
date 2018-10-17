import arrow
from django.conf import settings
from django.db import models

from datesdim.constants import MONTH_CHOICES
from datesdim.managers import DateDimManager


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

    def __str__(self):
        return "{}-{}-{}".format(self.year, self.month_str(), self.day_str())

    def __sub__(self, other):
        x = self.obj()
        y = other.obj()

        return x - y
