import operator
from django.apps import apps
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
        degrees = ", ".join([a.degree.abbreviation for a in self.get_degrees_rel()])
        fellowships = ", ".join([a.get_abbreviation() for a in self.get_fellowships_rel()])
        diplomates = ", ".join([a.get_abbreviation() for a in self.get_diplomates_rel()])

        title = f"Dr. {self.user.base_profile().get_name()} {degrees} {fellowships} {diplomates}"

        return title

    def get_degrees_rel(self):
        return self.doctor_degrees.filter(degree__is_approved=True)

    def get_degrees(self):
        rel = self.get_degrees_rel()
        return [d.degree for d in rel]

    def get_insurance_providers_rel(self):
        return self.doctor_insurance.filter(is_approved=True)

    def get_insurance_providers(self):
        return [ip.insurance for ip in self.get_insurance_providers_rel()]

    def get_specializations_rel(self):
        return self.doctor_specializations.filter(specialization__parent__isnull=True, specialization__is_approved=True)

    def get_specializations(self):
        return [s.specialization for s in self.get_specializations_rel()]

    def get_associations_rel(self):
        return self.doctor_associations.filter(association__is_approved=True)

    def get_associations(self):
        return [a.association for a in self.get_associations_rel()]

    def get_fellowships_rel(self):
        return self.doctor_associations.filter(level='Fellow', association__is_approved=True)

    def get_fellowships(self):
        return [a.association for a in self.get_fellowships_rel()]

    def get_diplomates_rel(self):
        return self.doctor_associations.filter(level='Diplomate', association__is_approved=True)

    def get_diplomates(self):
        return [a.association for a in self.get_diplomates_rel()]

    def get_medical_institutions_rel(self):
        return self.medical_institutions_joined.filter(is_approved=True)

    def get_medical_institutions(self):
        return [mi.medical_institution for mi in self.get_medical_institutions_rel()]

    def verify_receptionist(self, *, receptionist, medical_institution=None):
        filters = {
            'is_approved': True,
            'receptionist': receptionist
        }
        if medical_institution:
            filters['medical_institution'] = medical_institution

        try:
            connection = self.doctor_connections.get(**filters)
            return connection
        except self.doctor_connections.DoesNotExist:
            return False

    def get_receptionists(self, *, medical_institution=None, s=None):

        filters = {
            'is_approved': True
        }

        if medical_institution:
            filters['medical_institution'] = medical_institution

        connections = self.doctor_connections.filter(**filters).order_by(
            'receptionist__user__account_profiles__last_name')

        search_filters = {}
        if s:
            search_filters['receptionist__user__account_profiles__last_name__icontains'] = s
            search_filters['receptionist__user__account_profiles__first_name__icontains'] = s
            search_filters['receptionist__user__username__icontains'] = s
            search_filters['receptionist__user__email__icontains'] = s
            connections = connections.filter(
                reduce(operator.or_, (Q(**d) for d in [dict([i]) for i in search_filters.items()])))

        return {r.receptionist for r in connections}

    def get_unconnected_receptionists(self, *, medical_institution):
        pass

    def get_profile_progress_metadata(self):
        return self.metadata.get('doctor_progress')

    def dismiss_profile_progress_display(self):
        if self.get_profile_progress_metadata():
            self.metadata['doctor_progress']['show'] = False
            self.save()
            return True
        return False

    def display_profile_progress_status(self):
        try:
            progress = self.metadata['doctor_progress']
        except KeyError:
            self.initialize_progress_metadata()
            progress = self.metadata['doctor_progress']
        try:
            return progress['show']
        except KeyError:
            self.initialize_progress_metadata()
            return progress['show']

    def initialize_progress_metadata(self):

        self.metadata['doctor_progress'] = {
            'show': True,
            'data': {
                'medical_degree': self.doctor_degrees.count(),
                'insurance': self.doctor_insurance.count(),
                'specialization': self.doctor_specializations.count(),
                'association': self.doctor_associations.count(),
                'institution': self.medical_institutions_joined.count()
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

    def get_schedules(self, *, medical_institution=None, include_past=False):
        DateDim = apps.get_model('datesdim.DateDim')
        filters = {
            'is_approved': True
        }
        if medical_institution:
            filters['medical_institution'] = medical_institution

        if include_past:
            return self.doctor_schedules.filter(**filters)
        else:
            return self.doctor_schedules.filter(**filters).filter(
                end_date__date_obj__gte=DateDim.objects.today().date_obj
            )

    def get_schedule_days(self, *, medical_institution=None):
        filters = {}
        if medical_institution:
            filters['medical_institution'] = medical_institution

        return self.doctor_schedule_days.filter(**filters)

    def initialize_options(self):
        self.metadata['options'] = {
            'schedule_options': {
                'checkup_duration': 60,
                'checkup_gap': 15,
                'followup_duration': 30,
                'followup_gap': 5,
                'lab_result_duration': 15,
                'lab_result_gap': 5
            }
        }
        self.save()
        return self.metadata['options']

    def get_options(self, key=None):
        try:
            options = self.metadata['options']
        except KeyError:
            options = self.initialize_options()

        if key:
            try:
                return options[key]
            except KeyError:
                self.metadata['options'][key] = None
                self.save()
                return options[key]
        return options

    def set_option(self, key, value):
        self.metadata['options'][key] = value
        self.save()
        return value
