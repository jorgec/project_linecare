from django.urls import path

from accounts.modules.api import auth, retrieve
from .modules.views import auth as auth_views
from .modules.views import postlogin as postlogin_views

urlpatterns = [
    # API

    # Retrieval

    # Single
    path('api/get_user/by_pk', retrieve.ApiPrivateAccountGetByPK.as_view(), name='api_get_user_by_pk'),
    path('api/get_user/by_username', retrieve.ApiPublicAccountGetByUsername.as_view(), name='api_get_user_by_username'),
    path('api/get_user/by_email', retrieve.ApiPrivateAccountGetByEmail.as_view(), name='api_get_user_by_email'),

    # Many
    path('api/public/get_users/by_parent', retrieve.ApiPublicAccountsGetByParent.as_view(),
         name='api_public_get_users_by_parent'),
    path('api/public/get_users/by_type', retrieve.ApiPublicAccountsGetByUserType.as_view(),
         name='api_public_get_users_by_user_type'),
    path('api/private/get_users/by_type', retrieve.ApiPrivateAccountsGetByUserType.as_view(),
         name='api_private_get_users_by_user_type'),
    path('api/public/get_users', retrieve.ApiPublicAccountsGetAll.as_view(), name='api_public_get_users'),
    path('api/private/get_users', retrieve.ApiAdminAccountsGetAll.as_view(), name='api_private_get_users'),

    # Authentication
    path('api/login', auth.ApiLogin.as_view(), name='api_login'),
    path('api/register', auth.ApiRegister.as_view(), name='api_register')
]


# Views
urlpatterns += [
    path('register', auth_views.AccountRegistrationView.as_view(), name='accounts_register'),
    path('login', auth_views.AccountLoginView.as_view(), name='accounts_login'),
    path('logout', auth_views.AccountLogoutView.as_view(), name='accounts_logout'),

    path('postlogin', postlogin_views.PostLoginInitialView.as_view(), name='accounts_postlogin'),
]