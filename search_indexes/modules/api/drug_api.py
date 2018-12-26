from elasticsearch_dsl.query import MultiMatch, QueryString
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_indexes.documents import DrugDocument
from search_indexes.serializers import DrugDocumentSerializer


class ApiElasticSearchDrugLookup(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.GET.get('q', None)

        if not q:
            return Response("Search query not set", status=status.HTTP_400_BAD_REQUEST)

        q = f'{q.strip()[:-1]}*'

        query = QueryString(query=q, fields=['name', 'base_name', 'generic_names', 'active_ingredients'])
        drugs = DrugDocument.search().query(query)

        serializer = DrugDocumentSerializer(drugs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
