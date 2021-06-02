import frappe
from frappe.desk.search import search_link
from graphql import GraphQLResolveInfo


def search_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    search_link(kwargs.get("doctype"), kwargs.get("txt", ""),
                kwargs.get("filters"), kwargs.get("page_length"),
                kwargs.get("searchfield"), kwargs.get("reference_doctype"))

    return frappe.response['results']
