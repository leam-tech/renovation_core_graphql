import frappe
from graphql import GraphQLResolveInfo
from renovation_core.utils.translate import get_doc_translations


def get_doc_translation_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    dt = kwargs.get("doctype", None)
    dn = kwargs.get("name", None)
    translation = get_doc_translations(doctype=dt, name=dn)

    data = []
    meta = frappe.get_meta(dt)
    doc = frappe.get_cached_doc(dt, dn)
    for lang, field_dict in translation.items():
        for fieldname, value in field_dict.items():
            df = meta.get_field(fieldname)
            tr_item = frappe._dict(
                language=frappe._dict(doctype="Language", name=lang),
                language__name=lang,
                docfield=frappe._dict(doctype="DocField", name=df.name),
                fieldname=fieldname,
                fieldtype=df.fieldtype,
            )
            if df.fieldtype == "Select":
                tr_item.source_text = doc.get(fieldname)
                tr_item.translated_text = value.value

                for select_src_text, select_value in value.get("values", {}).items():
                    if select_src_text == doc.get(fieldname):
                        continue
                    tr_copy = frappe._dict(tr_item)
                    tr_copy.source_text = select_src_text
                    tr_copy.translated_text = select_value
                    data.append(tr_copy)
            else:
                tr_item.source_text = doc.get(fieldname)
                tr_item.translated_text = value

            data.append(tr_item)

    return data
