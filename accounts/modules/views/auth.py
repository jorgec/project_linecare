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

            context = {
                'page_title': 'Welcome to LineCare!',
                'form': form
            }

            user = authenticate(email=account.email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created! Please fill up your profile.", extra_tags="success")
                profile = user.base_profile()
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
                return HttpResponseRedirect(reverse('accounts_login_view'))

            login(request, user)
            messages.success(request, "Welcome to LineCare!", extra_tags="success")

            profile = user.base_profile()
            if profile.is_fresh:
                return HttpResponseRedirect(reverse('profile_settings_basic_info_view'))

        else:
            messages.error(request, "Unable to authenticate your account", extra_tags="danger")
            return HttpResponseRedirect(reverse('accounts_login_view'))


class AccountLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('accounts_login'))
