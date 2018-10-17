from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.forms import LoginForm, RegisterForm


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

            """ CAPTCHA """
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            """ /CAPTCHA """

            if not result['success']:
                messages.error(request, "Invalid reCAPTCHA. Please try again.", extra_tags="danger")
                return HttpResponseRedirect(reverse('frontend_home_view'))

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            account = Account.objects.create_user(
                email=email,
                password=password,
                user_type=TOURIST
            )

            """ email """
            email_subject = 'Welcome to Paradise!'
            email_body = "Thank you for registering; you can now schedule a visit to the island paradise of Boracay!" \
                         "\n\n\nFor future reference, you can login via the email and password you provided at {}{}." \
                         "\n\n\n\nCheers!\n\n" \
                         "https://www.paradiso.com.ph".format(
                settings.SITE_URL,
                reverse('accounts_login_view')
            )
            from_email = 'do-not-reply@paradiso.com.ph'
            to_email = email
            mail = EmailMultiAlternatives(
                subject=email_subject,
                body=email_body,
                from_email=from_email,
                to=[to_email],
            )
            mail.send()
            """ /email """

            user = authenticate(email=account.email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created! Please fill up your profile.", extra_tags="success")
                return HttpResponseRedirect(reverse('profiles_home_view'))
            else:
                messages.error(request, "Unable to authenticate your account", extra_tags="danger")
                return HttpResponseRedirect(reverse('frontend_home_view'))
        else:
            errors = PrettyErrors(errors=form.errors)
            messages.error(request, errors.as_html(), extra_tags="danger")
            return HttpResponseRedirect(reverse('frontend_home_view'))


class AccountLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm

        context = {
            'page_title': 'Login',
            'form': form
        }

        return render(request, 'accounts/login.html', context)

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


        else:
            messages.error(request, "Unable to authenticate your account", extra_tags="danger")
            return HttpResponseRedirect(reverse('accounts_login_view'))


class AccountLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('frontend_home_view'))
