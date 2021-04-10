from graphql import GraphQLResolveInfo

import frappe

from renovation_core.utils.fcm import register_client, get_user_notifications, \
    mark_all_as_read, mark_notification_seen


def register_fcm_client_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = register_client(
        token=kwargs.get("token"),
        user=kwargs.get("user"),
        is_huawei_token=kwargs.get("is_huawei_token")
    )

    return frappe._dict(
        success=True if r == "OK" else False,
        **kwargs
    )


def get_user_notifications_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return get_user_notifications(
        just_unseen=True if kwargs.get("ignore_seen") else False
    )


def mark_all_fcm_read_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return frappe._dict(
        success=True if mark_all_as_read() == "Success" else False
    )


def mark_fcm_seen_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    r = mark_notification_seen(
        message_id=kwargs.get("message_id"),
        seen=kwargs.get("seen")
    )

    return frappe._dict(
        success=True if r == "OK" else False,
        **kwargs
    )
