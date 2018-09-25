from albums.serializers import AlbumSerializer, PhotoSerializer
from profiles.serializers import PublicMobtelSerializer


def public_profile_template(user):

    profile = user.base_profile()
    albums = profile.get_albums()
    _albums = ''
    mobtels = profile.get_public_mobtels()
    _mobtels = ''
    profile_photo = profile.get_profile_photo()
    _profile_photo = ''
    cover_photo = profile.get_cover_photo()
    _cover_photo = ''

    if albums:
        _albums = AlbumSerializer(albums, many=True).data
    if mobtels:
        _mobtels = PublicMobtelSerializer(mobtels, many=True).data
    if  profile_photo:
        _profile_photo = PhotoSerializer(profile_photo).data
    if cover_photo:
        _cover_photo = PhotoSerializer(cover_photo).data


    data = {
        'username': user.username,
        'user_type': user.user_type,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': profile.gender,
        'profile_photo': _profile_photo,
        'cover_photo': _cover_photo,
        'albums': _albums,
        'mobtels': _mobtels
    }


    return data

