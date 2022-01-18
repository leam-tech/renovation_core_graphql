from graphql import GraphQLResolveInfo

import frappe
from frappe.desk.doctype.tag.tag import add_tag, remove_tag
from frappe.utils import cint
from frappe_graphql.api import get_query


def add_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    """
    Add a tag to a specific document.
    Adding the same tag again is a no-op.
    """
    r = frappe._dict(success_count=0, failure_count=0, total_count=len(kwargs.get("input")))
    error_outputs = []
    for tag_input in kwargs.get("input"):
        try:
            doctype = tag_input.get("doctype")
            docname = tag_input.get("docname")
            tag = tag_input.get("tag")
            add_tag(tag=tag, dt=doctype, dn=docname)
            frappe.db.commit()
            r.success_count += 1
        except Exception as e:
            frappe.db.rollback()
            r.failure_count += 1
            error_outputs.append(e)
    if len(error_outputs):
        query, variables, operation_name = get_query()
        log_tag_link_errors(query, variables, operation_name,
                            {
                                "success_count": r.success_count,
                                "failure_count": r.failure_count,
                                "total_count": r.total_count
                            },
                            error_outputs)
    return r


def remove_tag_link_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    """
    Remove a tag from a specific document.
    Removing a tag that does not exist is a no-op.
    """
    r = frappe._dict(success_count=0, failure_count=0, total_count=len(kwargs.get("input")))
    error_outputs = []
    for tag_input in kwargs.get("input"):
        try:
            doctype = tag_input.get("doctype")
            docname = tag_input.get("docname")
            tag = tag_input.get("tag")
            remove_tag(tag=tag, dt=doctype, dn=docname)
            frappe.db.commit()
            r.success_count += 1
        except Exception as e:
            frappe.db.rollback()
            r.failure_count += 1
            error_outputs.append(e)
    if len(error_outputs):
        query, variables, operation_name = get_query()
        log_tag_link_errors(query, variables, operation_name,
                            {
                                "success_count": r.success_count,
                                "failure_count": r.failure_count,
                                "total_count": r.total_count
                            },
                            error_outputs)
    return r


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


def log_tag_link_errors(query, variables, operation_name, graphql_output,
                        error_outputs):
    import frappe
    from frappe_graphql.utils.http import get_operation_name, get_masked_variables
    tracebacks = get_tag_link_errors_tracebacks(error_outputs)
    error_log = frappe.new_doc("GraphQL Error Log")
    error_log.update(frappe._dict(
        title="GraphQL API Error",
        operation_name=get_operation_name(query, operation_name),
        query=query,
        variables=frappe.as_json(
            get_masked_variables(query, variables)) if variables else None,
        output=frappe.as_json(graphql_output),
        traceback=tracebacks
    ))
    error_log.insert(ignore_permissions=True)


def get_tag_link_errors_tracebacks(error_outputs):
    import frappe
    import traceback as tb
    tracebacks = [f"Total Errors : {len(error_outputs)}"]
    for idx, error_output in enumerate(error_outputs):
        tracebacks.append(
            f"Error #{idx + 1}\n"
            f"Http Status Code: {error_output.http_status_code}\n\n" + \
            f"{str(error_output)}\n\n" + \
            f"{''.join(tb.format_exception(error_output, error_output, error_output.__traceback__))}")
    tracebacks = "\n==========================================\n".join(
        tracebacks)
    if frappe.conf.get("developer_mode"):
        frappe.errprint(tracebacks)
    return tracebacks
