from enum import Enum
from graphql import GraphQLResolveInfo

import frappe
from frappe.core.doctype.user.user import update_password


class ResetPasswordWithKeyErrorCodes(Enum):
    INVALID_KEY = "INVALID_KEY"
    WEAK_PASSWORD = "WEAK_PASSWORD"


def reset_pwd_with_key_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    key = kwargs.get("key")
    new_pwd = kwargs.get("new_password")

    r = frappe._dict(
        status="FAILED",
        error_code=None,
        user=None
    )

    if not key or not isinstance(key, str):
        r.error_code = ResetPasswordWithKeyErrorCodes.INVALID_KEY
    elif not new_pwd or not isinstance(new_pwd, str):
        r.error_code = ResetPasswordWithKeyErrorCodes.WEAK_PASSWORD

    if r.error_code:
        r.error_code = r.error_code.value
        return r

    try:
        response = update_password(
            new_password=new_pwd,
            key=key
        )
        if response == frappe._("The Link specified has either been used before or Invalid"):
            r.error_code = ResetPasswordWithKeyErrorCodes.INVALID_KEY
        elif frappe.session.user == "Guest":
            r.error_code = ResetPasswordWithKeyErrorCodes.INVALID_KEY

        if not r.error_code:
            r.status = "SUCCESS"
            r.user = frappe._dict(doctype="User", name=frappe.session.user)
    except Exception as e:
        msg = str(e)
        if frappe._("Invalid key type") in msg:
            r.error_code = ResetPasswordWithKeyErrorCodes.INVALID_KEY
        elif frappe._("Hint: Include symbols, numbers and capital letters in the password") in msg:
            r.error_code = ResetPasswordWithKeyErrorCodes.WEAK_PASSWORD

    if r.error_code:
        r.error_code = r.error_code.value

    return r
