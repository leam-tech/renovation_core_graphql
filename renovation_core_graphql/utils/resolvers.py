import frappe
from enum import Enum

from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.core.doctype.data_import.exporter import Exporter
from frappe.desk.search import search_link
from graphql import GraphQLResolveInfo


def search_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    search_link(kwargs.get("doctype"), kwargs.get("txt", ""),
                filters=kwargs.get("filters"),
                page_length=kwargs.get("page_length"),
                searchfield=kwargs.get("searchfield"),
                reference_doctype=kwargs.get("reference_doctype"))

    return frappe.response['results']


EXPORT_DATA_FILE_EXPIRY_IN_HOURS = 1


def export_data_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    doctype = kwargs.get("doctype")
    select_columns = kwargs.get("select_columns")
    # Excel only supported now..
    file_type = ExportDataFileType(kwargs.get("file_type")).name if kwargs.get(
        "file_type") else ExportDataFileType.Excel.name
    filters = kwargs.get("filters")

    make_access_log(doctype=doctype, file_type=file_type, columns=select_columns, filters=filters)
    exporter = Exporter(doctype=doctype, export_fields=frappe.parse_json(select_columns or '{}'),
                        export_data=True, file_type=file_type,
                        export_filters=frappe.parse_json(filters or '[]'))
    exporter.build_response()
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": frappe.response["filename"],
        "is_private": 0,
        "content": frappe.response["filecontent"],
        "decode": False
    })
    file_doc.save(ignore_permissions=True)
    frappe.get_doc({
        "doctype": "Temporary File",
        "file": file_doc.file_url,
        "expires_in_hours": EXPORT_DATA_FILE_EXPIRY_IN_HOURS
    }).insert(ignore_permissions=True)
    return file_doc.get("file_url")


class ExportDataFileType(Enum):
    Excel = "EXCEL"
    CSV = "CSV"
