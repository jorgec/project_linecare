from elasticsearch_dsl.query import MultiMatch, QueryString
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from drug_information.models import Drug
from drug_information.serializers.drug_serializers import DrugSerializer
from search_indexes.documents import DrugDocument
from search_indexes.serializers import DrugDocumentSerializer


class ApiElasticSearchDrugLookup(APIView):
    """
    Elasticsearch implementation
    ?q=str
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.GET.get('q', None)

        if not q:
            return Response("Search query not set", status=status.HTTP_400_BAD_REQUEST)

        q = f'*{q.strip()[:-1]}*'

        query = QueryString(query=q, fields=['name', 'base_name', 'generic_names', 'active_ingredients'])
        drugs = DrugDocument.search().query(query)

        serializer = DrugDocumentSerializer(drugs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiDrugDetail(APIView):
    """
    Drug detail via id
    ?id=drug_id
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        id = request.GET.get('id', None)
        drug = get_object_or_404(Drug, id=id)
        serializer = DrugSerializer(drug)

        return Response(serializer.data, status=status.HTTP_200_OK)
