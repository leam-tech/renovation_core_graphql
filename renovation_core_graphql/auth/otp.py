from graphql import GraphQLResolveInfo

import frappe

from renovation_core.utils.auth import generate_otp, verify_otp


def generate_otp_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return generate_otp(**kwargs)


def verify_otp_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    kwargs["login_to_user"] = 1 if kwargs.get("login_to_user") else 0
    if kwargs["login_to_user"] and kwargs["use_jwt"]:
        frappe.local.form_dict.use_jwt = 1
        del kwargs["use_jwt"]

    status_dict = verify_otp(**kwargs)
    status_dict.update(frappe.local.response)
    if status_dict["user"]:
        status_dict["user"] = frappe._dict(doctype="User", name=status_dict["user"])
    return status_dict
