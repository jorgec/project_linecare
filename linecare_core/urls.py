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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# from graphene_django.views import GraphQLView
from rest_framework.documentation import include_docs_urls

from accounts.modules.views.auth import AccountLoginView

from accounts.modules.api.auth import ApiFacebookLogin
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Linecare Core API')

urlpatterns = [
    path('mHBvVWdpEY/', admin.site.urls),
    path('policy/', TemplateView.as_view(template_name='neo/static_pages/privacy_policy.html')),
    path('terms/', TemplateView.as_view(template_name='neo/static_pages/terms_and_services.html')),
    path('', AccountLoginView.as_view(), name='home'),
    path('terms/', AccountLoginView.as_view(), name='terms'),
    path('policy/', AccountLoginView.as_view(), name='policy'),

    # auths
    path('accounts/', include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook', ApiFacebookLogin.as_view(), name='api_facebook_login'),
    # /auth

    path('location/', include('locations.urls')),
    path('profile/', include('profiles.urls')),
    path('album/', include('albums.urls')),
    path('doctor/', include('doctor_profiles.urls')),
    path('receptionist/', include('receptionist_profiles.urls')),
    path('drug/', include('drug_information.urls')),

    path('search/', include('search_indexes.urls')),
    # path('graphql/', GraphQLView.as_view(graphiql=True))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('apidocs/', schema_view),
        path('docs/', include_docs_urls(title='Linecare DRF Docs')),
        # path('swagger', yasg_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        # path('redoc', yasg_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        # url(r'^swagger(?P<format>\.json|\.yaml)$', yasg_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]
