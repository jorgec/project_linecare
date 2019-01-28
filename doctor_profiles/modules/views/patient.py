from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from doctor_profiles.models import PatientAppointment, PatientCheckupRecord, PatientConnection, \
    PatientCheckupRecordAccess, PatientSymptom, PatientFinding, DoctorProfile
from profiles.models import BaseProfile


class DoctorProfilePatientList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        context = {
            'page_title': f'Patients list for {doctor}',
            'location': 'doctor_profile_patients',
            'sublocation': 'list',
            'doctor': doctor,
        }

        return render(request, 'neo/doctor_profiles/patient/home.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfilePatientDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        patient = get_object_or_404(BaseProfile, id=kwargs['patient_id'])
        if request.user.doctor_profile():
            doctor = request.user.doctor_profile()
            connection = get_object_or_404(PatientConnection, doctor=doctor, patient=patient)

            checkups = PatientCheckupRecordAccess.objects.filter(
                doctor=doctor,
                checkup__appointment__patient=patient,
                is_approved=True
            ).order_by(
                '-checkup__appointment__schedule_day__date_obj'
            )

            context = {
                'page_title': f'Patient profile for {patient}',
                'location': 'doctor_profile_patients',
                'sublocation': 'detail_home',
                'doctor': doctor,
                'patient': patient,
                'checkups': checkups
            }

            return render(request, 'neo/doctor_profiles/patient/patient_detail.html', context)
        elif request.user.receptionist_profile():
            return HttpResponseRedirect(reverse(
                'receptionist_profile_patient_detail',
                kwargs={
                    'patient_id': patient.id
                }
            ))

        else:
            pass

    def test_func(self):
        return self.request.user.doctor_profile() or self.request.user.receptionist_profile()

class DoctorProfilePatientQSDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('doctor_profile_patient_detail', kwargs={'patient_id': request.GET.get('patient_id', None)}))


class DoctorProfilePatientAppointmentDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment', None))

        if appointment.status == 'done':
            return HttpResponseRedirect(
                f"{reverse('doctor_profile_patient_appointment_history_detail')}?appointment={appointment.id}"
            )

        checkup = appointment.appointment_checkup

        if not checkup.doctor_has_access(doctor):
            return HttpResponseRedirect('/403/Forbidden')

        context = {
            'page_title': f'Appointment for {appointment.patient} on {appointment.schedule_day.nice_name} at {appointment.medical_institution}',
            'location': 'doctor_profile_patients',
            'sublocation': 'detail',
            'doctor': doctor,
            'patient': appointment.patient,
            'appointment': appointment,
            'checkup': checkup
        }

        return render(request, 'neo/doctor_profiles/patient/appointment_detail.html', context)

    def post(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment', None))
        checkup = appointment.appointment_checkup

        if not checkup.doctor_has_access(doctor):
            return HttpResponseRedirect('/403/Forbidden')

        appointment.status = 'done'
        appointment.save()

        return_url = reverse('doctor_profile_schedule_detail', kwargs={'medical_institution': appointment.medical_institution.slug})

        return HttpResponseRedirect(
            f'{return_url}?date={str(appointment.schedule_day)}'
        )

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfilePatientAppointmentHistoryDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        appointment = get_object_or_404(PatientAppointment, id=request.GET.get('appointment', None))
        checkup = appointment.appointment_checkup

        if not checkup.doctor_has_access(doctor):
            return HttpResponseRedirect('/403/Forbidden')

        context = {
            'page_title': f'Appointment for {appointment.patient} on {appointment.schedule_day.nice_name()} at {appointment.medical_institution}',
            'location': 'doctor_profile_patients',
            'sublocation': 'detail',
            'doctor': doctor,
            'patient': appointment.patient,
            'appointment': appointment,
            'checkup': checkup
        }

        return render(request, 'neo/doctor_profiles/patient/appointment_history_detail.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfilePatientSymptomsFindingsList(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        doctor = request.user.doctor_profile()
        patient = get_object_or_404(BaseProfile, id=kwargs['patient_id'])
        connection = get_object_or_404(PatientConnection, doctor=doctor, patient=patient)

        symptoms = PatientSymptom.objects.filter(
            doctor=doctor,
            patient=patient
        )

        findings = PatientFinding.objects.filter(
            doctor=doctor,
            patient=patient
        )

        context = {
            'page_title': f'Symptoms and Findings for {patient}',
            'location': 'doctor_profile_patients',
            'sublocation': 'findings_symptoms',
            'doctor': doctor,
            'patient': patient,
            'symptoms': symptoms,
            'findings': findings
        }

        return render(request, 'neo/doctor_profiles/patient/patient_detail.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()
