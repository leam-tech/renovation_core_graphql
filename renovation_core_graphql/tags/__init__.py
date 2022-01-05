from graphql import GraphQLSchema

from .resolvers import get_tags_resolver, add_tag_link_resolver, remove_tag_link_resolver


def bind_schema(schema: GraphQLSchema):
    schema.mutation_type.fields["addTag"].resolve = add_tag_link_resolver
    schema.mutation_type.fields["removeTag"].resolve = remove_tag_link_resolver
    schema.query_type.fields["tags"].resolve = get_tags_resolver
