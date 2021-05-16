import frappe
from graphql import GraphQLResolveInfo
from renovation_core.utils.translate import add_translation


def add_translation_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    translation = add_translation(
        language=kwargs.get("language", None),
        source_text=kwargs.get("source_text", None),
        translated_text=kwargs.get("translated_text", None),
        context=kwargs.get("context", None),
        doctype=kwargs.get("doctype", None),
        docname=kwargs.get("docname", None),
        docfield=kwargs.get("docfield", None),
    )

    return frappe._dict(
        doctype="Translation",
        name=translation.name
    )
