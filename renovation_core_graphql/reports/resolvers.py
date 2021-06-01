import frappe
from graphql import GraphQLResolveInfo
from renovation_core.utils.report import get_report


def get_renovation_report_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    frappe.local.form_dict.report = kwargs.get("report")
    frappe.local.form_dict.filters = kwargs.get("filter")
    get_report()
    return frappe.local.response
