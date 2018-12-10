from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from receptionist_profiles.models import ReceptionistProfile


class ReceptionistProfileHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(ReceptionistProfile, user=request.user)
        context = {
            'page_title': 'Home',
            'location': 'receptionist_profile_home',
            'sublocation': 'home',
            'user': request.user,
            'profile': profile
        }

        return render(request, 'neo/receptionist_profiles/home/home.html', context)

    def test_func(self):
        return self.request.user.receptionist_profile()
