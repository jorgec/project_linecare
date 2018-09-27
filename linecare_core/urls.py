"""linecare_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from accounts.modules.api.auth import ApiFacebookLogin
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Linecare Core API')

urlpatterns = [
    path('mHBvVWdpEY/', admin.site.urls),

    # auths
    path('accounts/', include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook', ApiFacebookLogin.as_view(), name='api_facebook_login'),
    # /auth

    path('profile/', include('profiles.urls')),
    path('album/', include('albums.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('apidocs/', schema_view)
    ]