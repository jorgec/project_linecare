from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class DoctorProfileProgressSnippet(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.doctorprofile.get_profile_progress_metadata():
            request.user.doctorprofile.initialize_progress_metadata()
        return render(request, 'neo/doctor_profiles/common/snippets/profile_progress.html')


class DoctorProfileProgressDetailSnippet(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'neo/doctor_profiles/common/snippets/profile_progress_detail.html')
