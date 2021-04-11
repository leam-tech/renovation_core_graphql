from graphql import GraphQLSchema

from .meta import get_doc_meta_bundle_resolver
from .assign_doc import \
    get_docs_assigned_to_user_resolver, \
    get_users_assigned_to_doc_resolver, \
    assign_doc_resolver, \
    unassign_doc_resolver, \
    set_assignment_status_resolver


def bind_schema(schema: GraphQLSchema):
    schema.query_type.fields["get_docs_assigned_to_user"].resolve = \
        get_docs_assigned_to_user_resolver
    schema.query_type.fields["get_users_assigned_to_doc"].resolve = \
        get_users_assigned_to_doc_resolver

    schema.mutation_type.fields["assign_doc"].resolve = assign_doc_resolver
    schema.mutation_type.fields["unassign_doc"].resolve = unassign_doc_resolver
    schema.mutation_type.fields["set_assignment_status"].resolve = set_assignment_status_resolver

    schema.query_type.fields["get_doc_meta_bundle"].resolve = get_doc_meta_bundle_resolver
