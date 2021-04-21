from graphql import GraphQLResolveInfo

import frappe
from frappe.utils.password import update_password
from renovation_core.utils.auth import verify_otp, get_linked_user

from .otp import VERIFY_OTP_STATUS_MAP


def reset_pwd_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    user = get_linked_user(id_type=kwargs.get("medium"), id=kwargs.get("medium_id"))
    new_password = kwargs.get("new_password")
    if not user:
        return frappe._dict(status="NO_LINKED_USER")

    user = frappe.get_doc("User", user)
    r = verify_otp(
        medium=kwargs.get("medium"),
        medium_id=kwargs.get("medium_id"),
        otp=kwargs.get("otp"),
        purpose="reset_password"
    )

    if r.status != "verified":
        status = "FAILED"
        if r.status in VERIFY_OTP_STATUS_MAP:
            status = VERIFY_OTP_STATUS_MAP[r.status]

        return frappe._dict(status=status, user=user)

    from frappe.core.doctype.user.user import test_password_strength
    user_data = (user.first_name, user.middle_name,
                 user.last_name, user.email, user.birth_date)
    result = test_password_strength(new_password, '', None, user_data)
    feedback = result.get("feedback", None)

    if feedback and not feedback.get('password_policy_validation_passed', False):
        return frappe._dict(status="WEAK_PASSWORD", user=user)

    update_password(user.name, new_password)
    return frappe._dict(status="SUCCESS", user=user)
