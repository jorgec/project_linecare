from django import template

register = template.Library()

@register.simple_tag
def get_doctor_receptionists(doctor, medical_institution):
    return doctor.get_receptionists(medical_institution=medical_institution)