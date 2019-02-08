from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from datesdim.models import DateDim
from doctor_profiles.models import PatientAppointment, DoctorProfile, MedicalInstitution, MedicalInstitutionDoctor
from doctor_profiles.modules.api.doctor_schedule_api import is_doctor_or_receptionist
from doctor_profiles.serializers import PatientQueuePrivateSerializer

UPDATE_STATUS_PERMISSIONS_MATRIX = {
    'doctor': [
        'pending',
        'queueing',
        'in_progress',
        'finishing',
        'done',
        'cancelled_by_doctor',
        'rescheduled_by_doctor',
    ],
    'receptionist': [
        'pending',
        'queueing',
        'in_progress',
        'finishing',
        'cancelled_by_doctor',
        'rescheduled_by_doctor',
    ],
    'patient': [
        'pending',
        'queueing',
        'cancelled_by_patient',
        'rescheduled_by_patient'
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


class ApiPatientAppointmentCount(APIView):
	"""
	Count the number of appointments for specified date

	[optional]
	?date=YYYY-MM-DD
	?medical_institution_id=n
	"""

	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, *args, **kwargs):
		doctor = request.user.doctor_profile()
		if not doctor:
			return Response("Invalid user profile", status=status.HTTP_403_FORBIDDEN)

		date = None
		medical_institution = None

		if request.GET.get('date'):
			date = DateDim.objects.parse_get(request.GET.get('date'))
		if not date:
			date = DateDim.objects.today()

		if request.GET.get('medical_institution_id', None):
			medical_institution = get_object_or_404(MedicalInstitution.objects.get(id=request.GET.get('medical_institution_id')))

		appointments = doctor.get_patient_appointments(
			day_start=date,
			day_end=date,
			medical_institution=medical_institution
		)
		# serializer = PatientQueuePrivateSerializer(appointments, many=True)

		return Response(appointments.count(), status=status.HTTP_200_OK)


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
    - cancelled_by_patient: Cancelled by patient: patient
    - cancelled_by_doctor: Cancelled by doctor: doctor, receptionist
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

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=request.GET.get('doctor_id', None))

        access, profile_type = is_doctor_or_receptionist(request.user)
        if not access:
            return Response("Invalid account", status=status.HTTP_401_UNAUTHORIZED)

        if type(profile_type) != DoctorProfile:
            """ person accessing isn't the doctor, so check if receptionist is allowed """
            connection = doctor.verify_receptionist(receptionist=request.user.receptionistprofile)
            if not connection:
                return Response("Receptionist is not authorized by this doctor for this medical institution",
                                status=status.HTTP_403_FORBIDDEN)
        elif profile_type.id != doctor.id:
            return Response("This is not your schedule", status=status.HTTP_401_UNAUTHORIZED)

        medical_institution_id = request.GET.get('medical_institution', None)
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

        page = int(request.GET.get('page', 1))
        grab = int(request.GET.get('grab', 50))

        appointments = doctor.get_patient_appointments(
            medical_institution=medical_institution,
            s=s,
            day_start=day_start,
            day_end=day_end,
            status=appointment_status,
            appointment_type=appointment_type,
            page=page,
            grab=grab
        )

        serializer = PatientQueuePrivateSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
