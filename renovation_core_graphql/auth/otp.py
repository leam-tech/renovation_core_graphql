from graphql import GraphQLResolveInfo

import frappe

from renovation_core.utils.auth import generate_otp, verify_otp


VERIFY_OTP_STATUS_MAP = {
    "no_linked_user": "NO_LINKED_USER",
    "no_otp_for_mobile": "NO_OTP_GENERATED",
    "invalid_otp": "INVALID_OTP",
    "verified": "VERIFIED",
}


def generate_otp_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = generate_otp(**kwargs)
    r.status = "SUCCESS" if r.status == "success" else "FAILED"
    return r


def verify_otp_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    kwargs["login_to_user"] = 1 if kwargs.get("login_to_user") else 0
    if kwargs["login_to_user"] and kwargs["use_jwt"]:
        frappe.local.form_dict.use_jwt = 1
        del kwargs["use_jwt"]

    status_dict = verify_otp(**kwargs)
    status_dict.update(frappe.local.response)
    if status_dict.get("user"):
        user_doc = frappe.get_doc("User", status_dict["user"])
        user_doc.apply_fieldlevel_read_permissions()

        status_dict["user"] = user_doc.as_dict(convert_dates_to_str=True)

    status = status_dict.get("status")
    if status in VERIFY_OTP_STATUS_MAP:
        status_dict.status = VERIFY_OTP_STATUS_MAP[status]
    else:
        status_dict.status = "FAILED"
    return status_dict
