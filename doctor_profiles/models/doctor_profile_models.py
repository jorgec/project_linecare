import operator
from django.apps import apps
from django.contrib.postgres.fields import JSONField
from django.db import models as models, IntegrityError
from django.db.models import Q
from functools import reduce

from doctor_profiles.constants import QUEUE_NOT_CANCELLED_CODES, QUESTIONNAIRE_RESTRICTION_CHOICES
from doctor_profiles.models.managers.doctor_profile_manager import DoctorProfileManager
from helpers import search


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
        degrees, fellowships, diplomates = self.get_name_suffixes()

        try:
            title = f"{self.user.base_profile().get_name()} {degrees} {fellowships} {diplomates}"
        except AttributeError:
            return 'NoBaseProfile'

        return title

    def name_only(self):
        return self.user.base_profile().get_name()

    def get_name_suffixes(self):
        degrees = ", ".join([a.degree.abbreviation for a in self.get_degrees_rel()])
        fellowships = ", ".join([a.get_abbreviation() for a in self.get_fellowships_rel()])
        diplomates = ", ".join([a.get_abbreviation() for a in self.get_diplomates_rel()])

        return degrees, fellowships, diplomates

    def repr_name_suffixes(self):
        degrees, fellowships, diplomates = self.get_name_suffixes()
        title = f"{degrees} {fellowships} {diplomates}"
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

    def repr_specializations(self):
        specializations = self.get_specializations_rel()
        html = ''
        for s in specializations:
            html += f'{s.specialization.name} ({s.year_attained})<br><small>{s.place_of_residency}</small><hr>'
        return html

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
        return {mi.medical_institution for mi in self.get_medical_institutions_rel()}

    def verify_medical_institution_membership(self, medical_institution):
        try:
            return self.medical_institutions_joined.get(medical_institution=medical_institution)
        except:
            return False

    def verify_receptionist(self, *, receptionist, medical_institution=None):
        filters = {
            'is_approved': True,
            'receptionist': receptionist
        }
        if medical_institution:
            filters['medical_institution'] = medical_institution

        connection = self.doctor_connections.filter(**filters)
        if connection.count() > 0:
            return connection.first()
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
            retval['progress_pct'] = f'{round((total / max) * 100)}%'
            retval['progress_int'] = round((total / max) * 100)
            retval['items'] = progress
        return retval

    def settings_progress(self):
        return self.calculate_settings_progress()

    def get_schedules(self, *, medical_institution=None, include_past=True, filter_days=None, day=None):
        DateDim = apps.get_model('datesdim.DateDim')
        filters = {
            'is_approved': True
        }
        if medical_institution:
            filters['medical_institution'] = medical_institution

        if filter_days:
            filters['days__contains'] = filter_days

        if include_past:
            return self.doctor_schedules.filter(**filters)
        else:
            return self.doctor_schedules.filter(**filters).filter(
                end_date__date_obj__gte=DateDim.objects.today().date_obj
            )

    def get_active_schedules(self, medical_institution=None, filter_days=None):
        return self.get_schedules(medical_institution=medical_institution, include_past=False, filter_days=None)

    def get_schedule_days_for_month(self, *, year=None, month=None, medical_institution=None):
        DateDim = apps.get_model('datesdim.DateDim')
        if not year or not month:
            today = DateDim.objects.today()
            year = today.year
            month = today.month

        schedule_days = self.get_schedule_days(medical_institution=medical_institution)
        return schedule_days.filter(
            day__month=month,
            day__year=year
        )

    def get_schedule_days(self, *, medical_institution=None):
        filters = {}
        if medical_institution:
            filters['medical_institution'] = medical_institution

        return self.doctor_schedule_days.filter(**filters)

    def get_schedule_on_day(self, *, day=None, medical_institution=None, schedule_id=None):
        DateDim = apps.get_model('datesdim.DateDim')
        if not day:
            day = DateDim.objects.today()

        filters = {
            'day': day
        }
        if schedule_id:
            filters['schedule__id'] = schedule_id
        else:
            if medical_institution:
                filters['medical_institution'] = medical_institution

        return self.doctor_schedule_days.filter(**filters)

    def appointment_notifications(self):
        try:
            return self.metadata['notifiers']
        except KeyError:
            self.metadata['notifiers'] = []
            return []

    def update_appointment_notifications(self, data):
        notifs = self.appointment_notifications()
        notifs.append(data)
        notifs.reverse()
        self.metadata['notifiers'] = notifs
        self.save(update_fields=['metadata'])
        return self.appointment_notifications()

    def clear_appointment_notifications(self):
        self.metadata['notifiers'] = []
        self.save(update_fields=['metadata'])
        return []

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

    def get_medical_institution_meta(self, medical_institution):
        MedicalInstitutionDoctor = apps.get_model('doctor_profiles.MedicalInstitutionDoctor')
        try:
            connection = MedicalInstitutionDoctor.objects.get(
                is_approved=True,
                doctor=self,
                medical_institution=medical_institution
            )
            return connection.metadata
        except MedicalInstitutionDoctor.DoesNotExist:
            return []

    def get_patients(self, s=None):
        if s:
            patients_query = search.get_query(s, ['patient__first_name', 'patient__last_name'])
            return self.doctor_patients.filter(patients_query).order_by('patient__last_name')
        return self.doctor_patients.all()

    def find_earliest_active_schedule(self, exclude_day=None, grab=1):
        DateDim = apps.get_model('datesdim.DateDim')
        TimeDim = apps.get_model('datesdim.TimeDim')

        if exclude_day:
            today = exclude_day
        else:
            today = DateDim.objects.today()

        earliest_day = self.doctor_schedule_days.filter(
            day__date_obj__gte=today.date_obj
        ).order_by('day__date_obj', '-schedule__start_time__minutes_since')

        if earliest_day.count() > 0:
            return earliest_day[:grab]
        return None

    def create_appointment(
            self, *,
            patient,
            appointment_type='checkup',
            earliest_available=True,
            **kwargs
    ):
        PatientAppointment = apps.get_model('doctor_profiles.PatientAppointment')
        if earliest_available:
            schedule_day = self.find_earliest_active_schedule()
            if schedule_day:
                create_result, appointment, create_status = PatientAppointment.objects.create(
                    doctor_id=self.id,
                    patient_id=patient.id,
                    schedule_choice='first_available',
                    preferred_day=str(schedule_day[0].day),
                    medical_institution_id=schedule_day[0].medical_institution.id,
                    appointment_type=appointment_type
                )

                if create_result:
                    return appointment

                while not create_result:
                    schedule_day = self.find_earliest_active_schedule(exclude_day=schedule_day[0].day)
                    if schedule_day:
                        create_result, appointment, create_status = PatientAppointment.objects.create(
                            doctor_id=self.id,
                            patient_id=patient.id,
                            schedule_choice='first_available',
                            preferred_day=str(schedule_day.day),
                            medical_institution_id=schedule_day[0].medical_institution.id,
                            appointment_type=appointment_type
                        )
                        if create_result:
                            return appointment
                return False
            else:
                return False
        else:
            pass

    def get_patient_appointments(
            self, *,
            medical_institution=None,
            schedule_id=None,
            s=None,
            day_start=None,
            day_end=None,
            status=None,
            appointment_type=None,
            page=1,
            grab=50,
            show_cancelled=True,
            patient_id=None
    ):
        filters = {}

        if medical_institution:
            filters['medical_institution'] = medical_institution
        if day_start:
            filters['schedule_day__date_obj__gte'] = day_start.date_obj
        if day_end:
            filters['schedule_day__date_obj__lte'] = day_end.date_obj
        if status:
            filters['status'] = status
        if appointment_type:
            filters['type'] = appointment_type
        if patient_id:
            filters['patient_id'] = patient_id

        if not show_cancelled:
            filters['status__in'] = QUEUE_NOT_CANCELLED_CODES

        result_end = page * grab
        result_start = result_end - grab

        if s:
            appointments = self.doctor_scheduled_appointments.filter(**filters).filter(
                Q(patient__first_name__icontains=s) | Q(patient__last_name__icontains=s)
            )
        else:
            appointments = self.doctor_scheduled_appointments.filter(**filters)

        return appointments[result_start:result_end]

    def connect_medical_institution(self, *, medical_institution):
        MedicalInstitutionDoctor = apps.get_model('doctor_profiles.MedicalInstitutionDoctor')
        try:
            return MedicalInstitutionDoctor.objects.create(
                doctor=self,
                medical_institution=medical_institution
            )
        except IntegrityError:
            return MedicalInstitutionDoctor.objects.get(
                doctor=self,
                medical_institution=medical_institution
            )

    def connect_receptionist(self, *, medical_institution, receptionist):
        ReceptionistConnection = apps.get_model('receptionist_profiles.ReceptionistConnection')

        try:
            add_to_mi = ReceptionistConnection.objects.get(
                medical_institution=medical_institution,
                receptionist=receptionist,
                doctor=None
            )
        except ReceptionistConnection.DoesNotExist:
            add_to_mi = ReceptionistConnection.objects.create(
                medical_institution=medical_institution,
                receptionist=receptionist,
                doctor=None
            )

        try:
            receptionist_conn = ReceptionistConnection.objects.get(
                medical_institution=medical_institution,
                receptionist=receptionist,
                doctor=self
            )
        except ReceptionistConnection.DoesNotExist:
            receptionist_conn = ReceptionistConnection.objects.create(
                medical_institution=medical_institution,
                receptionist=receptionist,
                doctor=self
            )

        return receptionist_conn

    def create_schedule(
            self,
            *,
            medical_institution,
            start_time,
            end_time,
            start_date,
            end_date,
            days
    ):
        TimeDim = apps.get_model('datesdim.TimeDim')
        DateDim = apps.get_model('datesdim.DateDim')
        DoctorSchedule = apps.get_model('doctor_profiles.DoctorSchedule')

        result, message, schedule = DoctorSchedule.objects.create(
            doctor=self,
            medical_institution=medical_institution,
            start_time=TimeDim.objects.parse(start_time),
            end_time=TimeDim.objects.parse(end_time),
            start_date=DateDim.objects.parse_get(start_date),
            end_date=DateDim.objects.parse_get(end_date),
            days=days.split("^"),
        )

        return result, message, schedule

    """ questionaires """

    def create_questionnaire(self, **kwargs):
        """
        kwargs:
        - medical_institution: MedicalInstitution
        - restriction: QUESTIONNAIRE_RESTRICTION_CHOICES
        - is_required: boolean
        - name: str
        - description: str
        - created_by: BaseProfile

        Returns:
        result: bool, object: Questionnaire or None, message: str
        """
        Questionnaire = apps.get_model('doctor_profiles.Questionnaire')

        result, obj, message = Questionnaire.objects.create_by_user(
            name=kwargs.get('name'),
            description=kwargs.get('description', None),
            medical_institution=kwargs.get('medical_institution', None),
            created_by=self.user.base_profile(),
            restriction=kwargs.get('restriction', 'private')
        )

        return result, obj, message

    def add_questionnaire(self, **kwargs):
        """
        kwargs:
        - questionnaire: Questionnaire
        - medical_institution: MedicalInstitution
        """
        DoctorQuestionnaire = apps.get_model('doctor_profiles.DoctorQuestionnaire')

        questionnaire = kwargs.get('questionnaire', None)
        if not questionnaire:
            return False, "No questionnaire specified"

        if questionnaire.restriction == 'private' and questionnaire.created_by != self.user.base_profile():
            return False, "Cannot add a private questionnaire"

        if questionnaire.restriction == 'internal' and not self.verify_medical_institution_membership(
                medical_institution=kwargs.get('medical_institution', None)):
            return False, f"Cannot add an internal questionnaire when not a member of {kwargs.get('medical_institution')}"

        medical_institution = kwargs.get('medical_institution', None)
        if medical_institution:
            if not self.verify_medical_institution_membership(medical_institution=kwargs.get('medical_institution')):
                return False, f"{self} is not connected to {medical_institution}"

        return DoctorQuestionnaire.objects.create(
            doctor=self,
            questionnaire=questionnaire,
            medical_institution=medical_institution
        ), "Success"

    def get_questionnaires_rel(self, **kwargs):
        """
        kwargs:
        - medical_institution: MedicalInstitution
        """
        DoctorQuestionnaire = apps.get_model('doctor_profiles.DoctorQuestionnaire')
        filters = {
            'is_approved': True,
            'doctor': self
        }

        if kwargs.get('medical_instituttion', None):
            filters['medical_institution'] = kwargs.get('medical_institution')

        return DoctorQuestionnaire.objects.filter(**filters)

    def get_questionnaires(self, **kwargs):
        """
        kwargs:
        - medical_institution: MedicalInstitution
        """
        Questionnaire = apps.get_model('doctor_profiles.Questionnaire')
        filters = {
            'is_approved': True,
            'doctor': self
        }

        if kwargs.get('medical_instituttion', None):
            filters['medical_institution'] = kwargs.get('medical_institution')

        relids = {i.get('questionnaire_id') for i in self.get_questionnaires_rel(**filters).values('questionnaire_id')}

        return Questionnaire.objects.filter(id__in=relids)

    """ /questionnaires """

    def name_indexing(self):
        return self.__str__()

    def specializations_indexing(self):
        return [x.specialization.name for x in self.get_specializations_rel()]

    def degrees_indexing(self):
        return [x.degree.name for x in self.get_degrees_rel()]

    def associations_indexing(self):
        return [x.association.name for x in self.get_associations_rel()]

    def diplomates_indexing(self):
        return [x.association.name for x in self.get_diplomates_rel()]

    def fellowships_indexing(self):
        return [x.association.name for x in self.get_fellowships_rel()]

    def insurance_providers_indexing(self):
        return [x.insurance.name for x in self.get_insurance_providers_rel()]

    def medical_institutions_indexing(self):
        return [x.medical_institution.name for x in self.get_medical_institutions_rel()]

    def addresses_indexing(self):
        medical_institutions = self.get_medical_institutions()
        addresses = []
        for mi in medical_institutions:
            a = mi.address()
            if a:
                addresses.append(str(a['address']))
        return addresses
