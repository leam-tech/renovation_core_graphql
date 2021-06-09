from graphql import GraphQLSchema
from .resolvers import get_renovation_report_resolver, \
    export_renovation_report_resolver


def bind_schema(schema: GraphQLSchema):
    schema.query_type.fields[
        "getRenovationReport"].resolve = get_renovation_report_resolver
    schema.query_type.fields[
        "exportRenovationReport"].resolve = export_renovation_report_resolver
