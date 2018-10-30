import os
import uuid

import requests
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from albums.models import Photo
from helpers.file_extensions import FILE_EXTENSIONS


class PostLoginInitialView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()

        login_origin = request.session.get('login_origin', None)

        if profile.is_fresh:

            if login_origin:
                if login_origin == 'internal':
                    pass
            else:

                # Facebook login
                try:
                    facebook = SocialAccount.objects.get(user=request.user, provider='facebook')
                    data = facebook.extra_data
                    profile.first_name = data['first_name']
                    profile.last_name = data['last_name']

                    if not data['picture']['data']['is_silhouette']:

                        photo = requests .get(data['picture']['data']['url'], allow_redirects=True)
                        if photo.status_code == 200:
                            album = profile.get_profile_album()
                            type = photo.headers['Content-Type']

                            filename = '{}.{}'.format(
                                uuid.uuid4(),
                                FILE_EXTENSIONS[type]
                            )
                            upload_path = '{}uploads/{}/{}'.format(
                                settings.MEDIA_ROOT,
                                request.user.pk,
                                album.slug,
                            )

                            if not os.path.exists(upload_path):
                                os.makedirs(upload_path)

                            upload_file = '{}/{}'.format(upload_path, filename)
                            open(upload_file, 'wb').write(photo.content)

                            object_path = 'uploads/{}/{}/{}'.format(
                                request.user.pk,
                                album.slug,
                                filename
                            )

                            profile_photo = Photo.objects.create(
                                photo=object_path,
                                caption='Facebook Profile Photo',
                                is_primary=True,
                                is_public=True,
                                album=album
                            )
                    profile.is_fresh = False
                    profile.save()
                    return HttpResponseRedirect(reverse('profile_settings_basic_info_view'))

                except SocialAccount.DoesNotExist:
                    pass