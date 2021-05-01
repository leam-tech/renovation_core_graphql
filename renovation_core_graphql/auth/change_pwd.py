from graphql import GraphQLResolveInfo

import frappe
from renovation_core.utils.auth import change_password


def change_pwd_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    status = "FAILED"
    if change_password(**kwargs):
        status = "SUCCESS"

    return frappe._dict(status=status, user=frappe._dict(
        doctype="User",
        name=frappe.session.user
    ))
