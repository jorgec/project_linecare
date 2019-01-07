from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.analytics import patient_analytics
from doctor_profiles.analytics.patient_analytics import patient_appointment_earnings, \
    patient_appointment_slice_by_month, \
    patient_appointment_checkup_counts, patient_appointment_slice_by_year, patient_appointment_slice_by_week, \
    patient_appointment_slice_by_day, patient_symptoms_counts, patient_symptoms_slice_by_month, \
    patient_symptoms_slice_by_year, patient_symptoms_slice_by_week
from doctor_profiles.models import DoctorProfile, PatientAppointment
from receptionist_profiles.models import ReceptionistProfile


def is_doctor_or_receptionist(user):
    user_type = None
    try:
        doctor = DoctorProfile.objects.get(user=user)
        user_type = doctor
    except DoctorProfile.DoesNotExist:
        try:
            receptionist = ReceptionistProfile.objects.get(user=user)
            user_type = receptionist
        except ReceptionistProfile.DoesNotExist:
            return False, user_type
    return True, user_type


def has_access(request, person):
    """
    TODO:
    FIX THIS SUPERMASSIVE SECURITY HOLE
    """

    # return request.GET.get('doctor_id') == person.id
    return True


class ApiAnalyticsPatientByCheckupAggregateCounts(APIView):
    """

    :param doctor_id
    :type int

    :param slice
    :type str ("day", "week", "month", "year")

    :param day
    :type yyyy-mm-dd

    [ optional ]
    :param medical_institution_id
    :type int


    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        if not has_access(request, profile_type):
            return Response("You do not have access to this data", status=status.HTTP_403_FORBIDDEN)

        """
        params
        """
        params = {
            'doctor_id': request.GET.get('doctor_id'),
            'slice': request.GET.get('slice', 'month'),
            'day': request.GET.get('day', None),
            'medical_institution_id': request.GET.get('medical_institution_id', None),
        }
        time_slice = request.GET.get('slice', 'month')
        """
        /params
        """

        filters = patient_analytics.patient_appointment_build_filters(params)

        serialized = {
            'counts': {
                'data': {
                    'items': [],
                    'total': 0
                },
                'label': 'Appointments',
                'key': 'counts'
            },
            'earnings': {
                'data': {
                    'fees': {},
                    'total': 0
                },
                'label': 'Earnings',
                'key': 'earnings'
            },
            'slice': [],
            'labels': [],
            'dataset_keys': []
        }

        if filters:
            checkups = PatientAppointment.objects.filter(
                **filters
            )

            if checkups.count() > 0:
                checkup_earnings = patient_appointment_earnings(checkups)
                checkup_counts = patient_appointment_checkup_counts(checkups)


                if time_slice == 'month':
                    sliced_data, labels, dataset_keys = patient_appointment_slice_by_month(checkups)
                elif time_slice == 'year':
                    sliced_data, labels, dataset_keys = patient_appointment_slice_by_year(checkups)
                elif time_slice == 'week':
                    sliced_data, labels, dataset_keys = patient_appointment_slice_by_week(checkups)
                elif time_slice == 'day':
                    sliced_data, labels, dataset_keys = patient_appointment_slice_by_day(checkups)
                else:
                    sliced_data, labels, dataset_keys = patient_appointment_slice_by_month(checkups)

                serialized = {
                    'counts': {
                        'data': checkup_counts,
                        'label': 'Appointments',
                        'key': 'counts'
                    },
                    'earnings': {
                        'data': checkup_earnings,
                        'label': 'Earnings',
                        'key': 'earnings'
                    },
                    'slice': sliced_data,
                    'labels': labels,
                    'dataset_keys': dataset_keys
                }

                return Response(serialized, status=status.HTTP_200_OK)
            return Response(serialized, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class ApiAnalyticsPatientByCheckupSymptomsAggregateCounts(APIView):
    """

    :param doctor_id
    :type int

    :param slice
    :type str ("day", "week", "month", "year")

    :param day
    :type yyyy-mm-dd

    [ optional ]
    :param medical_institution_id
    :type int


    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        result, profile_type = is_doctor_or_receptionist(request.user)
        if not result:
            return Response("Incompatible user profile", status=status.HTTP_403_FORBIDDEN)

        if not has_access(request, profile_type):
            return Response("You do not have access to this data", status=status.HTTP_403_FORBIDDEN)

        """
        params
        """
        params = {
            'doctor_id': request.GET.get('doctor_id'),
            'slice': request.GET.get('slice', 'month'),
            'day': request.GET.get('day', None),
        }
        if request.GET.get('medical_institution_id', None):
            params['medical_institution_id'] = request.GET.get('medical_institution_id', None)
        time_slice = request.GET.get('slice', 'month')
        """
        /params
        """
        filters = patient_analytics.patient_appointment_build_filters(params)

        serialized = {}
        if filters:
            checkups = PatientAppointment.objects.filter(
                **filters
            )

            if checkups.count() > 0:

                if time_slice == 'month':
                    sliced_data, labels, dataset_keys = patient_symptoms_slice_by_month(checkups)
                elif time_slice == 'year':
                    sliced_data, labels, dataset_keys = patient_symptoms_slice_by_year(checkups)
                elif time_slice == 'week':
                    sliced_data, labels, dataset_keys = patient_symptoms_slice_by_week(checkups)
                else:
                    sliced_data, labels, dataset_keys = patient_symptoms_slice_by_month(checkups)

                symptom_counts = patient_symptoms_counts(checkups)
                serialized = {
                    'counts': {
                        'data': symptom_counts,
                        'label': 'Symptoms',
                        'key': 'counts'
                    },
                    'slice': sliced_data,
                    'labels': labels,
                    'dataset_keys': dataset_keys
                }


                return Response(serialized, status=status.HTTP_200_OK)
            return Response(serialized, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
