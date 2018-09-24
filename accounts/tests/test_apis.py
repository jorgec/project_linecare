import json

import pytest
from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.constants import USER_TYPES_TO_TEST, SUPERADMIN, USER_TYPE_CHOICES, ADMIN
from accounts.models import Account
from accounts.modules.api import auth, retrieve
from accounts.serializers import AccountSerializer, AccountSerializerPublic

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class TestApiViews:
    def test_init(self):
        user = mixer.blend('accounts.Account')
        assert user.pk == 1, "Should have a user"

    def test_get_user_by_pk_public(self):
        # create dummy user
        user = mixer.blend('accounts.Account')

        request = factory.get('/', {'pk': user.pk})
        response = retrieve.ApiGetUserByPK.as_view()(request)
        assert response.status_code == 401, "Must not be accessed if not authenticated"

    def test_get_user_by_pk_private(self):
        # create dummy user
        user = mixer.blend('accounts.Account')

        request = factory.get('/', {'pk': user.pk})
        force_authenticate(request, user=user)
        response = retrieve.ApiGetUserByPK.as_view()(request)
        assert response.status_code == 200, "Must be accessible if force_authed"

        request = factory.get('/')
        force_authenticate(request, user=user)
        response = retrieve.ApiGetUserByPK.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

    def test_get_user_by_username(self):
        user = mixer.blend('accounts.Account')

        request = factory.get('/', {'username': user.username})
        response = retrieve.ApiGetUserByUsername.as_view()(request)
        assert response.status_code == 200, "Able to call this user by username"

        request = factory.get('/')
        response = retrieve.ApiGetUserByUsername.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

    def test_get_users_by_user_type_public(self):
        for type in USER_TYPES_TO_TEST:
            users = []
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    username='user_{}_{}'.format(i, type[0]),
                    user_type=type[0]
                )
                u = {
                    'username': user.username,
                    'user_type': user.user_type
                }
                users.append(u)
            request = factory.get('/', {'user_type': type[0]})
            response = retrieve.ApiPublicGetUsersByUserType.as_view()(request)
            assert response.status_code == 200, "Call successful"
            assert len(response.data) == len(users), "Expected number of users, {}".format(response.data)

        request = factory.get('/')
        response = retrieve.ApiPublicGetUsersByUserType.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

    def test_get_users_by_user_type_private(self):
        requser = mixer.blend('accounts.Account', user_type=SUPERADMIN)
        requser.is_admin = True
        for type in USER_TYPES_TO_TEST:
            users = []
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    username='user_{}_{}'.format(i, type[0]),
                    user_type=type[0]
                )
                u = {
                    'username': user.username,
                    'user_type': user.user_type
                }
                users.append(u)
            request = factory.get('/', {'user_type': type[0]})
            force_authenticate(request, user=requser)
            response = retrieve.ApiPrivateGetUsersByUserType.as_view()(request)
            assert response.status_code == 200, "Call successful"
            assert len(response.data) == len(users), "Expected number of users, {}".format(response.data)

        request = factory.get('/')
        force_authenticate(request, user=requser)
        response = retrieve.ApiPrivateGetUsersByUserType.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

    def test_get_users_by_user_type_private_no_access(self):
        request = factory.get('/', {'user_type': 1})
        response = retrieve.ApiPrivateGetUsersByUserType.as_view()(request)
        assert response.status_code == 401, "Prevent non-admins"

    def test_get_users_public(self):
        for type in USER_TYPE_CHOICES:
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    username='user_{}_{}'.format(i, type[0]),
                    user_type=type[0]
                )
        users = Account.objects.exclude(
            Q(user_type=SUPERADMIN) | Q(user_type=ADMIN)
        ).actives()

        serializer = AccountSerializerPublic(users, many=True)

        request = factory.get('/')
        response = retrieve.ApiPublicGetUsers.as_view()(request)
        assert response.status_code == 200, "Call successful"
        assert serializer.data == response.data, "Users match"
        for user in response.data:
            assert user['user_type'] != SUPERADMIN and user[
                'user_type'] != ADMIN, "Superadmins and admins must not show up"

    def test_get_users_private(self):
        requser = mixer.blend('accounts.Account', user_type=SUPERADMIN)
        requser.is_admin = True
        for type in USER_TYPE_CHOICES:
            for i in range(5):
                user = mixer.blend(
                    'accounts.Account',
                    username='user_{}_{}'.format(i, type[0]),
                    user_type=type[0]
                )

        users = Account.objects.actives()
        serializer = AccountSerializer(users, many=True)

        request = factory.get('/')
        force_authenticate(request, user=requser)
        response = retrieve.ApiPrivateGetUsers.as_view()(request)
        assert response.status_code == 200, "Call successful"
        assert response.data == serializer.data, "Users match"

    def test_get_users_by_parent(self):
        parent = mixer.blend('accounts.Account')
        for i in range(5):
            child = mixer.blend('accounts.Account', parent_id=parent.id)

        users = Account.objects.filter(parent_id=parent.id)
        serializer = AccountSerializerPublic(users, many=True)

        request = factory.get('/', {'parent': parent.id})
        response = retrieve.ApiGetUsersByParent.as_view()(request)

        assert response.status_code == 200, "Call successful"
        assert serializer.data == response.data, "Users match"

        request = factory.get('/')
        response = retrieve.ApiGetUsersByParent.as_view()(request)
        assert response.status_code == 400, "Must fail on bad request"

    def test_remote_login(self):
        user = Account.objects.create_user(
            username='juantester',
            email='asdgasd@sadg.com'
        )
        user.set_password('asdf1234')
        user.save()

        request = factory.post('/', json.dumps({
            'email': 'asdgasd@sadg.com',
            'password': 'asdf1234'
        }), content_type='application/json')

        response = auth.ApiLogin.as_view()(request)
        assert response.status_code == 200, response.data

        request = factory.post('/', json.dumps({
            'email': 'a3sdgasd@sadg.com',
            'password': 'asdf1234'
        }), content_type='application/json')

        response = auth.ApiLogin.as_view()(request)
        assert response.status_code == 401, response.data

        request = factory.post('/', json.dumps({
            'email': '',
            'password': ''
        }), content_type='application/json')

        response = auth.ApiLogin.as_view()(request)
        assert response.status_code == 400, response.data

    def test_remote_register(self):
        request = factory.post('/', {
            'username': 'juantester',
            'email': 'juan@tester.com',
            'password': 'asdf1234',
            'first_name': 'Juan',
            'last_name': 'Tester'
        }, format='json')

        response = auth.ApiRegister.as_view()(request)

        try:
            user = Account.objects.get(username='juantester')
        except Account.DoesNotExist:
            user = None

        assert user is not None, "User was created"
        assert response.status_code == 200, response.data

        # duplicate
        request = factory.post('/', {
            'username': 'juantester',
            'email': 'juan@tester.com',
            'password': 'asdf1234',
            'first_name': 'Juan',
            'last_name': 'Tester'
        }, format='json')

        response = auth.ApiRegister.as_view()(request)
        assert response.status_code == 400, response.data

        # no username
        request = factory.post('/', {
            'username': '',
            'email': 'juan2@tester.com',
            'password': 'asdf1234',
            'first_name': 'Juan',
            'last_name': 'Tester'
        }, format='json')

        response = auth.ApiRegister.as_view()(request)
        assert response.status_code == 200, response.data

        # bad form
        request = factory.post('/', {
            'username': '',
            'email': '',
            'password': 'asdf1234',
            'first_name': 'Juan',
            'last_name': 'Tester'
        }, format='json')

        response = auth.ApiRegister.as_view()(request)
        assert response.status_code == 400, response.data
