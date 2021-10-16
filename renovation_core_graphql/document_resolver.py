from frappe.utils import cint
from graphql import GraphQLResolveInfo

import frappe
from frappe_graphql.utils.resolver import document_resolver, get_singular_doctype
from renovation_core.utils.translate import get_doc_field_translation


def resolve(obj, info: GraphQLResolveInfo, **kwargs):
    # We are here just to implement our custom translation
    frappe.flags.ignore_doc_resolver_translation = True
    value = document_resolver(
        obj=obj, info=info, **kwargs
    )
    doctype = obj.get('doctype') or get_singular_doctype(info.parent_type.name)
    meta = frappe.get_meta(doctype)
    df = meta.get_field(info.field_name)

    if df and cint(df.get("translatable")):
        try:
            cached_doc = frappe.get_cached_doc(doctype, obj.get("name"))
        except BaseException:
            cached_doc = obj

        return get_doc_field_translation(
            doc=cached_doc, fieldname=info.field_name, value=value)
    return value
