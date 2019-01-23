import pytest
import arrow
from mixer.backend.django import mixer

from datesdim.models import DateDim

pytestmark = pytest.mark.django_db


class TestDatesDimModels:
    def test_init(self):
        obj = mixer.blend('accounts.Account')
        assert obj.pk is not None, "Should save an instance"

    def test_date_data(self):
        obj = DateDim.objects.create(
            year=2018,
            month=10,
            day=2
        )

        # test creation of date_obj
        d = arrow.get('2018-10-02')

        assert obj.date_obj is not None, "date_obj was not created"

        assert d.date() == obj.date_obj, "{} must be equal to {}, got {} instead".format(
            d.date(), obj.date_obj, obj.date_obj
        )

        assert obj.day_name == 'Tuesday', "dayname should be Tuesday, got {} instead".format(
            obj.day_name
        )

        assert obj.week_day == 1, "week_day should be 1, got {} instead".format(
            obj.week_day
        )

        assert obj.week_month == 1, "week_month should be 1, got {} instead".format(
            obj.week_month
        )

        assert obj.week_year == 40, "week_year should be 40, got {} instead".format(
            obj.week_year
        )

        assert obj.obj() == d

        assert obj.datestr() == d.format('YYYY-MM-DD')

    def test_subtract(self):
        obj1 = DateDim.objects.create(
            year=2018,
            month=10,
            day=2
        )

        # test creation of date_obj
        d1 = arrow.get('2018-10-02')

        obj2 = DateDim.objects.create(
            year=2018,
            month=10,
            day=10
        )

        # test creation of date_obj
        d2 = arrow.get('2018-10-10')

        assert obj1 - obj2 == d1 - d2, f"Expected {d1 - d2}, got {obj1 - obj2}"

    def test_day_str(self):
        obj = DateDim.objects.create(
            year=2018,
            month=10,
            day=2
        )

        assert obj.day_str() == '02', f"Expected 02, got {obj.day_str()}"

    def test_nice_name(self):
        obj = DateDim.objects.create(
            year=2019,
            month=1,
            day=23
        )

        assert obj.nice_name() == 'Wednesday, January 23, 2019'