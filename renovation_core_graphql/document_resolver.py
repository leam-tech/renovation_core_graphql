from graphql import GraphQLResolveInfo

import frappe
from frappe_graphql.utils.resolver import document_resolver, get_singular_doctype


def resolve(obj, info: GraphQLResolveInfo, **kwargs):
    # We are here just to implement our custom translation
    frappe.flags.ignore_doc_resolver_translation = True
    value = document_resolver(
        obj=obj, info=info, **kwargs
    )

    if isinstance(value, str):
        doctype = obj.get('doctype') or get_singular_doctype(info.parent_type.name)
        try:
            cached_doc = frappe.get_cached_doc(doctype, obj.get("name"))
        except BaseException:
            cached_doc = obj

        return get_translated(cached_doc, info.field_name, value)
    return value


def get_translated(doc, fieldname, value):
    """
    Precedence Order:
        key:doctype:name:fieldname
        key:doctype:name
        key:parenttype:parent
        key:doctype:fieldname
        key:doctype
        key:parenttype

        *:doctype:name:fieldname
        *:doctype:name
        *:parenttype:parent
        *:doctype:fieldname
        *:doctype
        *:parenttype

        key

    """
    if not isinstance(value, str):
        return value

    for v in (value, "*"):
        plain_translation = frappe._(v)

        # key:doctype:name:fieldname
        field_translation = frappe._(v, context=f"{doc.doctype}:{doc.name}:{fieldname}")
        if field_translation != plain_translation:
            return field_translation

        # key:doctype:name
        doc_translation = frappe._(v, context=f"{doc.doctype}:{doc.name}")
        if doc_translation != plain_translation:
            return doc_translation

        # key:parenttype:parent
        if doc.get("parenttype") and doc.get("parent"):
            parent_translation = frappe._(v, context=f"{doc.parenttype}:{doc.parent}")
            if parent_translation != plain_translation:
                return parent_translation

        # key:doctype:fieldname
        doctype_field_translation = frappe._(v, context=f"{doc.doctype}:{fieldname}")
        if doctype_field_translation != plain_translation:
            return doctype_field_translation

        # key:doctype
        doctype_translation = frappe._(v, context=f"{doc.doctype}")
        if doctype_translation != plain_translation:
            return doctype_translation

        if doc.get("parenttype"):
            parenttype_translation = frappe._(v, context=f"{doc.parenttype}")
            if parenttype_translation != plain_translation:
                return parenttype_translation

    return frappe._(value)
