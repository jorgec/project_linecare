from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor_profiles.models import LabTest
from doctor_profiles.serializers.labtest_serializers import LabTestSerializer


class ApiPublicLabtestList(APIView):
    """
    List lab tests
    [optional]
    ?s=str
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)

        if s:
            labtests = LabTest.objects.annotate(
                search=SearchVector(
                    'description',
                    'purpose',
                    'indication',
                    'usage',
                )
            ).filter(
                Q(search=s) |
                Q(name__icontains=s) |
                Q(aliases__icontains=s)
            )
        else:
            labtests = LabTest.objects.all()

        serializer = LabTestSerializer(labtests, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
