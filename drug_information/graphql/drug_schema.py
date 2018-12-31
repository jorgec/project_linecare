import graphene
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from drug_information.models import Drug


class DrugNode(DjangoObjectType):
    class Meta:
        model = Drug
        interfaces = (Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'generic_name__name': ['exact', 'icontains', 'istartswith'],
        }


class Query(graphene.ObjectType):
    drug = Node.Field(DrugNode)
    all_drugs = DjangoFilterConnectionField(DrugNode)
