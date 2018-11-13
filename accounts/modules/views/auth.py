from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.forms import LoginForm, RegisterForm
from accounts.models import Account
from helpers.errors import PrettyErrors


class AccountRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm

        context = {
            'page_title': 'Welcome to LineCare!',
            'form': form
        }

        return render(request, 'neo/accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            account = Account.objects.create_user(
                email=email,
                password=password,
            )

            primary_profile = request.POST.get('primary_profile')

            if primary_profile == "1":
                # doctor profile

                """
                todo create doctor profile
                """

                account.user_settings = {
                    'primary_profile': {
                        'type': 'doctor',
                        'pk': None # doctor profile pk
                    }
                }
            elif primary_profile == "2":
                # patient profile
                pass
            elif primary_profile == "3":
                # receptionist profile
                pass

            account.save()
            context = {
                'page_title': 'Welcome to LineCare!',
                'form': form
            }

            user = authenticate(email=account.email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created! Please fill up your profile.", extra_tags="success")
                profile = user.base_profile()

                request.session['login_origin'] = 'internal'

                if profile.is_fresh:
                    return HttpResponseRedirect(reverse('profile_settings_basic_info_view'))
            else:
                messages.error(request, "Unable to authenticate your account", extra_tags="danger")
                return HttpResponseRedirect(reverse('accounts_register'))
        else:
            errors = PrettyErrors(errors=form.errors)
            messages.error(request, errors.as_html(), extra_tags="danger")
            return HttpResponseRedirect(reverse('accounts_register'))


class AccountLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm

        context = {
            'page_title': 'Login',
            'form': form
        }

        return render(request, 'neo/accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "User account is not active", extra_tags="danger")
                return HttpResponseRedirect(reverse('accounts_login'))

            login(request, user)
            messages.success(request, "Welcome to LineCare!", extra_tags="success")

            profile = user.base_profile()
            if profile.is_fresh:
                return HttpResponseRedirect(reverse('profile_settings_basic_info_view'))

        else:
            messages.error(request, "Invalid credentials", extra_tags="danger")
            return HttpResponseRedirect(reverse('accounts_login'))


class AccountLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('accounts_login'))
