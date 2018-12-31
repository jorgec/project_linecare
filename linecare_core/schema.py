import drug_information.graphql.drug_schema as drug_schema
import graphene

from graphene_django.debug import DjangoDebug


class Query(
    drug_schema.Query,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)
