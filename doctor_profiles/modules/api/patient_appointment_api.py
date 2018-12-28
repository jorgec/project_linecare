from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.constants import QUEUE_STATUS_MESSAGES
from doctor_profiles.models import PatientAppointment
from doctor_profiles.modules.notifiers.doctor_appointment_notifiers import doctor_notify_update_queue
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

    if queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['doctor']:
        if actor.doctor_profile() and appointment.doctor == actor.doctor_profile():
            is_allowed = True
    elif queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['receptionist']:
        if actor.receptionist_profile() and actor.receptionist_profile() in appointment.doctor.get_receptionists(
                medical_institution=appointment.medical_institution):
            is_alllowed = True
    elif queue_status in UPDATE_STATUS_PERMISSIONS_MATRIX['patient']:
        if actor.base_profile() == appointment.patient:
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

        doctor_notify_update_queue(appointment.doctor)

        return Response(f"Status of {appointment} changed to {queue_status}", status=status.HTTP_200_OK)
