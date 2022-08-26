from graphql import GraphQLResolveInfo, GraphQLError

import frappe
from frappe.auth import LoginManager

from renovation_core.utils.auth import pin_login


def login_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    user = kwargs.get("usr")
    pwd = kwargs.get("pwd")
    use_jwt = kwargs.get("use_jwt")
    frappe.local.form_dict.use_jwt = 1 if use_jwt else 0

    login = LoginManager()
    try:
        login.authenticate(user, pwd)
        login.post_login()
        login.run_trigger('on_session_creation')

        obj = frappe.local.response

        user_doc = frappe.get_doc("User", obj["user"])
        user_doc.apply_fieldlevel_read_permissions()

        obj["user"] = user_doc.as_dict(convert_dates_to_str=True)
    except frappe.AuthenticationError as e:
        raise GraphQLError("Invalid Credentials", original_error=e)
    except Exception as e:
        raise GraphQLError("Something went wrong", original_error=e)

    return obj


def pin_login_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    user = kwargs.get("user")
    pin = kwargs.get("pin")
    device = kwargs.get("device")

    pin_login(user, pin, device)

    obj = frappe.local.response
    obj["user"] = frappe._dict(doctype="User", name=obj["user"])

    return obj
