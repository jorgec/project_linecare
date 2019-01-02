from django.db.models import Count

from datesdim.constants import MONTH_CHOICES
from datesdim.models import DateDim
from doctor_profiles.models import DoctorProfile, MedicalInstitution
from doctor_profiles.models.medical_institution_doctor_models import MedicalInstitutionDoctor
from doctor_profiles.modules.analytics_api.serializers.patient_analytics_serializers import \
    PatientByCheckupAggregateSerializer


def patient_appointment_earnings(queryset):
    total = 0.0
    fees = {}
    for row in queryset:
        try:
            connection = MedicalInstitutionDoctor.objects.get(doctor=row.doctor,
                                                              medical_institution=row.medical_institution)
        except MedicalInstitutionDoctor.DoesNotExist:
            break

        try:
            fee = connection.metadata['fees'][row.type]
            fee_name = row.get_type_display()

            if row.type in fees:
                fees[row.type]['subtotal'] = fees[row.type]['subtotal'] + float(fee)
            else:
                fees[row.type] = {
                    'subtotal': float(fee),
                    'name': fee_name
                }
        except KeyError:
            fee = 0

        total = total + float(fee)

    return {
        'fees': fees,
        'total': total
    }


def patient_appointment_checkup_counts(queryset):
    aggregated = queryset.values(
        'type'
    ).annotate(
        type_count=Count('type')
    ).order_by(
        'type'
    )

    count_serializer = PatientByCheckupAggregateSerializer(
        list(aggregated.values('type', 'type_count')),
        many=True
    )

    return count_serializer.data


def patient_appointment_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year)

    data = {}

    for day in days:
        queryset_on_day = queryset.filter(schedule_day=day)

        data[str(day)] = {
            'earnings': patient_appointment_earnings(queryset_on_day),
            'counts': patient_appointment_checkup_counts(queryset_on_day)
        }

    return data


def patient_appointment_slice_by_year(queryset):
    data = {}
    year = queryset.first().schedule_day.year
    for month in MONTH_CHOICES:
        queryset_on_month = queryset.filter(schedule_day__month=month[0])

        data[month[1]] = {
            'month_numeric': month[0],
            'month_name': month[1],
            'year': year,
            'earnings': patient_appointment_earnings(queryset_on_month),
            'counts': patient_appointment_checkup_counts(queryset_on_month)
        }
    return data

def patient_appointment_slice_by_week(queryset):
    data = {}
    days = queryset.first().schedule_day.get_week()

    for day in days:
        queryset_on_day = queryset.filter(schedule_day=day)

        data[str(day)] = {
            'earnings': patient_appointment_earnings(queryset_on_day),
            'counts': patient_appointment_checkup_counts(queryset_on_day)
        }

    return data


def patient_appointment_slice_by_day(queryset):
    data = {}
    day = queryset.first().schedule_day

    queryset_on_day = queryset.filter(schedule_day=day)

    data[str(day)] = {
        'earnings': patient_appointment_earnings(queryset_on_day),
        'counts': patient_appointment_checkup_counts(queryset_on_day)
    }

    return data



def patient_appointment_build_filters(params):
    try:
        doctor = DoctorProfile.objects.get(id=params.get('doctor_id', None))
    except DoctorProfile.DoesNotExist:
        return False
    slice = params.get('slice', None)
    day_str = params.get('day', None)
    medical_institution_id = params.get('medical_institution_id', None)
    gender = params.get('gender', None)

    filters = {
        'doctor': doctor
    }

    if day_str:
        day = DateDim.objects.parse_get(day_str)
    else:
        day = DateDim.objects.today()

    if slice == 'day':
        filters['schedule_day'] = day
    elif slice == 'week':
        week = day.get_week()
        filters['schedule_day__in'] = week
    elif slice == 'month':
        filters['schedule_day__year'] = day.year
        filters['schedule_day__month'] = day.month
    elif slice == 'year':
        filters['schedule_day__year'] = day.year
    else:
        filters['schedule_day'] = day

    if medical_institution_id:
        try:
            medical_institution = MedicalInstitution.objects.get(id=medical_institution_id)
        except MedicalInstitution.DoesNotExist:
            return False
        filters['medical_institution'] = medical_institution

    if gender:
        filters['patient__gender__slug'] = gender

    return filters
