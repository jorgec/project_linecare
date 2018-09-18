from django.urls import path

from accounts.modules.api import auth, retrieve

urlpatterns = [
    # API

    # Retrieval
    path('api/get_user/by_pk', retrieve.ApiGetUserByPK.as_view(), name='api_get_user_by_pk'),

    # Authentication
    path('api/login', auth.ApiLogin.as_view(), name='api_login')
]