from graphql import GraphQLResolveInfo

import frappe
from renovation_core.utils.auth import change_password


def change_pwd_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    status = "FAILED"
    if change_password(**kwargs):
        status = "SUCCESS"

    user_doc = frappe.get_doc("User", frappe.session.user)
    user_doc.apply_fieldlevel_read_permissions()

    return frappe._dict(status=status, user=user_doc.as_dict(convert_dates_to_str=True))
