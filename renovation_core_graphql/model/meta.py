
from graphql import GraphQLResolveInfo

from renovation_core.utils.meta import get_bundle


def get_doc_meta_bundle_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return get_bundle(
        doctype=kwargs.get("doctype"),
        user=kwargs.get("user")
    )
