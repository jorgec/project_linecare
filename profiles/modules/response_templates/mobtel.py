from profiles.serializers import PublicMobtelSerializer, PrivateMobtelSerializer


def mobtel_dict_template(qs):
    data = {}
    for item in qs:
        data[str(item.number)] = PublicMobtelSerializer(item).data
    return data

def private_mobtel_dict_template(qs):
    data = {}
    for item in qs:
        data[str(item.number)] = PrivateMobtelSerializer(item).data
    return data