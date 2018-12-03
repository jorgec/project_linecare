import operator
from django.db.models import Q
from functools import reduce

from django.contrib.postgres.fields import JSONField
from django.db import models as models

from doctor_profiles.models.managers.doctor_profile_manager import DoctorProfileManager


class DoctorProfile(models.Model):
    """
    The core Doctor profile
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    metadata = JSONField(default=dict, null=True, blank=True)

    """
    admin
    """
    is_approved = models.BooleanField(default=True)

    # Relationship Fields
    user = models.OneToOneField('accounts.Account', related_name='doctorprofile', on_delete=models.CASCADE, null=True)

    objects = DoctorProfileManager()

    class Meta:
        ordering = ('user',)

    def __str__(self):
        degrees = ", ".join([a.degree.abbreviation for a in self.get_degrees()])
        fellowships = ", ".join([a.get_abbreviation() for a in self.get_fellowships()])
        diplomates = ", ".join([a.get_abbreviation() for a in self.get_diplomates()])

        title = f"Dr. {self.user.base_profile().get_name()} {degrees} {fellowships} {diplomates}"

        return title

    def get_degrees(self):
        return self.doctor_degrees.filter(degree__is_approved=True)

    def get_insurance_providers(self):
        return self.doctor_insurance.filter(is_approved=True)

    def get_specializations(self):
        return self.doctor_specializations.filter(specialization__parent__isnull=True, specialization__is_approved=True)

    def get_associations(self):
        return self.doctor_associations.filter(association__is_approved=True)

    def get_fellowships(self):
        return self.doctor_associations.filter(level='Fellow', association__is_approved=True)

    def get_diplomates(self):
        return self.doctor_associations.filter(level='Diplomate', association__is_approved=True)

    def get_medical_institutions(self):
        return self.medical_institutions_joined.filter(is_approved=True)

    def get_receptionists(self, *, medical_institution=None, s=None):

        filters = {
            'is_approved': True
        }

        if medical_institution:
            filters['medical_institution'] = medical_institution

        connections = self.doctor_connections.filter(**filters).order_by('receptionist__user__account_profiles__last_name')

        search_filters = {}
        if s:
            search_filters['receptionist__user__account_profiles__last_name__icontains'] = s
            search_filters['receptionist__user__account_profiles__first_name__icontains'] = s
            search_filters['receptionist__user__username__icontains'] = s
            search_filters['receptionist__user__email__icontains'] = s
            connections = connections.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in search_filters.items()])))


        return {r.receptionist for r in connections}

    def get_unconnected_receptionists(self, *, medical_institution):
        pass

    def get_profile_progress_metadata(self):
        return self.metadata.get('doctor_progress')

    def dismiss_profile_progress_display(self):
        if self.get_profile_progress_metadata():
            print(self.get_profile_progress_metadata())
            self.metadata['doctor_progress']['show'] = False
            self.save()
            print(self.get_profile_progress_metadata())
            return True
        return False

    def display_profile_progress_status(self):
        try:
            return self.metadata['doctor_progress']['show']
        except KeyError:
            self.initialize_progress_metadata()
            return self.metadata['doctor_progress']['show']

    def initialize_progress_metadata(self):
        self.metadata = {
            'doctor_progress': {
                'show': True,
                'data': {
                    'medical_degree': self.doctor_degrees.count(),
                    'insurance': self.doctor_insurance.count(),
                    'specialization': self.doctor_specializations.count(),
                    'association': self.doctor_associations.count(),
                    'institution': None
                }
            }
        }
        self.save()
        return self.metadata.get('doctor_progress')

    def calculate_settings_progress(self):
        progress = self.initialize_progress_metadata()
        retval = {
            'progress': 0.0,
            'progress_pct': '0%',
            'progress_int': 0,
            'items': {}
        }
        if progress:
            max = len(progress['data'])
            total = 0
            for key, value in progress['data'].items():
                if value is not None:
                    if type(value) == int:
                        if value > 0:
                            total = total + 1
            retval['progress'] = total / max
            retval['progress_pct'] = f'{round((total/max)*100)}%'
            retval['progress_int'] = round((total / max) * 100)
            retval['items'] = progress
        return retval

    def settings_progress(self):
        return self.calculate_settings_progress()
