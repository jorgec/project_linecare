from elasticsearch_dsl.query import MultiMatch, QueryString
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_indexes.documents import DoctorDocument
from search_indexes.serializers import DoctorDocumentSerializer


class ApiElasticSearchDoctorLookup(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.GET.get('q', None)

        if not q:
            return Response("Search query not set", status=status.HTTP_400_BAD_REQUEST)

        q = f'{q.strip()[:-1]}*'

        query = QueryString(query=q, fields=[
            'name',
            'specializations',
            'degrees',
            'associations',
            'fellowships',
            'diplomates',
            'insurance_providers',
            'medical_institutions',
            'addresses'
        ])
        doctors = DoctorDocument.search().query(query)

        serializer = DoctorDocumentSerializer(doctors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
