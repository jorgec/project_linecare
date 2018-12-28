from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drug_information.models.drug_models import DrugRoute
from drug_information.serializers.drug_route_serializers import DrugRouteSerializer


class ApiDrugRouteList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        routes = DrugRoute.objects.all()

        serializer = DrugRouteSerializer(routes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
