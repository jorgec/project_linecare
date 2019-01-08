import pandas as pd
from django.db.models import Count

from datesdim.constants import MONTH_CHOICES
from datesdim.models import DateDim
from doctor_profiles.models import DoctorProfile, MedicalInstitution, PatientCheckupRecord, PatientSymptom, \
    PatientFinding, PatientDiagnosis
from doctor_profiles.models.patient_checkup_models import Prescription, PatientLabTestRequest
from doctor_profiles.modules.analytics_api.serializers.patient_analytics_serializers import \
    PatientByCheckupAggregateSerializer


def patient_appointment_earnings(queryset):
    total = 0.0
    fees = {}
    for row in queryset:
        try:
            # fee = connection.metadata['fees'][row.type]
            fee = row.fee
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
    total = queryset.count()
    aggregated = queryset.values(
        'type'
    ).annotate(
        type_count=Count('type')
    ).order_by(
        'type'
    )

    if aggregated.count() > 0:

        count_serializer = PatientByCheckupAggregateSerializer(
            list(aggregated.values('type', 'type_count')),
            many=True
        )

        return {
            'items': count_serializer.data,
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_symptoms_counts(queryset):
    records = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    patient_symptoms = PatientSymptom.objects.filter(checkup__in=records)
    total = patient_symptoms.count()

    aggregate = patient_symptoms.values('symptom__name').annotate(scount=Count('symptom')).order_by('symptom__name')

    if total > 0:
        return {
            'items': list(
                aggregate.values(
                    'symptom__name',
                    'scount'
                )
            ),
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_appointment_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}

    dataset_keys = {(c.type, c.get_type_display()) for c in queryset}
    for day in days:
        labels.append(str(day))

        queryset_on_day = queryset.filter(schedule_day=day)

        dataset = {}
        if queryset_on_day.count() > 0:
            df = pd.DataFrame(list(queryset_on_day.values()))

            splits = dict(df.groupby('type').type.count())
            for dk in dataset_keys:
                if dk[0] in splits:
                    dataset[dk[0]] = {
                        'label': dk[1],
                        'slug': dk[0],
                        'count': splits[dk[0]]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk[0]] = {
                    'label': dk[1],
                    'slug': dk[0],
                    'count': 0
                }

        datasets[str(day)] = dataset

    return datasets, labels, dataset_keys


def patient_appointment_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    dataset_keys = {(c.type, c.get_type_display()) for c in queryset}
    for month in MONTH_CHOICES:
        queryset_on_month = queryset.filter(schedule_day__month=month[0])
        labels.append(month[1])
        dataset = {}
        if queryset_on_month.count() > 0:
            df = pd.DataFrame(list(queryset_on_month.values()))
            splits = dict(df.groupby('type').type.count())

            for dk in dataset_keys:
                if dk[0] in splits:
                    dataset[dk[0]] = {
                        'label': dk[1],
                        'slug': dk[0],
                        'count': splits[dk[0]]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk[0]] = {
                    'label': dk[1],
                    'slug': dk[0],
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys


def patient_appointment_slice_by_week(queryset):
    labels = []
    days = queryset.first().schedule_day.get_week()
    datasets = {}

    dataset_keys = {(c.type, c.get_type_display()) for c in queryset}
    for day in days:
        labels.append(str(day))

        queryset_on_day = queryset.filter(schedule_day=day)

        dataset = {}
        if queryset_on_day.count() > 0:
            df = pd.DataFrame(list(queryset_on_day.values()))

            splits = dict(df.groupby('type').type.count())
            for dk in dataset_keys:
                if dk[0] in splits:
                    dataset[dk[0]] = {
                        'label': dk[1],
                        'slug': dk[0],
                        'count': splits[dk[0]]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk[0]] = {
                    'label': dk[1],
                    'slug': dk[0],
                    'count': 0
                }

        datasets[str(day)] = dataset

    return datasets, labels, dataset_keys


def patient_appointment_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    dataset_keys = {(c.type, c.get_type_display()) for c in queryset}

    for hour in labels:
        queryset_on_hour = queryset.filter(time_start__hour=hour)
        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values()))

            splits = dict(df.groupby('type').type.count())
            for dk in dataset_keys:
                if dk[0] in splits:
                    dataset[dk[0]] = {
                        'label': dk[1],
                        'slug': dk[0],
                        'count': splits[dk[0]]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk[0]] = {
                    'label': dk[1],
                    'slug': dk[0],
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys


def patient_symptoms_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    symptoms = PatientSymptom.objects.filter(checkup__in=checkups)
    dataset_keys = {c.symptom.name for c in symptoms}

    for hour in labels:
        queryset_on_hour = PatientSymptom.objects.filter(checkup__in=checkups.filter(appointment__time_start__hour=hour))

        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values('symptom', 'symptom__name')))

            splits = dict(df.groupby('symptom__name').symptom.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys


def patient_symptoms_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    symptoms = PatientSymptom.objects.filter(checkup__in=checkups)
    dataset_keys = {c.symptom.name for c in symptoms}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        symptoms_on_day = PatientSymptom.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if symptoms_on_day.count() > 0:
            df = pd.DataFrame(list(symptoms_on_day.values('symptom', 'symptom__name')))

            splits = dict(df.groupby('symptom__name').symptom.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_symptoms_slice_by_week(queryset):
    days = queryset.first().schedule_day.get_week()

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    symptoms = PatientSymptom.objects.filter(checkup__in=checkups)
    dataset_keys = {c.symptom.name for c in symptoms}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        symptoms_on_day = PatientSymptom.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if symptoms_on_day.count() > 0:
            df = pd.DataFrame(list(symptoms_on_day.values('symptom', 'symptom__name')))

            splits = dict(df.groupby('symptom__name').symptom.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_symptoms_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    symptoms = PatientSymptom.objects.filter(checkup__in=checkups)
    dataset_keys = {c.symptom.name for c in symptoms}

    for month in MONTH_CHOICES:
        queryset_on_month = checkups.filter(appointment__schedule_day__month=month[0])
        symptoms_on_month = PatientSymptom.objects.filter(checkup__in=queryset_on_month)
        labels.append(month[1])
        dataset = {}
        if symptoms_on_month.count() > 0:
            df = pd.DataFrame(list(symptoms_on_month.values('symptom', 'symptom__name')))
            splits = dict(df.groupby('symptom__name').symptom.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys


def patient_findings_counts(queryset):
    records = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    patient_findings = PatientFinding.objects.filter(checkup__in=records)
    total = patient_findings.count()

    aggregate = patient_findings.values('finding__name').annotate(scount=Count('finding')).order_by('finding__name')

    if total > 0:
        return {
            'items': list(
                aggregate.values(
                    'finding__name',
                    'scount'
                )
            ),
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_findings_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    findings = PatientFinding.objects.filter(checkup__in=checkups)
    dataset_keys = {c.finding.name for c in findings}

    for hour in labels:
        queryset_on_hour = PatientFinding.objects.filter(checkup__in=checkups.filter(appointment__time_start__hour=hour))

        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values('finding', 'finding__name')))

            splits = dict(df.groupby('finding__name').finding.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys


def patient_findings_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    findings = PatientFinding.objects.filter(checkup__in=checkups)
    dataset_keys = {c.finding.name for c in findings}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        findings_on_day = PatientFinding.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if findings_on_day.count() > 0:
            df = pd.DataFrame(list(findings_on_day.values('finding', 'finding__name')))

            splits = dict(df.groupby('finding__name').finding.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_findings_slice_by_week(queryset):
    days = queryset.first().schedule_day.get_week()

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    findings = PatientFinding.objects.filter(checkup__in=checkups)
    dataset_keys = {c.finding.name for c in findings}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        findings_on_day = PatientFinding.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if findings_on_day.count() > 0:
            df = pd.DataFrame(list(findings_on_day.values('finding', 'finding__name')))

            splits = dict(df.groupby('finding__name').finding.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_findings_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    findings = PatientFinding.objects.filter(checkup__in=checkups)
    dataset_keys = {c.finding.name for c in findings}

    for month in MONTH_CHOICES:
        queryset_on_month = checkups.filter(appointment__schedule_day__month=month[0])
        findings_on_month = PatientFinding.objects.filter(checkup__in=queryset_on_month)
        labels.append(month[1])
        dataset = {}
        if findings_on_month.count() > 0:
            df = pd.DataFrame(list(findings_on_month.values('finding', 'finding__name')))
            splits = dict(df.groupby('finding__name').finding.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys


def patient_diagnoses_counts(queryset):
    records = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    patient_diagnoses = PatientDiagnosis.objects.filter(checkup__in=records)
    total = patient_diagnoses.count()

    aggregate = patient_diagnoses.values('diagnosis__name').annotate(scount=Count('diagnosis')).order_by('diagnosis__name')

    if total > 0:
        return {
            'items': list(
                aggregate.values(
                    'diagnosis__name',
                    'scount'
                )
            ),
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_diagnoses_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    diagnoses = PatientDiagnosis.objects.filter(checkup__in=checkups)
    dataset_keys = {c.diagnosis.name for c in diagnoses}

    for hour in labels:
        queryset_on_hour = PatientDiagnosis.objects.filter(checkup__in=checkups.filter(appointment__time_start__hour=hour))

        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values('diagnosis', 'diagnosis__name')))

            splits = dict(df.groupby('diagnosis__name').diagnosis.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys


def patient_diagnoses_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    diagnoses = PatientDiagnosis.objects.filter(checkup__in=checkups)
    dataset_keys = {c.diagnosis.name for c in diagnoses}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        diagnoses_on_day = PatientDiagnosis.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if diagnoses_on_day.count() > 0:
            df = pd.DataFrame(list(diagnoses_on_day.values('diagnosis', 'diagnosis__name')))

            splits = dict(df.groupby('diagnosis__name').diagnosis.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_diagnoses_slice_by_week(queryset):
    days = queryset.first().schedule_day.get_week()

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    diagnoses = PatientDiagnosis.objects.filter(checkup__in=checkups)
    dataset_keys = {c.diagnosis.name for c in diagnoses}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        diagnoses_on_day = PatientDiagnosis.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if diagnoses_on_day.count() > 0:
            df = pd.DataFrame(list(diagnoses_on_day.values('diagnosis', 'diagnosis__name')))

            splits = dict(df.groupby('diagnosis__name').diagnosis.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_diagnoses_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    diagnoses = PatientDiagnosis.objects.filter(checkup__in=checkups)
    dataset_keys = {c.diagnosis.name for c in diagnoses}

    for month in MONTH_CHOICES:
        queryset_on_month = checkups.filter(appointment__schedule_day__month=month[0])
        diagnoses_on_month = PatientDiagnosis.objects.filter(checkup__in=queryset_on_month)
        labels.append(month[1])
        dataset = {}
        if diagnoses_on_month.count() > 0:
            df = pd.DataFrame(list(diagnoses_on_month.values('diagnosis', 'diagnosis__name')))
            splits = dict(df.groupby('diagnosis__name').diagnosis.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys


def patient_prescriptions_counts(queryset):
    records = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    patient_prescriptions = Prescription.objects.filter(checkup__in=records)
    total = patient_prescriptions.count()

    aggregate = patient_prescriptions.values('drug__name').annotate(scount=Count('drug')).order_by('drug__name')

    if total > 0:
        return {
            'items': list(
                aggregate.values(
                    'drug__name',
                    'scount'
                )
            ),
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_prescriptions_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    prescriptions = Prescription.objects.filter(checkup__in=checkups)
    dataset_keys = {c.drug.name for c in prescriptions}

    for hour in labels:
        queryset_on_hour = Prescription.objects.filter(checkup__in=checkups.filter(appointment__time_start__hour=hour))

        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values('drug', 'drug__name')))

            splits = dict(df.groupby('drug__name').drug.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys

def patient_prescriptions_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    prescriptions = Prescription.objects.filter(checkup__in=checkups)
    dataset_keys = {c.drug.name for c in prescriptions}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        prescriptions_on_day = Prescription.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if prescriptions_on_day.count() > 0:
            df = pd.DataFrame(list(prescriptions_on_day.values('drug', 'drug__name')))

            splits = dict(df.groupby('drug__name').drug__name.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_prescriptions_slice_by_week(queryset):
    days = queryset.first().schedule_day.get_week()

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    prescriptions = Prescription.objects.filter(checkup__in=checkups)
    dataset_keys = {c.drug.name for c in prescriptions}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        prescriptions_on_day = Prescription.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if prescriptions_on_day.count() > 0:
            df = pd.DataFrame(list(prescriptions_on_day.values('drug', 'drug__name')))

            splits = dict(df.groupby('drug__name').drug__name.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_prescriptions_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    prescriptions = Prescription.objects.filter(checkup__in=checkups)
    dataset_keys = {c.drug.name for c in prescriptions}

    for month in MONTH_CHOICES:
        queryset_on_month = checkups.filter(appointment__schedule_day__month=month[0])
        prescriptions_on_month = Prescription.objects.filter(checkup__in=queryset_on_month)
        labels.append(month[1])
        dataset = {}
        if prescriptions_on_month.count() > 0:
            df = pd.DataFrame(list(prescriptions_on_month.values('drug', 'drug__name')))
            splits = dict(df.groupby('drug__name').drug__name.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys


def patient_labtests_counts(queryset):
    records = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    patient_labtests = PatientLabTestRequest.objects.filter(checkup__in=records)
    total = patient_labtests.count()

    aggregate = patient_labtests.values('lab_test__name').annotate(scount=Count('lab_test')).order_by('lab_test__name')

    if total > 0:
        return {
            'items': list(
                aggregate.values(
                    'lab_test__name',
                    'scount'
                )
            ),
            'total': total
        }
    else:
        return {
            'items': [],
            'total': 0
        }


def patient_labtests_slice_by_day(queryset):
    labels = [hour for hour in range(0, 24)]
    day = queryset.first().schedule_day
    datasets = {}

    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    labtests = PatientLabTestRequest.objects.filter(checkup__in=checkups)
    dataset_keys = {c.lab_test.name for c in labtests}

    for hour in labels:
        queryset_on_hour = PatientLabTestRequest.objects.filter(checkup__in=checkups.filter(appointment__time_start__hour=hour))

        dataset = {}
        if queryset_on_hour.count() > 0:
            df = pd.DataFrame(list(queryset_on_hour.values('lab_test', 'lab_test__name')))

            splits = dict(df.groupby('lab_test__name').lab_test.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }

        datasets[str(hour)] = dataset

    return datasets, labels, dataset_keys

def patient_labtests_slice_by_month(queryset):
    month = queryset.first().schedule_day.month
    year = queryset.first().schedule_day.year

    days = DateDim.objects.days_in_month(month=month, year=year).order_by('day')

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    labtests = PatientLabTestRequest.objects.filter(checkup__in=checkups)
    dataset_keys = {c.lab_test.name for c in labtests}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        labtests_on_day = PatientLabTestRequest.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if labtests_on_day.count() > 0:
            df = pd.DataFrame(list(labtests_on_day.values('lab_test', 'lab_test__name')))

            splits = dict(df.groupby('lab_test__name').lab_test.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_labtests_slice_by_week(queryset):
    days = queryset.first().schedule_day.get_week()

    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    labtests = PatientLabTestRequest.objects.filter(checkup__in=checkups)
    dataset_keys = {c.lab_test.name for c in labtests}

    for day in days:
        labels.append(str(day))

        queryset_on_day = checkups.filter(appointment__schedule_day=day)
        labtests_on_day = PatientLabTestRequest.objects.filter(checkup__in=queryset_on_day)
        dataset = {}
        if labtests_on_day.count() > 0:
            df = pd.DataFrame(list(labtests_on_day.values('lab_test', 'lab_test__name')))

            splits = dict(df.groupby('lab_test__name').lab_test.count())

            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[str(day)] = dataset
    return datasets, labels, dataset_keys


def patient_labtests_slice_by_year(queryset):
    datasets = {}
    labels = []
    year = queryset.first().schedule_day.year
    labels = []
    datasets = {}
    checkups = PatientCheckupRecord.objects.filter(appointment__in=queryset)
    labtests = PatientLabTestRequest.objects.filter(checkup__in=checkups)
    dataset_keys = {c.lab_test.name for c in labtests}

    for month in MONTH_CHOICES:
        queryset_on_month = checkups.filter(appointment__schedule_day__month=month[0])
        labtests_on_month = PatientLabTestRequest.objects.filter(checkup__in=queryset_on_month)
        labels.append(month[1])
        dataset = {}
        if labtests_on_month.count() > 0:
            df = pd.DataFrame(list(labtests_on_month.values('lab_test', 'lab_test__name')))
            splits = dict(df.groupby('lab_test__name').lab_test.count())
            for dk in dataset_keys:
                if dk in splits:
                    dataset[dk] = {
                        'label': dk,
                        'count': splits[dk]
                    }
        else:
            for dk in dataset_keys:
                dataset[dk] = {
                    'label': dk,
                    'count': 0
                }
        datasets[month[1]] = dataset
    return datasets, labels, dataset_keys



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
