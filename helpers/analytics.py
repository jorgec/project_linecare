from helpers.colors import MColors
from locations.models import Country
from profiles.models import Gender
from visits.models import VisitDay


def split_by_genders(visit_days: VisitDay) -> list:
    """
    Split VisitDays queryset by gender
    """

    if not visit_days:
        return []

    genders = Gender.objects.all()
    gender_splits = []

    colors = MColors()

    for gender in genders:
        visit_days_filtered = visit_days.filter(
            visit__user__account_profiles__gender_id=gender.pk
        ).values('visit__user').distinct()
        gender_splits.append(
            {
                'name': gender.name,
                'slug': gender.slug,
                'pk': gender.pk,
                'visit_days': visit_days_filtered,
                'count': visit_days_filtered.count(),
                'color': colors.get_color()
            }
        )

    return gender_splits


def split_by_origin(visit_days: VisitDay) -> list:
    """
    Split VisitDays queryset by country of origin
    """
    if not visit_days:
        return []

    colors = MColors()

    countries = []
    country_splits = []
    for visit_day in visit_days:
        if visit_day.visit.user.base_profile().country_of_origin.pk not in countries:
            countries.append(visit_day.visit.user.base_profile().country_of_origin.pk)

    for country in countries:
        c = Country.objects.get(pk=country)
        visit_days_filtered = visit_days.filter(
            visit__user__account_profiles__country_of_origin_id=country
        ).values('visit__user').distinct()
        country_splits.append(
            {
                'name': c.name,
                'slug': c.slug,
                'pk': c.pk,
                'visit_days': visit_days_filtered,
                'count': visit_days_filtered.count(),
                'color': colors.get_color()
            }
        )

    return country_splits
