from django.urls import path

from accounts import api

urlpatterns = [
    # API

    # Retrieval
    path('api/get_user/by_pk', api.ApiGetUserByPK.as_view(), name='api_get_user_by_pk'),

    # Authentication
    path('api/login', api.ApiLogin.as_view(), name='api_login')
]