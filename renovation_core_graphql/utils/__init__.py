from graphql import GraphQLSchema
from .resolvers import search_link_resolver


def bind_schema(schema: GraphQLSchema):
    schema.query_type.fields[
        "search_link"].resolve = search_link_resolver
