import frappe
from graphql import GraphQLResolveInfo
from renovation_core.utils.translate import add_translation


def add_translation_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    tr = kwargs.get("translation")
    translation = add_translation(
        language=tr.get("language", None),
        source_text=tr.get("source_text", None),
        translated_text=tr.get("translated_text", None),
        context=tr.get("context", None),
        doctype=tr.get("doctype", None),
        docname=tr.get("docname", None),
        docfield=tr.get("docfield", None),
    )

    return frappe._dict(
        doctype="Translation",
        name=translation.name
    )
