# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version  # noqa

app_name = "renovation_core_graphql"
app_title = "Renovation Core Graphql"
app_publisher = "Leam Technology Systems"
app_description = "GraphQL Wrapper for renovation_core"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@leam.ae"
app_license = "MIT"

graphql_sdl_dir = [
    "./renovation_core_graphql/renovation_core_graphql/auth/sdls",
    "./renovation_core_graphql/renovation_core_graphql/model/sdls",
    "./renovation_core_graphql/renovation_core_graphql/notifications/sdls",
]

graphql_schema_processors = [
    "renovation_core_graphql.auth.bind_schema",
    "renovation_core_graphql.model.bind_schema",
    "renovation_core_graphql.notifications.bind_schema",
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/renovation_core_graphql/css/renovation_core_graphql.css"
# app_include_js = "/assets/renovation_core_graphql/js/renovation_core_graphql.js"

# include js, css files in header of web template
# web_include_css = "/assets/renovation_core_graphql/css/renovation_core_graphql.css"
# web_include_js = "/assets/renovation_core_graphql/js/renovation_core_graphql.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "renovation_core_graphql/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#   "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "renovation_core_graphql.install.before_install"
# after_install = "renovation_core_graphql.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "renovation_core_graphql.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#   }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"renovation_core_graphql.tasks.all"
# 	],
# 	"daily": [
# 		"renovation_core_graphql.tasks.daily"
# 	],
# 	"hourly": [
# 		"renovation_core_graphql.tasks.hourly"
# 	],
# 	"weekly": [
# 		"renovation_core_graphql.tasks.weekly"
# 	]
# 	"monthly": [
# 		"renovation_core_graphql.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "renovation_core_graphql.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "renovation_core_graphql.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "renovation_core_graphql.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
