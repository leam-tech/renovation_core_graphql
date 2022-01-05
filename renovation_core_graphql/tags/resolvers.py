from graphql import GraphQLResolveInfo

import frappe
from frappe.desk.doctype.tag.tag import add_tag, remove_tag
from frappe.utils import cint


def add_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    """
    Add a tag to a specific document.
    Adding the same tag again is a no-op.
    """
    input = kwargs.get("input")
    doctype = input.get("doctype")
    docname = input.get("docname")
    tag = input.get("tag")
    return add_tag(tag=tag, dt=doctype, dn=docname)


def remove_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    """
    Remove a tag from a specific document.
    Removing a tag that does not exist is a no-op.
    """
    input = kwargs.get("input")
    doctype = input.get("doctype")
    docname = input.get("docname")
    tag = input.get("tag")
    remove_tag(tag=tag, dt=doctype, dn=docname)
    return True


def get_tags_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    """
    Get tags filtered by doctype and tag name. If none specified, return all tags.
    Default limitPageLength is 10.
    Default limitStart is 0.
    """
    filters = kwargs.get("filters") or {}
    doctype = filters.get("doctype")
    search = filters.get("search") or ""
    limit_start = cint(kwargs.get("limitStart")) or 0
    limit_page_length = cint(kwargs.get("limitPageLength")) or 10

    # This will return all tags in the system
    if not doctype:
        tags = frappe.get_all("Tag", filters={"name": ["like", "%{}%".format(search)]},
                              fields=["name"], limit_start=limit_start,
                              limit_page_length=limit_page_length)
        return [tag.get("name") for tag in tags]

    # This will return all tags for a specific doctype
    query = """
        SELECT DISTINCT tag FROM `tabTag Link`
         WHERE parenttype = %s AND tag LIKE %s
         LIMIT %s, %s
        """

    variables = [doctype, "%" + search + "%", limit_start, limit_page_length]

    return frappe.db.sql_list(query, variables)
