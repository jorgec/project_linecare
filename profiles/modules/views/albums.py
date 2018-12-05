from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from albums.forms import PhotoUploadForm
from albums.models import Album


class BaseProfileAlbumList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()

        context = {
            'page_title': profile,
            'location': 'profile_albums',
            'sublocation': 'home',
            'profile': profile,
            'albums': profile.get_all_albums()
        }

        return render(request, 'neo/profile/albums/home.html', context)


class BaseProfileAlbumDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.base_profile()
        album = get_object_or_404(Album, slug=kwargs['slug'])

        context = {
            'page_title': profile,
            'location': 'profile_albums',
            'sublocation': 'home',
            'profile': profile,
            'album': album,
            'upload_form': PhotoUploadForm
        }

        return render(request, 'neo/profile/albums/detail.html', context)

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, slug=kwargs['slug'])
        form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.save()

            messages.success(request, "Photo uploaded!", extra_tags='success')
        else:
            messages.error(request, form.errors, extra_tags='danger')

        return HttpResponseRedirect(reverse('profile_album_detail', kwargs={
            'slug': album.slug
        }))
