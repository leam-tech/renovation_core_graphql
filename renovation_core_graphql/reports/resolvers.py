import frappe
from frappe import unscrub
from frappe.desk.query_report import export_query
from graphql import GraphQLResolveInfo
from renovation_core.utils.report import get_report


def get_renovation_report_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    frappe.local.form_dict.report = kwargs.get("report")
    frappe.local.form_dict.filters = kwargs.get("filter")
    get_report()
    return frappe.local.response


def export_renovation_report_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    frappe.local.form_dict.report_name = kwargs.get("report_name")
    frappe.local.form_dict.filters = kwargs.get("filter", "[]")
    frappe.local.form_dict.file_format_type = unscrub(
        kwargs.get("file_format_type", ""))
    frappe.local.form_dict.custom_columns = kwargs.get("custom_columns")
    frappe.local.form_dict.include_indentation = kwargs.get(
        "include_indentation")
    frappe.local.form_dict.visible_idx = kwargs.get("visible_idx")
    export_query()
    ret = frappe.get_doc({
        "doctype": "File",
        "file_name": frappe.response["filename"],
        "is_private": 0,
        "content": frappe.response["filecontent"],
        "decode": False
    })
    ret.save()
    return ret.get("file_url")
