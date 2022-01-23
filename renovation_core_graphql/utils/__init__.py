from graphql import GraphQLSchema
from renovation_core_graphql.utils.resolvers import search_link_resolver, export_data_resolver


def bind_schema(schema: GraphQLSchema):
    schema.query_type.fields[
        "search_link"].resolve = search_link_resolver
    schema.query_type.fields["export_data"].resolve = export_data_resolver
