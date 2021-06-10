import frappe
from graphql import GraphQLResolveInfo
from renovation_core.utils.translate import add_translation


def add_translation_multiple_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    translations = kwargs.get("translations")
    translation_docs = []

    for tr in translations:
        tr = add_translation(
            language=tr.get("language", None),
            source_text=tr.get("source_text", None),
            translated_text=tr.get("translated_text", None),
            context=tr.get("context", None),
            doctype=tr.get("doctype", None),
            docname=tr.get("docname", None),
            docfield=tr.get("docfield", None),
        )
        translation_docs.append(
            frappe._dict(
                doctype="Translation",
                name=tr.name
            )
        )

    return translation_docs
