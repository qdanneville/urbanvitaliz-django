# encoding: utf-8

"""
Urls for crm application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2022-07-19 17:27:25 CEST
"""


from django.urls import path

from . import views

urlpatterns = [
    path(
        r"crm/org/<int:organization_id>/",
        views.organization_details,
        name="crm-organization-details",
    ),
    path(
        r"crm/user/<int:user_id>/",
        views.user_details,
        name="crm-user-details",
    ),
    path(
        r"crm/project/<int:project_id>/",
        views.project_details,
        name="crm-project-details",
    ),
]