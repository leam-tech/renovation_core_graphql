from graphql import GraphQLResolveInfo

import frappe
from renovation_core.utils.auth import change_password


def change_pwd_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    status = "fail"
    if change_password(**kwargs):
        status = "success"

    return frappe._dict(status=status)
