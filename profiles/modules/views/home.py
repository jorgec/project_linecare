from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class BaseProfileHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()

        context = {
            'page_title': profile,
            'location': 'profile_home',
            'sublocation': 'home',
            'profile': profile
        }

        return render(request, 'neo/profile/home/home.html', context)
