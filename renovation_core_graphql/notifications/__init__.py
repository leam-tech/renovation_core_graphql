from graphql import GraphQLSchema

from .resolvers import \
    register_fcm_client_resolver, get_user_notifications_resolver, \
    mark_all_fcm_read_resolver, mark_fcm_seen_resolver


def bind_schema(schema: GraphQLSchema):
    schema.mutation_type.fields["register_fcm_client"].resolve = register_fcm_client_resolver
    schema.mutation_type.fields["get_user_notifications"].resolve = get_user_notifications_resolver
    schema.mutation_type.fields["mark_all_fcm_read"].resolve = mark_all_fcm_read_resolver
    schema.mutation_type.fields["mark_fcm_seen"].resolve = mark_fcm_seen_resolver
