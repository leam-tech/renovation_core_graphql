from graphql import GraphQLResolveInfo

import frappe
from frappe.auth import LoginManager

from renovation_core.utils.auth import pin_login


def login_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    user = kwargs.get("usr")
    pwd = kwargs.get("pwd")
    use_jwt = kwargs.get("use_jwt")
    frappe.local.form_dict.use_jwt = 1 if use_jwt else 0

    login = LoginManager()
    login.authenticate(user, pwd)
    login.post_login()
    login.run_trigger('on_session_creation')

    obj = frappe.local.response
    obj["user"] = frappe._dict(doctype="User", name=obj["user"])

    return obj


def pin_login_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    user = kwargs.get("user")
    pin = kwargs.get("pin")
    device = kwargs.get("device")

    pin_login(user, pin, device)

    obj = frappe.local.response
    obj["user"] = frappe._dict(doctype="User", name=obj["user"])

    return obj
