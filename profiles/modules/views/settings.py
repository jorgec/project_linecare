from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from accounts.forms import EmailChangeForm, PasswordChangeForm
from biometrics.forms import BiometricForm
from biometrics.models import Biometric
from profiles.forms import ProfileUpdateForm


class ProfileSettingsBasicInfoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        form = ProfileUpdateForm(instance=profile)

        context = {
            'page_title': 'Update Basic Info',
            'location': 'profile_settings',
            'sublocation': 'basic',
            'profile': profile,
            'form': form
        }

        return render(request, 'neo/profile/settings/basic_info.html', context)

    def post(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        form = ProfileUpdateForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!', extra_tags='success')
            return HttpResponseRedirect(reverse('profile_settings_basic_info_view'))
        else:
            context = {
                'page_title': 'Update Basic Info',
                'location': 'profile_settings',
                'sublocation': 'basic',
                'profile': profile,
                'form': form
            }

            return render(request, 'neo/profile/settings/basic_info.html', context)


class ProfileSettingsEmailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EmailChangeForm(instance=request.user)

        context = {
            'page_title': 'Update Email',
            'location': 'profile_settings',
            'sublocation': 'email',
            'form': form,
        }

        return render(request, 'neo/profile/settings/email.html', context)

    def post(self, request, *args, **kwargs):
        form = EmailChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Email updated!', extra_tags='success')
            return HttpResponseRedirect(reverse('profile_settings_email_view'))
        else:
            context = {
                'page_title': 'Update Email',
                'location': 'profile_settings',
                'sublocation': 'email',
                'form': form,
            }

            return render(request, 'neo/profile/settings/email.html', context)


class ProfileSettingsPasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(instance=request.user)

        context = {
            'page_title': 'Update Password',
            'location': 'profile_settings',
            'sublocation': 'password',
            'form': form
        }

        return render(request, 'neo/profile/settings/password.html', context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()

            messages.success(request, 'Password updated!', extra_tags='success')
            return HttpResponseRedirect(reverse('profile_settings_password_view'))
        else:
            context = {
                'page_title': 'Update Password',
                'location': 'profile_settings',
                'sublocation': 'password',
                'form': form
            }

            return render(request, 'neo/profile/settings/password.html', context)


class BiometricsCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()

        if profile.get_biometrics():
            return HttpResponseRedirect(reverse('profile_settings_biometrics_update'))

        form = BiometricForm

        context = {
            'page_title': 'Initialize Biometric data',
            'location': 'profile_settings',
            'sublocation': 'biometrics',
            'profile': profile,
            'form': form
        }

        return render(request, 'neo/profile/settings/biometrics/create.html', context)

    def post(self, request, *args, **kwargs):

        formdata = {
            'height': request.POST.get('height', None),
            'weight': request.POST.get('weight', None),
            'blood_type': request.POST.get('blood_type', None)
        }

        is_valid, bm_response = Biometric.objects.validate(**formdata)

        if is_valid:
            bm = Biometric(
                height=bm_response['height'],
                weight=bm_response['weight'],
                blood_type=bm_response['blood_type'],
                user=request.user
            )
            bm.save()
            messages.success(request, "Biometrics saved", extra_tags='success')
            return HttpResponseRedirect(reverse('profile_settings_biometrics_update'))
        else:
            messages.success(request, bm_response, extra_tags='danger')
            return HttpResponseRedirect(reverse('profile_settings_biometrics_create'))


class BiometricsUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        biometrics = profile.get_biometrics()

        if not biometrics:
            return HttpResponseRedirect(reverse('profile_settings_biometrics_create'))

        form = BiometricForm(instance=biometrics)

        context = {
            'page_title': 'Update Biometric data',
            'location': 'profile_settings',
            'sublocation': 'biometrics',
            'profile': profile,
            'form': form
        }

        return render(request, 'neo/profile/settings/biometrics/create.html', context)

    def post(self, request, *args, **kwargs):
        biometrics = request.user.base_profile().get_biometrics()
        formdata = {
            'height': request.POST.get('height', None),
            'weight': request.POST.get('weight', None),
            'blood_type': request.POST.get('blood_type', None)
        }

        is_valid, bm_response = Biometric.objects.validate(**formdata)

        if is_valid:

            biometrics.height = bm_response['height']
            biometrics.weight = bm_response['weight']
            biometrics.blood_type = bm_response['blood_type']

            biometrics.save()

            messages.success(request, "Biometrics saved", extra_tags='success')
            return HttpResponseRedirect(reverse('profile_settings_biometrics_update'))
        else:
            messages.success(request, bm_response, extra_tags='danger')
            return HttpResponseRedirect(reverse('profile_settings_biometrics_create'))