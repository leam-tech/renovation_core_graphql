from graphql import GraphQLType, GraphQLResolveInfo
from renovation_core.utils.translate import get_ctx_translation

from frappe.model.meta import Meta
from frappe_graphql.utils.resolver.translate import \
    _translatable_resolver as default_translatable_resolver


def setup_ctx_translation_resolver(meta: Meta, gql_type: GraphQLType):
    for df_fieldname in meta.get_translatable_fields():
        if df_fieldname not in gql_type.fields:
            continue

        gql_field = gql_type.fields[df_fieldname]
        if gql_field.resolve and gql_field.resolve != default_translatable_resolver:
            continue

        gql_field.resolve = _translatable_resolver


def _translatable_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return get_ctx_translation(
        doc=obj,
        fieldname=info.field_name,
        value=obj.get(info.field_name)
    )
