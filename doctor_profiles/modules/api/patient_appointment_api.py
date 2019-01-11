from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import DateDim
from doctor_profiles.constants import QUEUE_STATUS_MESSAGES
from doctor_profiles.models import PatientAppointment, DoctorProfile, MedicalInstitution, MedicalInstitutionDoctor
from doctor_profiles.modules.notifiers.doctor_appointment_notifiers import doctor_notify_update_queue
from doctor_profiles.serializers import PatientQueuePrivateSerializer
from profiles.notifiers.patient_appointment_notifiers import patient_appointment_status_notify

UPDATE_STATUS_PERMISSIONS_MATRIX = {
    'doctor': [
        'pending',
        'queueing',
        'in_progress',
        'finishing',
        'done',
        'doctor_cancel',
        'doctor_resched',
    ],
    'receptionist': [
        'pending',
        'queueing',
        'in_progress',
        'finishing',
        'doctor_cancel',
        'doctor_resched',
    ],
    'patient': [
        'pending',
        'queueing',
        'patient_cancel',
        'patient_resched'
    ]
}


def update_status_permissions_check(appointment, request, queue_status):
    is_allowed = False
    actor = request.user

    if actor.doctor_profile() and appointment.doctor == actor.doctor_profile():
        if queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['doctor']:
            is_allowed = True
    if actor.receptionist_profile() and actor.receptionist_profile() in appointment.doctor.get_receptionists(
            medical_institution=appointment.medical_institution):
        if queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['receptionist']:
            is_allowed = True
    if actor.base_profile() == appointment.patient:
        if queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['patient']:
            is_allowed = True

    return is_allowed


class ApiPatientAppointmentUpdateStatus(APIView):
    """
    Update status of patient appointment
    ?appointment_id=appointment_id&queue_status=str

    status codes:
    - pending: Pending: default
    - queueing: Queueing: doctor, receptionist, patient
    - in_progress: In Progress: doctor, receptionist
    - finishing: Finishing: doctor
    - done: Done: doctor, receptionist
    - patient_cancel: Cancelled by patient: patient
    - doctor_cancel: Cancelled by doctor: doctor, receptionist
    - patient_resched: Rescheduled by patient: patient
    - doctor_resched: Rescheduled by doctor: doctor, receptionist
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment_id', None))
        queue_status = request.GET.get('queue_status', None)
        if not queue_status:
            return Response("Status parameter is required", status=status.HTTP_400_BAD_REQUEST)

        if not update_status_permissions_check(appointment, request, queue_status):
            return Response(f"You are not allowed to perform this action: {queue_status}",
                            status=status.HTTP_403_FORBIDDEN)

        PatientAppointment.objects.update_status(id=appointment.id, status=queue_status)

        # doctor_notify_update_queue(appointment.doctor)

        return Response(f"Status of {appointment} changed to {queue_status}", status=status.HTTP_200_OK)


class ApiPatientAppointmentList(APIView):
    """
    Get list of appointments by doctor
    ?doctor_id=id
    [optional]
    medical_institution_id=id
    day_start=str('YYYY-MM-DD')
    day_end=str('YYYY-MM-DD')
    appointment_status=str
    appointment_type=str
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))

        medical_institution_id = request.GET.get('medical_institution_id', None)
        if medical_institution_id:
            medical_institution = get_object_or_404(MedicalInstitution, id=medical_institution_id)
            connection = get_object_or_404(MedicalInstitutionDoctor, is_approved=True, doctor=doctor,
                                           medical_institution=medical_institution)

            """
            TODO:
            
            Receptionist check
            """
        else:
            medical_institution = None

        day_start_str = request.GET.get('day_start', None)
        if day_start_str:
            day_start = DateDim.objects.parse_get(day_start_str)
            if not day_start:
                day_start = None
        else:
            day_start = None

        day_end_str = request.GET.get('day_end', None)
        if day_end_str:
            day_end = DateDim.objects.parse_get(day_end_str)
            if not day_end:
                day_end = None
        else:
            day_end = None
        appointment_status = request.GET.get('appointment_status', None)
        appointment_type = request.GET.get('appointment_type', None)
        s = request.GET.get('s', None)

        params = {
            'medical_institution': medical_institution,
            's': s,
            'day_start': day_start,
            'day_end': day_end,
            'status': appointment_status,
            'appointment_type': appointment_type,
            'page': 1,
            'grab': 50
        }

        print(params)

        appointments = doctor.get_patient_appointments(
            **params
        )

        serializer = PatientQueuePrivateSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
