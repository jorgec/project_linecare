from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View


class DoctorProfileCareerSettingsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Career Settings',
            'location': 'doctor_profile_career',
            'sublocation': 'degree',

        }

    def test_func(self):
        return self.request.user.doctor_profile()
