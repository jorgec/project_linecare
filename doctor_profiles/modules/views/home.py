from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class DoctorProfileHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Home',
            'location': 'doctor_profile_home',
            'sublocation': 'home',
            'user': request.user,
            'profile': request.user.doctor_profile()
        }

        return render(request, 'neo/doctor_profiles/home/home.html', context)

    def test_func(self):
        return self.request.user.doctor_profile()


class DoctorProfileCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.create_doctor_profile()
        return HttpResponseRedirect(reverse('doctor_profile_home'))
