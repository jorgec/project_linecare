from profiles.serializers import PublicPhoneSerializer, PrivatePhoneSerializer


def phone_dict_template(qs):
    data = {}
    for item in qs:
        data[str(item.number)] = PublicPhoneSerializer(item).data
    return data

def private_phone_dict_template(qs):
    data = {}
    for item in qs:
        data[str(item.number)] = PrivatePhoneSerializer(item).data
    return data