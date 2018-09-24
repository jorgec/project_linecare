from django.urls import path

from accounts.modules.api import auth, retrieve

urlpatterns = [
    # API

    # Retrieval

    # Single
    path('api/get_user/by_pk', retrieve.ApiGetUserByPK.as_view(), name='api_get_user_by_pk'),
    path('api/get_user/by_username', retrieve.ApiGetUserByUsername.as_view(), name='api_get_user_by_username'),
    path('api/get_user/by_email', retrieve.ApiGetUserByEmail.as_view(), name='api_get_user_by_email'),

    # Many
    path('api/public/get_users/by_parent', retrieve.ApiGetUsersByParent.as_view(),
         name='api_public_get_users_by_parent'),
    path('api/public/get_users/by_type', retrieve.ApiPublicGetUsersByUserType.as_view(),
         name='api_public_get_users_by_user_type'),
    path('api/private/get_users/by_type', retrieve.ApiPrivateGetUsersByUserType.as_view(),
         name='api_private_get_users_by_user_type'),
    path('api/public/get_users', retrieve.ApiPublicGetUsers.as_view(), name='api_public_get_users'),
    path('api/private/get_users', retrieve.ApiPrivateGetUsers.as_view(), name='api_private_get_users'),

    # Authentication
    path('api/login', auth.ApiLogin.as_view(), name='api_login'),
    path('api/register', auth.ApiRegister.as_view(), name='api_register')
]
