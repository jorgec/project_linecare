import arrow
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class DoctorScheduleCalendarView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        now = arrow.utcnow.to(settings.TIME_ZONE)
        year = request.GET.get('year', now.year)
        month = request.GET.get('month', now.month)