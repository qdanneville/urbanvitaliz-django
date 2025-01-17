# encoding: utf-8

"""
Admin for project application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 13:55:23 CEST
"""


from csvexport.actions import csvexport
from django.contrib import admin
from ordered_model.admin import (OrderedInlineModelAdminMixin,
                                 OrderedTabularInline)

from . import models


class ProjectTaskTabularInline(OrderedTabularInline):
    model = models.Task
    fields = (
        "site",
        "intent",
        "content",
        "resource",
        "order",
        "move_up_down_links",
    )
    ordering = ("order", "site")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    extra = 1


class ProjectMemberTabularInline(admin.TabularInline):
    model = models.ProjectMember
    fields = (
        "member",
        "is_owner",
    )
    extra = 1


class ProjectSwitchtenderTabularInline(admin.TabularInline):
    model = models.ProjectSwitchtender
    fields = (
        "switchtender",
        "is_observer",
        "site",
    )
    extra = 1


@admin.register(models.Project)
class ProjectAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = [
        "sites",
        "created_on",
        "exclude_stats",
        "publish_to_cartofriches",
        "tags",
        "status",
    ]
    list_display = ["created_on", "name", "location"]
    actions = [csvexport]
    inlines = (
        ProjectMemberTabularInline,
        ProjectSwitchtenderTabularInline,
        ProjectTaskTabularInline,
    )


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ["content", "tags"]
    list_filter = ["tags", "created_on"]
    list_display = ["created_on", "project_name", "tags"]

    def project_name(self, o):
        return o.project.name


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ["content", "tags"]
    list_filter = ["site", "deadline", "tags"]
    list_display = ["created_on", "deadline", "project_name", "tags"]

    actions = [csvexport]

    def project_name(self, o):
        return o.project.name


@admin.register(models.TaskFollowup)
class TaskFollowupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaskFollowupRsvp)
class TaskFollowupRsvpAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaskRecommendation)
class TaskRecommendationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["description", "the_file"]
    list_filter = ["created_on"]
    list_display = ["created_on", "description", "the_file"]


# eof
