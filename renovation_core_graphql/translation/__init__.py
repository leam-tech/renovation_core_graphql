from graphql import GraphQLSchema

from .add_translation import add_translation_resolver
from .add_translation_multiple import add_translation_multiple_resolver
from .get_doc_translation import get_doc_translation_resolver


def bind_schema(schema: GraphQLSchema):
    schema.mutation_type.fields["addTranslation"].resolve = add_translation_resolver
    schema.mutation_type.fields["addTranslationMultiple"].resolve = \
        add_translation_multiple_resolver
    schema.query_type.fields["getDocTranslation"].resolve = get_doc_translation_resolver
