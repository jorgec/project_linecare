from django.contrib.postgres.search import SearchVector
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drug_information.models import Drug, GenericName
from drug_information.serializers.drug_serializers import DrugSerializer, GenericNameSerializer, DrugCreateSerializer


class ApiPublicGenericNameList(APIView):
    """
    List of generic names
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        s = request.GET.get('s', None)
        page = request.GET.get('page', None)
        if s:
            drugs = GenericName.objects.filter(name__icontains=s)
        else:
            drugs = GenericName.objects.all()

        if not page:
            drugs = drugs[:10]
        else:
            start = page * 10
            end = start + 10
            drugs = drugs[start:end]

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
            drugs = Drug.objects.filter(
                Q(name__icontains=s) |
                Q(base_name__icontains=s) |
                Q(generic_name__name__icontains=s) |
                Q(drug_ingredients__active_ingredient__name__icontains=s) |
                Q(meta__generic_names__icontains=s)
            )
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


class ApiPrivateDrugCreate(APIView):
    """
    Add a new drug
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.data.get('is_generic', None) == 'yes':
            try:
                generic = GenericName.objects.create(
                    name=request.data.get('name')
                )
            except IntegrityError:
                generic = GenericName.objects.get(name=request.data.get('name'))

            try:
                drug = Drug.objects.create(
                    name=request.data.get('name'),
                    base_name=request.data.get('base_name'),
                    generic_name=generic,
                    is_generic=True,
                    product_type=request.data.get('product_type')
                )
            except IntegrityError:
                drug = Drug.objects.get(base_name=request.data.get('base_name'))
        else:
            try:
                generic = GenericName.objects.get(id=request.data.get('generic_name_id'))
            except GenericName.DoesNotExist:
                generic = None

            try:
                drug = Drug.objects.create(
                    name=request.data.get('name'),
                    base_name=request.data.get('base_name'),
                    generic_name=generic,
                    is_generic=False,
                    product_type=request.data.get('product_type')
                )
            except IntegrityError:
                drug = Drug.objects.get(base_name=request.data.get('base_name'))

        serializer = DrugSerializer(drug)

        return Response(serializer.data, status=status.HTTP_200_OK)
