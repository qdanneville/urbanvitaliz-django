from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from urbanvitaliz.apps.projects import models as projects_models
from urbanvitaliz.apps.survey import models as survey_models
from urbanvitaliz.utils import check_if_switchtender

from .utils import can_administrate_project, can_manage_project, get_active_project


def is_switchtender_processor(request):
    return {
        "is_switchtender": check_if_switchtender(request.user),
        "is_administrating_project": can_administrate_project(
            project=None, user=request.user
        ),
    }


def active_project_processor(request):
    active_project = get_active_project(request)
    context = {
        "active_project": active_project,
    }

    if active_project:
        try:
            survey = survey_models.Survey.on_site.get(pk=1)  # XXX Hardcoded survey ID
            session, created = survey_models.Session.objects.get_or_create(
                project=active_project, survey=survey
            )
        except survey_models.Survey.DoesNotExist:
            session = None

        # Retrieve notification count
        project_ct = ContentType.objects.get_for_model(projects_models.Project)
        project_notifications = request.user.notifications.filter(
            target_content_type=project_ct.pk,
            target_object_id=active_project.pk,
        )

        # Task notifications
        task_ct = ContentType.objects.get_for_model(projects_models.Task)
        task_followup_ct = ContentType.objects.get_for_model(
            projects_models.TaskFollowup
        )
        action_notification_count = (
            project_notifications.filter(
                Q(action_object_content_type=task_ct)
                | Q(action_object_content_type=task_followup_ct)
            )
            .unread()
            .count()
        )

        note_ct = ContentType.objects.get_for_model(projects_models.Note)
        # Conversations notifications
        conversations_notification_count = (
            project_notifications.filter(
                action_object_content_type=note_ct, action_notes__public=True
            )
            .unread()
            .count()
        )

        # Internal followup notifications
        followup_notification_count = (
            project_notifications.filter(
                action_object_content_type=note_ct, action_notes__public=False
            )
            .unread()
            .count()
        )

        context.update(
            {
                "active_project_can_manage": can_manage_project(
                    active_project, request.user
                ),
                "active_project_can_administrate": can_administrate_project(
                    active_project, request.user
                ),
                "active_project_survey_session": session,
                "active_project_action_notification_count": action_notification_count,
                "active_project_conversations_notification_count": conversations_notification_count,
                "active_project_followup_notification_count": followup_notification_count,
            }
        )

    return context
