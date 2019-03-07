from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.views import View

from doctor_profiles.models import PatientCheckupRecordAccess
from profiles.models import BaseProfile


class ReceptionistProfilePatientDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        patient = get_object_or_404(BaseProfile, id=kwargs['patient_id'])
        receptionist = request.user.receptionist_profile()
        doctors = [c.doctor for c in receptionist.get_doctor_connections()]

        checkups = PatientCheckupRecordAccess.objects.filter(
            doctor__in=doctors,
            checkup__appointment__patient=patient,
            is_approved=True
        ).order_by(
            '-checkup__appointment__schedule_day__date_obj'
        )

        context = {
            'page_title': f'Patient profile for {patient}',
            'location': 'doctor_profile_patients',
            'sublocation': 'detail_home',
            'patient': patient,
            'checkups': checkups
        }

        return render(request, 'neo/receptionist_profiles/patient/patient_detail.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()