from django.contrib.postgres.search import SearchVector
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drug_information.models import Drug, GenericName
from drug_information.serializers.drug_serializers import DrugSerializer, GenericNameSerializer


class ApiPublicGenericNameList(APIView):
    """
    List of generic names
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        if s:
            drugs = GenericName.objects.filter(name__icontains=s)
        else:
            drugs = GenericName.objects.all()

        serializer = GenericNameSerializer(drugs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiPublicDrugList(APIView):
    """
    List of prescriptions
    [optional]
    ?s=str
    ?page=n
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        page = request.GET.get('page', None)
        if s:
            drugs = Drug.objects.annotate(
                search=SearchVector('name', 'generic_name__name')
            ).filter(search__icontains=s)
        else:
            drugs = Drug.objects.all()

        if not page:
            drugs = drugs[:10]
        else:
            start = page * 10
            end = start + 10
            drugs = drugs[start:end]

        serializer = DrugSerializer(drugs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
