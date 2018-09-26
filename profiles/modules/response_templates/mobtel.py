from profiles.serializers import PublicMobtelSerializer


def mobtel_dict_template(qs):
    data = {}
    for item in qs:
        data[str(item.number)] = PublicMobtelSerializer(item).data
    return data
