from graphql import GraphQLResolveInfo

import frappe
from frappe.desk.form.assign_to import remove, add, set_status
from renovation_core.utils.assign_doc import getDocsAssignedToUser, getUsersAssignedToDoc


def get_docs_assigned_to_user_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = getDocsAssignedToUser(
        user=kwargs.get("user"),
        doctype=kwargs.get("doctype"),
        status=kwargs.get("status"),
    )

    for todo in r:
        todo.due_date = todo.dueDate
        todo.reference_type = todo.doctype
        todo.reference_name = todo.docname
        todo.assigned_by = frappe._dict(doctype="User", name=todo.assignedBy)
        todo.assigned_to = frappe._dict(doctype="User", name=todo.assignedTo)

    return r


def get_users_assigned_to_doc_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = getUsersAssignedToDoc(
        doctype=kwargs.get("doctype"),
        name=kwargs.get("name")
    )

    for todo in r:
        todo.due_date = todo.dueDate
        todo.reference_type = kwargs.get("doctype")
        todo.reference_name = kwargs.get("name")
        todo.assigned_by = frappe._dict(doctype="User", name=todo.assignedBy)
        todo.assigned_to = frappe._dict(doctype="User", name=todo.assignedTo)

    return r


def assign_doc_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = add(args=frappe._dict(
        assign_to=[kwargs.get("assign_to")],
        doctype=kwargs.get("doctype"),
        name=kwargs.get("name"),
        description=kwargs.get("description"),
        date=kwargs.get("due_date")
    ))

    for todo in r:
        todo.update(frappe.get_doc("ToDo", todo.name).as_dict())
        todo.name = None
        todo.doctype = None
        todo.due_date = todo.date
        todo.assigned_to = frappe._dict(doctype="User", name=todo.owner)
        todo.assigned_by = frappe._dict(doctype="User", name=todo.assigned_by)

    return r


def unassign_doc_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = remove(
        doctype=kwargs.get("doctype"),
        name=kwargs.get("name"),
        assign_to=kwargs.get("assign_to")
    )

    for todo in r:
        todo.update(frappe.get_doc("ToDo", todo.name).as_dict())
        todo.name = None
        todo.doctype = None
        todo.due_date = todo.date
        todo.assigned_to = frappe._dict(doctype="User", name=todo.owner)
        todo.assigned_by = frappe._dict(doctype="User", name=todo.assigned_by)

    return r


def set_assignment_status_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = set_status(
        doctype=kwargs.get("doctype"),
        name=kwargs.get("name"),
        assign_to=kwargs.get("assign_to"),
        status="Closed"
    )

    for todo in r:
        todo.update(frappe.get_doc("ToDo", todo.name).as_dict())
        todo.name = None
        todo.doctype = None
        todo.due_date = todo.date
        todo.assigned_to = frappe._dict(doctype="User", name=todo.owner)
        todo.assigned_by = frappe._dict(doctype="User", name=todo.assigned_by)

    return r
