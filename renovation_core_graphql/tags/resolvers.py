from graphql import GraphQLResolveInfo

import frappe
from frappe.desk.doctype.tag.tag import add_tag, remove_tag, get_tags


def add_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    input = kwargs.get("input")
    doctype = input.get("doctype")
    docname = input.get("docname")
    tag = input.get("tag")
    return add_tag(tag=tag, dt=doctype, dn=docname)


def remove_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    input = kwargs.get("input")
    doctype = input.get("doctype")
    docname = input.get("docname")
    tag = input.get("tag")
    remove_tag(tag=tag, dt=doctype, dn=docname)
    return True


def get_tags_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    doctype = kwargs.get("doctype")
    search = kwargs.get("search") or ""

    # This will return all tags in the system
    if not doctype:
        return get_tags(doctype, search)

    # This will return all tags for a specific doctype
    query = """
        SELECT DISTINCT tag FROM `tabTag Link`
         WHERE parenttype = %s AND tag LIKE %s
        """
    tags = frappe.db.sql(query, [doctype, "%" + search + "%"], as_dict=True, debug=1)
    return [tag.get("tag") for tag in tags]
